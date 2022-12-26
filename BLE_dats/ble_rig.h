#ifndef _BLE_RIG_H_
#define _BLE_RIG_H_

#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include "mxc_device.h"
#include "nvic_table.h"
#include "pb.h"
#include "board.h"
#include "gpio.h"


uint32_t crc32_for_byte(uint32_t r);
void crc32(const void *data, size_t n_bytes, uint32_t *crc);
void config_gpio(void);
#endif