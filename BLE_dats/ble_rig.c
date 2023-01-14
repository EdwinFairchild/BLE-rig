#include "ble_rig.h"

#define ME17_MAIN_PORT MXC_GPIO0
#define ME17_MAIN_PIN MXC_GPIO_PIN_25

#define ME17_PORT MXC_GPIO0
#define ME17_PIN MXC_GPIO_PIN_24

#define ME14_PORT MXC_GPIO0
#define ME14_PIN MXC_GPIO_PIN_20

#define ME18_PORT MXC_GPIO1
#define ME18_PIN MXC_GPIO_PIN_8

powerOptions_t power_ctl;
uint8_t hanlderId = 0;
/*! \brief    Custom Command Handler. */
static uint8_t cmd_me17MainState(uint32_t argc, char **argv);
static uint8_t cmd_me17State(uint32_t argc, char **argv);
static uint8_t cmd_me14State(uint32_t argc, char **argv);
static uint8_t cmd_me18State(uint32_t argc, char **argv);
static uint8_t cmd_allOn(uint32_t argc, char **argv);
static uint8_t cmd_allOff(uint32_t argc, char **argv);
/*! \brief    command list */
terminalCommand_t appTerminalCustomCommandList[] = {

    {NULL, "me17main", "<power state>>", cmd_me17MainState},
    {NULL, "me17", "<power state>>", cmd_me17State},
    {NULL, "me14", "<power state>>", cmd_me14State},
    {NULL, "me18", "<power state>>", cmd_me18State},
    {NULL, "allon", "<power state>>", cmd_allOn},
    {NULL, "alloff", "<power state>>", cmd_allOff},
    {NULL, NULL, NULL, NULL}, // used as delimter for end of list

};
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

mxc_gpio_cfg_t gpio_out;
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

void parsePacket() {

  if (power_ctl.all_on == true) {
    MXC_GPIO_OutSet(ME17_MAIN_PORT, ME17_MAIN_PIN);
    MXC_GPIO_OutSet(ME17_PORT, ME17_PIN);
    MXC_GPIO_OutSet(ME14_PORT, ME14_PIN);
    MXC_GPIO_OutSet(ME18_PORT, ME18_PIN);
    APP_TRACE_INFO0("All on");

  } else if (power_ctl.all_off == true) {
    MXC_GPIO_OutClr(ME17_MAIN_PORT, ME17_MAIN_PIN);
    MXC_GPIO_OutClr(ME17_PORT, ME17_PIN);
    MXC_GPIO_OutClr(ME14_PORT, ME14_PIN);
    MXC_GPIO_OutClr(ME18_PORT, ME18_PIN);
    APP_TRACE_INFO0("All off");

  } else {

    if (power_ctl.me17_main_state) {
      APP_TRACE_INFO0("ME17 Main turned on");
      MXC_GPIO_OutSet(ME17_MAIN_PORT, ME17_MAIN_PIN);
    } else {
      APP_TRACE_INFO0("ME17 Main turned off");
      MXC_GPIO_OutClr(ME17_MAIN_PORT, ME17_MAIN_PIN);
    }

    if (power_ctl.me17_state) {
      APP_TRACE_INFO0("ME17 turned on");
      MXC_GPIO_OutSet(ME17_PORT, ME17_PIN);
    } else {
      APP_TRACE_INFO0("ME17 turned off");
      MXC_GPIO_OutClr(ME17_PORT, ME17_PIN);
    }

    if (power_ctl.me14_state) {
      APP_TRACE_INFO0("ME14 turned on");
      MXC_GPIO_OutSet(ME14_PORT, ME14_PIN);
    } else {
      APP_TRACE_INFO0("ME14 turned off");
      MXC_GPIO_OutClr(ME14_PORT, ME14_PIN);
    }

    if (power_ctl.me18_state) {
      APP_TRACE_INFO0("ME18 turned on");
      MXC_GPIO_OutSet(ME18_PORT, ME18_PIN);
    } else {
      APP_TRACE_INFO0("ME18 turned off");
      MXC_GPIO_OutClr(ME18_PORT, ME18_PIN);
    }
  }
}
/*************************************************************************************************/
/*!
 *  \brief  Handler for a custom terminal command.
 *
 *  \param  argc      The number of arguments passed to the command.
 *  \param  argv      The array of arguments; the 0th argument is the command.
 *
 *  \return Error code.
 */
