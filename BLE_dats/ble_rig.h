#ifndef _BLE_RIG_H_
#define _BLE_RIG_H_

#include "app_ui.h"
#include "att_api.h"
#include "board.h"
#include "dm_api.h"
#include "gpio.h"
#include "mxc_device.h"
#include "nvic_table.h"
#include "pb.h"
#include "util/print.h"
#include "util/terminal.h"
#include "wsf_msg.h"
#include "wsf_trace.h"
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef enum __attribute__((__packed__)) {
  POWER_OPTIONS,
  RESERVED

} packet_t;

typedef enum __attribute__((__packed__)) { OFF, ON } power_state_t;

typedef struct __attribute__((__packed__)) {
  // uint32_t crc32;
  packet_t packet_type;
  power_state_t me14_state;
  power_state_t me17_state;
  power_state_t me17_main_state;
  power_state_t me18_state;
  bool all_on;
  bool all_off;

} powerOptions_t;

uint32_t crc32_for_byte(uint32_t r);
void crc32(const void *data, size_t n_bytes, uint32_t *crc);
void config_gpio(void);
void parsePacket(void);
void setHandlerID(uint8_t id);
#endif