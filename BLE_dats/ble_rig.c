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

/*! \brief    Custom Command Handler. */
static uint8_t appNameCommandHandler(uint32_t argc, char **argv);


/*! \brief    command list */
terminalCommand_t appTerminalCustomCommandList[] = {

    { NULL, "name", "name <First> <Last>", appNameCommandHandler },
    { NULL, NULL, NULL, NULL }, // used as delimter for end of list

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
uint32_t crc32_for_byte(uint32_t r)
{
    for (int j = 0; j < 8; ++j) r = (r & 1 ? 0 : (uint32_t)0xEDB88320L) ^ r >> 1;
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
static uint32_t table[0x100] = { 0 };
void crc32(const void *data, size_t n_bytes, uint32_t *crc)
{
    if (!*table) {
        for (size_t i = 0; i < 0x100; ++i) table[i] = crc32_for_byte(i);
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
static uint8_t appNameCommandHandler(uint32_t argc, char **argv)
{
    if (argc < 3) {
        return TERMINAL_ERROR_TOO_FEW_ARGUMENTS;
    } else if (argc == 3) {
        TerminalTxPrint("Hello %s %s\r\n", argv[1], argv[2]);

    } else {
        return TERMINAL_ERROR_TOO_MANY_ARGUMENTS;
    }

    return TERMINAL_ERROR_OK;
}
void register_at_Commands(void)
{
    uint8_t index = 0;
    while (appTerminalCustomCommandList[index].pName != NULL) {
        TerminalRegisterCommand(&appTerminalCustomCommandList[index]);
        index++;
    }
}