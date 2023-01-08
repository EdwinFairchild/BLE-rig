#include "ble_rig.h"

#define MXC_GPIO_PORT_OUT MXC_GPIO0
#define MXC_GPIO_PIN_OUT MXC_GPIO_PIN_19
#define RED_LED_PIN MXC_GPIO_PIN_OUT
#define RED_LED_PORT MXC_GPIO_PORT_OUT

/* Mutual exclusion (mutex) semaphores */
SemaphoreHandle_t xGPIOmutex;
mxc_gpio_cfg_t gpio_out;
/* Task IDs */
TaskHandle_t vTask1_hdl;
// http://home.thep.lu.se/~bjorn/crc/
/*************************************************************************************************/
/*!
 *  \brief  Create the CRC32 table.
 *
 *  \param  r       Index into the table
 *
 *  \return None.
 */
/*************************************************************************************************/
uint32_t crc32_for_byte(uint32_t r) {
  for (int j = 0; j < 8; ++j)
    r = (r & 1 ? 0 : (uint32_t)0xEDB88320L) ^ r >> 1;
  return r ^ (uint32_t)0xFF000000L;
}

/*************************************************************************************************/
/*!
 *  \brief  Calculate the CRC32 value for the given buffer.
 *
 *  \param  data    Pointer to the data.
 *  \param  n_bytes Number of bytes in the buffer.
 *  \param  crc     Pointer to store the result.
 *
 *  \return None.
 */
/*************************************************************************************************/
static uint32_t table[0x100] = {0};
void crc32(const void *data, size_t n_bytes, uint32_t *crc) {
  if (!*table) {
    for (size_t i = 0; i < 0x100; ++i)
      table[i] = crc32_for_byte(i);
  }
  for (size_t i = 0; i < n_bytes; ++i) {
    *crc = table[(uint8_t)*crc ^ ((uint8_t *)data)[i]] ^ *crc >> 8;
  }
}

void config_gpio(void) {

  /* Setup output pin. */
  gpio_out.port = RED_LED_PORT;
  gpio_out.mask = RED_LED_PIN;
  gpio_out.pad = MXC_GPIO_PAD_NONE;
  gpio_out.func = MXC_GPIO_FUNC_OUT;
  gpio_out.vssel = MXC_GPIO_VSSEL_VDDIOH;
  MXC_GPIO_Config(&gpio_out);
}

void vTask1(void *pvParameters) {
  TickType_t xLastWakeTime;
  unsigned int x = LED_ON;

  /* Get task start time */
  xLastWakeTime = xTaskGetTickCount();
  uint32_t notificationValue;
  bool state = false;
  while (1) {
    xTaskNotifyWait(0x00, 0xFFFFFFFF, &notificationValue, portMAX_DELAY);
    APP_TRACE_INFO3("ME14: %d\r\nME17: %d \r\nME18: %d",
                    (notificationValue & 0x01), (notificationValue & 0x02),
                    (notificationValue & 0x03));

    if (state == true) {
      MXC_GPIO_OutSet(gpio_out.port, gpio_out.mask);
      state = false;
    } else {
      MXC_GPIO_OutClr(gpio_out.port, gpio_out.mask);
      state = true;
    }

    // if (xSemaphoreTake(xGPIOmutex, portMAX_DELAY) == pdTRUE) {

    //     /* Return the mutex after we have modified the hardware state */
    //     xSemaphoreGive(xGPIOmutex);
    // }
  }
}
extern TaskHandle_t vTask1_hdl;
uint8_t datsWpWriteCback(dmConnId_t connId, uint16_t handle, uint8_t operation,
                         uint16_t offset, uint16_t len, uint8_t *pValue,
                         attsAttr_t *pAttr) {
  powerOptions_t temp;
  uint32_t crcResult = 0x00000000;
  int err = 0;
  if (len == sizeof(powerOptions_t)) {
    memcpy(&temp, pValue, sizeof(powerOptions_t));
    // calculate crc32 starting from second element
    crc32(&temp.packet_type, sizeof(powerOptions_t) - 4, &crcResult);
    if (crcResult == temp.crc32) {
      // process message
      uint32_t valueToSend =
          (temp.me14_state << 0 | temp.me17_state << 1 | temp.me18_state << 2);
      xTaskNotify(vTask1_hdl, valueToSend, eSetValueWithOverwrite);

    } else {
      // TODO implement retry
      APP_TRACE_INFO0("CRC did not mathc");
      err++;
    }

  } else {
    APP_TRACE_INFO0("Len did not match");
  }
  // if (len < 64) {
  //     /* print received data if not a speed test message */
  //     APP_TRACE_INFO0((const char *)pValue);

  //     /* send back some data */
  //     datsSendData(connId);
  // }
  return ATT_SUCCESS;
}
void freeRTOS_init(void) {
  /* Create mutexes */
  xGPIOmutex = xSemaphoreCreateMutex();
  if (xGPIOmutex == NULL) {
    APP_TRACE_INFO0("xSemaphoreCreateMutex failed to create a mutex.\n");
  }

  // start tasks
  if (xTaskCreate(vTask1, (const char *)"Task1", configMINIMAL_STACK_SIZE, NULL,
                  tskIDLE_PRIORITY + 1, &vTask1_hdl) != pdPASS) {
    APP_TRACE_INFO0("Failed to create task");

  } else {
    APP_TRACE_INFO0("Task 1 created!");
  }
}