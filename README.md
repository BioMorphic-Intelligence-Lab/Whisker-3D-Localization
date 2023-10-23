# Whisker-3D-Localization

# Table of contents
1. [Overview](#overview)
2. [PCB design](#design)
3. [Data reading](#reading)
4. [3D-Localization](#3D-Localization)
   1. [Installation](#Installation)
   2. [Dataset](#Dataset)
   3. [Model training](#training) 
   4. [Test](#Test) 

## Overview <a name="overview"></a>
**This repository provides open-source files of the paper:**

![]()

<b>A Biomorphic Whisker Sensor for Aerial Tactile Applications</b>, Chaoxiang Ye, Guido de Croon, and Salua Hamaza. <br>
2024 IEEE International Conference on Robotics and Automation (ICRA 2024), Under Review. <br>

## PCB design <a name="design"></a>
Including KiCAD files and the manufacturer's files. The manufacturer's files encompass the gerber file, Bill of Materials (BOM), and position file. The primary electronic components consist of barometers and microcontrollers. To optimize sensing ability and PCB size, we recommend utilizing the BMP390 along with the STM32F070F6. In the event of a microcontroller substitution, we recommend choosing for one with a minimum of 32Kbytes flash memory.
## Data reading <a name="reading"></a>
Including all programs utilizing the STM32 to read data from three BMP390s. The SPI bus is employed for communication between the STM32 and the BMP390, where the chip select pins are sequentially lowered to read sensor data in sequence. Additionally, a UART is utilized for communication between the STM32 and the PC.

We use the In-system programming (ISP) to download the program into the STM32. Initially, the BOOT0 pin necessitates a pull-up, which entails soldering an additional wire on the PCB, connecting BOOT0 to any of the leads linked to the 3.3V (PWR-layer). Subsequently, employ the MCU ISP software to flash the "whiskeropt2.0.hex" file from the Data Reading folder onto the STM32, ensuring the baud rate is set to 115200.
## 3D-Localization <a name="3D-Localization"></a>
Coming soon
### Installation <a name="Installation"></a>

### Dataset <a name="Dataset"></a>

### Model training <a name="training"></a>

### Test <a name="Test"></a>
