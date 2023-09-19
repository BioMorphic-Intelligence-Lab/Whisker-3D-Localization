#ifndef __BMP390_H
#define __BMP390_H
#include "math.h"
#include "main.h"
#include <stdarg.h>
#include "stdio.h"
#include "stm32f0xx_hal.h"
#define CHIP_ID_Addr 0x80
#define REV_ID_Addr 0x01

#define BMP390_REGISTER_PRESSUREDATA 0x04

#define BMP390_REGISTER_TEMPDATA 0x07

#define IF_CONF_Addr 0x1A
#define PWR_CTRL_Addr 0x1B
#define OSR_Addr 0x1C
#define ODR_Addr 0x1D
#define CONFIG_Addr 0x1F
#define CMD_Addr 0x7E

#define BMP390_REGISTER_DIG_T1  0x31
#define BMP390_REGISTER_DIG_T2  0x33
#define BMP390_REGISTER_DIG_T3  0x35
#define BMP390_REGISTER_DIG_P1  0x36
#define BMP390_REGISTER_DIG_P2  0x38
#define BMP390_REGISTER_DIG_P3  0x3A
#define BMP390_REGISTER_DIG_P4  0x3B
#define BMP390_REGISTER_DIG_P5  0x3C
#define BMP390_REGISTER_DIG_P6  0x3E
#define BMP390_REGISTER_DIG_P7  0x40
#define BMP390_REGISTER_DIG_P8  0x41
#define BMP390_REGISTER_DIG_P9  0x42
#define BMP390_REGISTER_DIG_P10  0x44
#define BMP390_REGISTER_DIG_P11  0x45



#define Total_Number_32 4294967296.0
#define Total_Number_30 1073741824.0
#define Total_Number_29 536870912.0
#define Total_Number_24 16777216.0
#define Total_Number_20 1048576.0
#define Total_Number_16 65536.0
#define Total_Number_15 32768.0
#define Total_Number_14 16384.0
#define Total_Number_12 4096.0
#define Total_Number_8 256.0
#define Total_Number_6 64.0
#define Total_Number_5 32.0
#define Total_Number_1 2.0

#define Total_Number_Neg_8 0.00390625
#define Total_Number_Neg_3 0.125



uint8_t BMP390_Init(uint16_t GPIO_Pin);
uint8_t read8(unsigned char reg,uint16_t GPIO_Pin);
uint16_t read16(unsigned char reg,uint16_t GPIO_Pin);
uint32_t read32(unsigned char reg,uint16_t GPIO_Pin);
void write8(uint8_t addr,uint8_t data,uint16_t GPIO_Pin);
void Parameter_Reading(int *Pressure_Para,int *Temperature_Para);
double Correcting_Temperature(uint32_t Temperature,int *Temperature_Para);
double Correcting_Pressure(uint32_t Pressure,int *Pressure_Para,double Corr_Temperature);



#endif
