#ifndef _BLE_RIG_H_
#define _BLE_RIG_H_

#include "board.h"
#include "gpio.h"
#include "mxc_device.h"
#include "nvic_table.h"
#include "pb.h"
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "FreeRTOS.h"
#include "FreeRTOSConfig.h"
#include "FreeRTOS_CLI.h"
#include "app_api.h"
#include "app_db.h"
#include "app_main.h"
#include "app_ui.h"
#include "att_api.h"
#include "board.h"
#include "dats_api.h"
#include "dm_api.h"
#include "gatt/gatt_api.h"
#include "hci_api.h"
#include "led.h"
#include "lp.h"
#include "mxc_device.h"
#include "pal_btn.h"
#include "pal_uart.h"
#include "portmacro.h"
#include "queue.h"
#include "sec_api.h"
#include "semphr.h"
#include "smp_api.h"
#include "svc_ch.h"
#include "svc_core.h"
#include "svc_sds.h"
#include "svc_wp.h"
#include "task.h"
#include "tmr.h"
#include "trimsir_regs.h"
#include "uart.h"
#include "util/bstream.h"
#include "util/calc128.h"
#include "wsf_buf.h"
#include "wsf_msg.h"
#include "wsf_nvm.h"
#include "wsf_timer.h"
#include "wsf_trace.h"
#include "wsf_types.h"
#include "wut.h"
#include <string.h>

typedef enum __attribute__((__packed__)) {
  POWER_OPTIONS,
  RESERVED

} packet_t;

typedef enum __attribute__((__packed__)) { OFF, ON } power_state_t;

typedef struct __attribute__((__packed__)) {
  uint32_t crc32;
  packet_t packet_type;
  power_state_t me14_state;
  power_state_t me17_state;
  power_state_t me17_main_state;
  power_state_t me18_state;

} powerOptions_t;

uint32_t crc32_for_byte(uint32_t r);
void crc32(const void *data, size_t n_bytes, uint32_t *crc);
void config_gpio(void);
void vTask1(void *pvParameters);
uint8_t datsWpWriteCback(dmConnId_t connId, uint16_t handle, uint8_t operation,
                         uint16_t offset, uint16_t len, uint8_t *pValue,
                         attsAttr_t *pAttr);
void freeRTOS_init(void);
#endif