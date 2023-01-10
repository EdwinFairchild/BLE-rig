#include "ble_rig.h"

#define ME17_MAIN_PORT MXC_GPIO0
#define ME17_MAIN_PIN MXC_GPIO_PIN_25

#define ME17_PORT MXC_GPIO0
#define ME17_PIN MXC_GPIO_PIN_24

#define ME14_PORT MXC_GPIO0
#define ME14_PIN MXC_GPIO_PIN_20

#define ME18_PORT MXC_GPIO1
#define ME18_PIN MXC_GPIO_PIN_8

/* Mutual exclusion (mutex) semaphores */
SemaphoreHandle_t xGPIOmutex;
mxc_gpio_cfg_t gpio_out;
/* Task IDs */
TaskHandle_t vTask1_hdl;
powerOptions_t power_ctl;
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
  gpio_out.port = ME17_MAIN_PORT;
  gpio_out.mask = ME17_MAIN_PIN;
  gpio_out.pad = MXC_GPIO_PAD_NONE;
  gpio_out.func = MXC_GPIO_FUNC_OUT;
  gpio_out.vssel = MXC_GPIO_VSSEL_VDDIOH;
  MXC_GPIO_Config(&gpio_out);

  gpio_out.mask = ME17_PIN;
  MXC_GPIO_Config(&gpio_out);

  gpio_out.mask = ME14_PIN;
  MXC_GPIO_Config(&gpio_out);

  gpio_out.port = ME18_PORT;
  gpio_out.mask = ME18_PIN;
  MXC_GPIO_Config(&gpio_out);
  APP_TRACE_INFO1("Size of enum %d", sizeof(packet_t));
}

void vTask1(void *pvParameters) {
  TickType_t xLastWakeTime;
  unsigned int x = LED_ON;

  /* Get task start time */
  xLastWakeTime = xTaskGetTickCount();
  powerOptions_t *powerOptions;

  bool state = false;
  while (1) {
    xTaskNotifyWait(0x00, 0xFFFFFFFF, &powerOptions, portMAX_DELAY);
    if (powerOptions->all_on == true) {
      MXC_GPIO_OutSet(ME17_MAIN_PORT, ME17_MAIN_PIN);
      MXC_GPIO_OutSet(ME17_PORT, ME17_PIN);
      MXC_GPIO_OutSet(ME14_PORT, ME14_PIN);
      MXC_GPIO_OutSet(ME18_PORT, ME18_PIN);
      APP_TRACE_INFO0("All on");

    } else if (powerOptions->all_off == true) {
      MXC_GPIO_OutClr(ME17_MAIN_PORT, ME17_MAIN_PIN);
      MXC_GPIO_OutClr(ME17_PORT, ME17_PIN);
      MXC_GPIO_OutClr(ME14_PORT, ME14_PIN);
      MXC_GPIO_OutClr(ME18_PORT, ME18_PIN);
      APP_TRACE_INFO0("All off");

    } else {

      if (powerOptions->me17_main_state) {
        APP_TRACE_INFO0("ME17 Main turned on");
        MXC_GPIO_OutSet(ME17_MAIN_PORT, ME17_MAIN_PIN);
      } else {
        APP_TRACE_INFO0("ME17 Main turned off");
        MXC_GPIO_OutClr(ME17_MAIN_PORT, ME17_MAIN_PIN);
      }

      if (powerOptions->me17_state) {
        APP_TRACE_INFO0("ME17 turned on");
        MXC_GPIO_OutSet(ME17_PORT, ME17_PIN);
      } else {
        APP_TRACE_INFO0("ME17 turned off");
        MXC_GPIO_OutClr(ME17_PORT, ME17_PIN);
      }

      if (powerOptions->me14_state) {
        APP_TRACE_INFO0("ME14 turned on");
        MXC_GPIO_OutSet(ME14_PORT, ME14_PIN);
      } else {
        APP_TRACE_INFO0("ME14 turned off");
        MXC_GPIO_OutClr(ME14_PORT, ME14_PIN);
      }

      if (powerOptions->me18_state) {
        APP_TRACE_INFO0("ME18 turned on");
        MXC_GPIO_OutSet(ME18_PORT, ME18_PIN);
      } else {
        APP_TRACE_INFO0("ME18 turned off");
        MXC_GPIO_OutClr(ME18_PORT, ME18_PIN);
      }
    }
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
    // calculate crc32 starting from second element

    memcpy(&power_ctl, pValue, sizeof(powerOptions_t));
    // Xnotify value passed is address of powerOptions
    xTaskNotify(vTask1_hdl, &power_ctl, eSetValueWithOverwrite);
    // // crc32 to validate packet
    // memcpy(&temp, pValue, sizeof(powerOptions_t));
    // crc32(&temp.packet_type, sizeof(powerOptions_t) - 4, &crcResult);
    // if (crcResult == temp.crc32) {
    //   // copy to cached version
    //   memcpy(&power_ctl, &temp, sizeof(powerOptions_t));
    //   // Xnotify value passed is address of powerOptions
    //   xTaskNotify(vTask1_hdl, &power_ctl, eSetValueWithOverwrite);

    // } else {
    //   // TODO implement retry
    //   APP_TRACE_INFO0("CRC did not mathc");
    //   err++;
    // }

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