/*************************************************************************************************/
static uint8_t cmd_me17MainState(uint32_t argc, char **argv) {
  dmEvt_t *pMsg;
  pMsg = WsfMsgAlloc(sizeof(attEvt_t));
  pMsg->hdr.event = DM_VENDOR_SPEC_IND;

  if (argc < 2) {
    return TERMINAL_ERROR_TOO_FEW_ARGUMENTS;
  } else if (argc == 2) {
    if (atoi(argv[1]) == 1) {

      power_ctl.me17_main_state = ON;
    } else {

      power_ctl.me17_main_state = OFF;
    }
    WsfMsgSend(hanlderId, pMsg);
  } else {
    return TERMINAL_ERROR_TOO_MANY_ARGUMENTS;
  }

  return TERMINAL_ERROR_OK;
}
static uint8_t cmd_me17State(uint32_t argc, char **argv) {
  dmEvt_t *pMsg;
  pMsg = WsfMsgAlloc(sizeof(attEvt_t));
  pMsg->hdr.event = DM_VENDOR_SPEC_IND;

  if (argc < 2) {
    return TERMINAL_ERROR_TOO_FEW_ARGUMENTS;
  } else if (argc == 2) {
    if (atoi(argv[1]) == 1) {

      power_ctl.me17_state = ON;
    } else {

      power_ctl.me17_state = OFF;
    }
    WsfMsgSend(hanlderId, pMsg);
  } else {
    return TERMINAL_ERROR_TOO_MANY_ARGUMENTS;
  }

  return TERMINAL_ERROR_OK;
}
static uint8_t cmd_me14State(uint32_t argc, char **argv) {
  dmEvt_t *pMsg;
  pMsg = WsfMsgAlloc(sizeof(attEvt_t));
  pMsg->hdr.event = DM_VENDOR_SPEC_IND;

  if (argc < 2) {
    return TERMINAL_ERROR_TOO_FEW_ARGUMENTS;
  } else if (argc == 2) {
    if (atoi(argv[1]) == 1) {

      power_ctl.me14_state = ON;
    } else {

      power_ctl.me14_state = OFF;
    }
    WsfMsgSend(hanlderId, pMsg);
  } else {
    return TERMINAL_ERROR_TOO_MANY_ARGUMENTS;
  }

  return TERMINAL_ERROR_OK;
}
static uint8_t cmd_me18State(uint32_t argc, char **argv) {
  dmEvt_t *pMsg;
  pMsg = WsfMsgAlloc(sizeof(attEvt_t));
  pMsg->hdr.event = DM_VENDOR_SPEC_IND;

  if (argc < 2) {
    return TERMINAL_ERROR_TOO_FEW_ARGUMENTS;
  } else if (argc == 2) {
    if (atoi(argv[1]) == 1) {

      power_ctl.me18_state = ON;
    } else {

      power_ctl.me18_state = OFF;
    }
    WsfMsgSend(hanlderId, pMsg);
  } else {
    return TERMINAL_ERROR_TOO_MANY_ARGUMENTS;
  }

  return TERMINAL_ERROR_OK;
}
static uint8_t cmd_allOn(uint32_t argc, char **argv) {
  dmEvt_t *pMsg;
  pMsg = WsfMsgAlloc(sizeof(attEvt_t));
  pMsg->hdr.event = DM_VENDOR_SPEC_IND;

  if (argc < 1) {
    return TERMINAL_ERROR_TOO_FEW_ARGUMENTS;
  } else if (argc == 1) {
    power_ctl.me17_main_state = ON;
    power_ctl.me17_state = ON;
    power_ctl.me14_state = ON;
    power_ctl.me18_state = ON;
    WsfMsgSend(hanlderId, pMsg);
  } else {
    return TERMINAL_ERROR_TOO_MANY_ARGUMENTS;
  }

  return TERMINAL_ERROR_OK;
}
static uint8_t cmd_allOff(uint32_t argc, char **argv) {
  dmEvt_t *pMsg;
  pMsg = WsfMsgAlloc(sizeof(attEvt_t));
  pMsg->hdr.event = DM_VENDOR_SPEC_IND;

  if (argc < 1) {
    return TERMINAL_ERROR_TOO_FEW_ARGUMENTS;
  } else if (argc == 1) {
    power_ctl.me17_main_state = OFF;
    power_ctl.me17_state = OFF;
    power_ctl.me14_state = OFF;
    power_ctl.me18_state = OFF;
    WsfMsgSend(hanlderId, pMsg);
  } else {
    return TERMINAL_ERROR_TOO_MANY_ARGUMENTS;
  }

  return TERMINAL_ERROR_OK;
}

void register_at_Commands(void) {
  uint8_t index = 0;
  while (appTerminalCustomCommandList[index].pName != NULL) {
    TerminalRegisterCommand(&appTerminalCustomCommandList[index]);
    index++;
  }
}
void setHandlerID(uint8_t id) { hanlderId = id; }