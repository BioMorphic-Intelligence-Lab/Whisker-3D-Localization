#include "BMP390.h"
unsigned char rx_data[32]={1};
unsigned char tx_data[32]={1};



void write8(unsigned char addr,uint8_t data,uint16_t GPIO_Pin)
{
	tx_data[0] = addr;
	tx_data[1] = data;
	HAL_GPIO_WritePin(SPI_CS1_GPIO_Port, GPIO_Pin, GPIO_PIN_RESET);
	HAL_SPI_TransmitReceive(&hspi1, tx_data, rx_data, 2, 0x10);
	HAL_GPIO_WritePin(SPI_CS1_GPIO_Port, GPIO_Pin, GPIO_PIN_SET);
}

uint8_t read8(unsigned char reg,uint16_t GPIO_Pin)
{
  int8_t value;
	tx_data[0] = reg | 0b10000000;
	HAL_GPIO_WritePin(SPI_CS1_GPIO_Port, GPIO_Pin, GPIO_PIN_RESET);
	HAL_SPI_TransmitReceive(&hspi1, tx_data, rx_data, 3, 0x10);
	HAL_GPIO_WritePin(SPI_CS1_GPIO_Port, GPIO_Pin, GPIO_PIN_SET);
	value = rx_data[2];
  return value;

}
uint16_t read16(unsigned char reg,uint16_t GPIO_Pin)
{
  uint16_t value;
	tx_data[0] = reg | 0b10000000;
	HAL_GPIO_WritePin(SPI_CS1_GPIO_Port, GPIO_Pin, GPIO_PIN_RESET);
	HAL_SPI_TransmitReceive(&hspi1, tx_data, rx_data, 4, 0x10);
	HAL_GPIO_WritePin(SPI_CS1_GPIO_Port, GPIO_Pin, GPIO_PIN_SET);
	value = (rx_data[3]<<8) + rx_data[2];
  return value;
}

uint32_t read32(unsigned char reg,uint16_t GPIO_Pin)
{
  uint32_t value;
	tx_data[0] = reg | 0b10000000;
	HAL_GPIO_WritePin(SPI_CS1_GPIO_Port, GPIO_Pin, GPIO_PIN_RESET);
	HAL_SPI_TransmitReceive(&hspi1, tx_data, rx_data, 5, 0x10);
	HAL_GPIO_WritePin(SPI_CS1_GPIO_Port, GPIO_Pin, GPIO_PIN_SET);
	value = (rx_data[4]<<16) + (rx_data[3]<<8) + rx_data[2];
  return value;
}


uint8_t BMP390_Init(uint16_t GPIO_Pin)
{
	uint8_t BMP390_ID;
	write8(CMD_Addr,0x36,GPIO_Pin);//RESET
	BMP390_ID = read8(CHIP_ID_Addr,GPIO_Pin);//Read the CHIP_ID-0x60
	write8(PWR_CTRL_Addr,0x33,GPIO_Pin);//Set Working mode and state of sensor（P:E, T:E，normal mode）
	write8(IF_CONF_Addr,0x00,GPIO_Pin);//Serial interface settings
	write8(OSR_Addr,0x00,GPIO_Pin);//Set the PM-RATE and PM-PRC,Set the TMPI-RATE and TMP-PRC P:16,T:16
	write8(ODR_Addr,0x00,GPIO_Pin);//Set the configuration of the output data rates by means of setting the subdivision/subsampling.（200HZ） 50HZ
	write8(CONFIG_Addr,0x00,GPIO_Pin);//IIR filter coeffcients（IIR0）
	return BMP390_ID;
}



