/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2023 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "spi.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */
extern void Uart1_printf(const char *format,...);



/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */
  uint8_t BMP390_ID1,BMP390_ID2,BMP390_ID3,r1,r2;
  int Pressure_Para[11],Temperature_Para[3];
  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_SPI1_Init();
  MX_USART1_UART_Init();
  /* USER CODE BEGIN 2 */
  HAL_Delay(10000);
  HAL_GPIO_WritePin(SPI_CS1_GPIO_Port, SPI_CS1_Pin, GPIO_PIN_SET);
  HAL_GPIO_WritePin(SPI_CS2_GPIO_Port, SPI_CS2_Pin, GPIO_PIN_SET);
  HAL_GPIO_WritePin(SPI_CS3_GPIO_Port, SPI_CS3_Pin, GPIO_PIN_SET);

  BMP390_ID1 = BMP390_Init(SPI_CS1_Pin);
  BMP390_ID2 = BMP390_Init(SPI_CS2_Pin);
  BMP390_ID3 = BMP390_Init(SPI_CS3_Pin);
  r1 = read8(PWR_CTRL_Addr,SPI_CS1_Pin);
  r2 = read8(CMD_Addr,SPI_CS1_Pin);
  Parameter_Reading(Pressure_Para,Temperature_Para);
  Uart1_printf("chipid1= 0x%x,chipid2= 0x%x,chipid3= 0x%x,r1= 0x%x,r2= 0x%x\r\n",BMP390_ID1,BMP390_ID2,BMP390_ID3,r1,r2);


  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
	  uint32_t Pressure1 = 0,Pressure2 = 1,Pressure3 = 2;
	  uint32_t Temperature1 = 0,Temperature2 = 1,Temperature3 = 2;
//	  uint32_t Pressure1 = 0;
//	  uint32_t Temperature1 = 0;
	  double Correcting_Temp1,Correcting_Press1,Correcting_Temp2,Correcting_Press2,Correcting_Temp3,Correcting_Press3;
//	  double Correcting_Temp1,Correcting_Press1;
	  Pressure1 = read32(BMP390_REGISTER_PRESSUREDATA,SPI_CS1_Pin);
	  Temperature1 = read32(BMP390_REGISTER_TEMPDATA,SPI_CS1_Pin);
	  Pressure2 = read32(BMP390_REGISTER_PRESSUREDATA,SPI_CS2_Pin);
	  Temperature2 = read32(BMP390_REGISTER_TEMPDATA,SPI_CS2_Pin);
	  Pressure3 = read32(BMP390_REGISTER_PRESSUREDATA,SPI_CS3_Pin);
	  Temperature3 = read32(BMP390_REGISTER_TEMPDATA,SPI_CS3_Pin);
//	  Uart1_printf("T1: %d; P1: %d\r\n",Temperature1, Pressure1);
//	  Uart1_printf("T2: %d; P2: %d\r\n",Temperature2, Pressure2);
//	  Uart1_printf("T3: %d; P3: %d\r\n",Temperature3, Pressure3);

	  Correcting_Temp1 = Correcting_Temperature(Temperature1,Temperature_Para);
	  Correcting_Press1 = Correcting_Pressure(Pressure1,Pressure_Para,Correcting_Temp1);
	  Correcting_Temp2 = Correcting_Temperature(Temperature2,Temperature_Para);
	  Correcting_Press2 = Correcting_Pressure(Pressure2,Pressure_Para,Correcting_Temp2);
	  Correcting_Temp3 = Correcting_Temperature(Temperature3,Temperature_Para);
	  Correcting_Press3 = Correcting_Pressure(Pressure3,Pressure_Para,Correcting_Temp3);
//	  Uart1_printf("{T:%d,%d,%d\n}",Temperature1,Temperature2,Temperature3);
//	  Uart1_printf("{T_C:%f,%f,%f\n}",Correcting_Temp1,Correcting_Temp2,Correcting_Temp3);
//	  Uart1_printf("{P:%d,%d,%d\n}",Pressure1,Pressure2,Pressure3);
	  Uart1_printf("{P_C:%f,%f,%f\n}",Correcting_Press1,Correcting_Press2,Correcting_Press3);

	  /* TEST UART*/
	  //HAL_UART_Transmit(&huart1,(uint8_t*) "10",2,0xFFFF);

	  /*

	  tx_data[0] = 0x80;
	  HAL_GPIO_WritePin(SPI_CS1_GPIO_Port, SPI_CS1_Pin, GPIO_PIN_RESET);
	  HAL_SPI_TransmitReceive(&hspi1, tx_data, rx_data, 3, 0xFFFF);
	  HAL_GPIO_WritePin(SPI_CS1_GPIO_Port, SPI_CS1_Pin, GPIO_PIN_SET);
	  P = readPressure();
	  Uart1_printf("chipid= 0x%x; P: %.2f\r\n",rx_data[2], P);
	  HAL_Delay(100);

	  HAL_GPIO_WritePin(SPI_CS2_GPIO_Port, SPI_CS2_Pin, GPIO_PIN_RESET);
	  HAL_SPI_TransmitReceive(&hspi1, tx_data, rx_data, 3, 0xFFFF);
	  HAL_GPIO_WritePin(SPI_CS2_GPIO_Port, SPI_CS2_Pin, GPIO_PIN_SET);
	  //Uart1_printf("SPI communication error: %s\r\n", Status);
	  P = readPressure();
	  Uart1_printf("chipid= 0x%x; P: %.2f\r\n",rx_data[2], P);
	  HAL_Delay(100);

	  HAL_GPIO_WritePin(SPI_CS3_GPIO_Port, SPI_CS3_Pin, GPIO_PIN_RESET);
	  HAL_SPI_TransmitReceive(&hspi1, tx_data, rx_data, 3, 0xFFFF);
	  HAL_GPIO_WritePin(SPI_CS3_GPIO_Port, SPI_CS3_Pin, GPIO_PIN_SET);
	  P = readPressure();
	  Uart1_printf("chipid= 0x%x; P: %.2f\r\n",rx_data[2], P);
	  HAL_Delay(1000);
	  */


	  //Uart1_printf("spi: 0x%x\r\n",0x58);
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */

		//T = readTemperature();
		//P = readPressure();
		//Uart1_printf("T = %.2f; P = %.2f\r\n",T,P);
		//HAL_Delay(100);
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL2;
  RCC_OscInitStruct.PLL.PREDIV = RCC_PREDIV_DIV1;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_USART1;
  PeriphClkInit.Usart1ClockSelection = RCC_USART1CLKSOURCE_PCLK1;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */


/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
