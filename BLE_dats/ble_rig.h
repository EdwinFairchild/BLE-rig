#ifndef _BLE_RIG_H_
#define _BLE_RIG_H_

#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include "mxc_device.h"
#include "nvic_table.h"
#include "pb.h"
#include "board.h"
#include "gpio.h"
#include "wsf_trace.h"
#include "util/terminal.h"
#include "app_ui.h"
#include "util/print.h"
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
#endif