void Parameter_Reading(int *Pressure_Para,int *Temperature_Para)
{

	//Temperature coefficients
	Temperature_Para[0] = read16(BMP390_REGISTER_DIG_T1,SPI_CS1_Pin);//T1
	Temperature_Para[1] = read16(BMP390_REGISTER_DIG_T2,SPI_CS1_Pin);//T2
	Temperature_Para[2] = read8(BMP390_REGISTER_DIG_T3,SPI_CS1_Pin);//T3
	//if(Temperature_Para[2]&0x80) Temperature_Para[2] = Temperature_Para[2]-Total_Number_8;
	//Pressure coefficients
	//Coefficient P1
	Pressure_Para[0] = read16(BMP390_REGISTER_DIG_P1,SPI_CS1_Pin);//P1
	//if(Pressure_Para[0]&0x8000) Pressure_Para[0] = Pressure_Para[0] - Total_Number_16;//P1
	//Coefficient P2
	Pressure_Para[1] = read16(BMP390_REGISTER_DIG_P2,SPI_CS1_Pin);//P2
	//if(Pressure_Para[1]&0x8000) Pressure_Para[1] = Pressure_Para[1] - Total_Number_16;//P2
	//Coefficient P3
	Pressure_Para[2] = read8(BMP390_REGISTER_DIG_P3,SPI_CS1_Pin);//P3
	//if(Pressure_Para[2]&0x80) Pressure_Para[2] = Pressure_Para[2] - Total_Number_8;//P3
	//Coefficient P4
	Pressure_Para[3] = read8(BMP390_REGISTER_DIG_P4,SPI_CS1_Pin);//P4
	//if(Pressure_Para[3]&0x80) Pressure_Para[3] = Pressure_Para[3] - Total_Number_8;//P4
	//Coefficient P5
	Pressure_Para[4] = read16(BMP390_REGISTER_DIG_P5,SPI_CS1_Pin);//P5
	//Coefficient P6
	Pressure_Para[5] = read16(BMP390_REGISTER_DIG_P6,SPI_CS1_Pin);//P6
	//Coefficient P7
	Pressure_Para[6] = read8(BMP390_REGISTER_DIG_P7,SPI_CS1_Pin);//P7
	//if(Pressure_Para[6]&0x80) Pressure_Para[6] = Pressure_Para[6] - Total_Number_8;//P7
	//Coefficient P8
	Pressure_Para[7] = read8(BMP390_REGISTER_DIG_P8,SPI_CS1_Pin);//P8
	//if(Pressure_Para[7]&0x80) Pressure_Para[7] = Pressure_Para[7] - Total_Number_8;//P8
	//Coefficient P9
	Pressure_Para[8] = read16(BMP390_REGISTER_DIG_P9,SPI_CS1_Pin);//P9
	//if(Pressure_Para[8]&0x8000) Pressure_Para[8] = Pressure_Para[8] - Total_Number_16;//P9
	//Coefficient P10
	Pressure_Para[9] = read8(BMP390_REGISTER_DIG_P10,SPI_CS1_Pin);//P10
	//if(Pressure_Para[9]&0x80) Pressure_Para[9] = Pressure_Para[9] - Total_Number_8;//P10
	//Coefficient P11
	Pressure_Para[10] = read8(BMP390_REGISTER_DIG_P11,SPI_CS1_Pin);//P11
	//if(Pressure_Para[10]&0x80) Pressure_Para[10] = Pressure_Para[10] - Total_Number_8;//P11
}
double Correcting_Pressure(uint32_t Pressure,int *Pressure_Para,double Corr_Temperature)
{
	  double PAR_P1,PAR_P2,PAR_P3,PAR_P4,PAR_P5;
	  double PAR_P6,PAR_P7,PAR_P8,PAR_P9,PAR_P10,PAR_P11;
	  double Corr_Pressure,partial_data1,partial_data2,partial_data3,partial_data4;
	  double partial_out1,partial_out2;
	  PAR_P1 = (Pressure_Para[0]-Total_Number_14)/Total_Number_20;
	  PAR_P2 = (Pressure_Para[1]-Total_Number_14)/Total_Number_29;
	  PAR_P3 = Pressure_Para[2]/Total_Number_32;
	  PAR_P4 = Pressure_Para[3]/Total_Number_32/Total_Number_5;
	  PAR_P5 = Pressure_Para[4]/Total_Number_Neg_3;
	  PAR_P6 = Pressure_Para[5]/Total_Number_6;
	  PAR_P7 = Pressure_Para[6]/Total_Number_8;
	  PAR_P8 = Pressure_Para[7]/Total_Number_15;
	  PAR_P9 =  Pressure_Para[8]/Total_Number_32/Total_Number_16;
	  PAR_P10 =  Pressure_Para[9]/Total_Number_32/Total_Number_16;
	  PAR_P11 =  Pressure_Para[10]/Total_Number_32/Total_Number_32/Total_Number_1;
	  //Calculation
	  partial_data1 = PAR_P6*Corr_Temperature;
	  partial_data2 = PAR_P7*Corr_Temperature*Corr_Temperature;
	  partial_data3 = PAR_P8*Corr_Temperature*Corr_Temperature*Corr_Temperature;
	  partial_out1 = PAR_P5+partial_data1+partial_data2+partial_data3;

	  partial_data1 = PAR_P2*Corr_Temperature;
	  partial_data2 = PAR_P3*Corr_Temperature*Corr_Temperature;
	  partial_data3 = PAR_P4*Corr_Temperature*Corr_Temperature*Corr_Temperature;
	  partial_out2 = (double)(Pressure)*(PAR_P1+partial_data1+partial_data2+partial_data3);

	  partial_data1 = (double)(Pressure)*(double)(Pressure);
	  partial_data2 = PAR_P9+PAR_P10*Corr_Temperature;
	  partial_data3 = partial_data1*partial_data2;
	  partial_data4 = partial_data3+(double)(Pressure)*(double)(Pressure)*(double)(Pressure)*PAR_P11;
	  Corr_Pressure = partial_out1+partial_out2+partial_data4;
	  return Corr_Pressure;
}

double Correcting_Temperature(uint32_t Temperature,int *Temperature_Para)
{
	double Corr_Temperature,PAR_T1,PAR_T2,PAR_T3;
	double	partial_data1,parital_data2;


	PAR_T1 = Temperature_Para[0]/Total_Number_Neg_8;
	PAR_T2 = Temperature_Para[1]/Total_Number_30;
	PAR_T3 = Temperature_Para[2]/Total_Number_32/Total_Number_16;
	//Calculation
	partial_data1 = (double)(Temperature)-PAR_T1;
	parital_data2 = partial_data1*PAR_T2;
	Corr_Temperature = parital_data2+partial_data1*partial_data1*PAR_T3;
	return Corr_Temperature;
}

unsigned char printf_temp[64];
void Uart1_printf(const char *format,...)
{
	unsigned short len;

	va_list args;
	va_start(args, format);
	len = vsnprintf((char*)printf_temp, sizeof(printf_temp)+1, (char*)format,args);
	va_end(args);

	HAL_UART_Transmit(&huart1, printf_temp, len, 0xFFFF);
}
