#ifndef _BLE_RIG_H_
#define _BLE_RIG_H_

#include <stdint.h>
#include <stddef.h>

uint32_t crc32_for_byte(uint32_t r);
void crc32(const void *data, size_t n_bytes, uint32_t *crc);

#endif