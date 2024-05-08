# Whisker-3D-Localization

# Table of contents
1. [Overview](#overview)
2. [PCB design](#design)
3. [Data reading](#reading)
4. [3D-Localization](#3D-Localization)
   1. [Architecture](#Architecture)
   2. [Installation](#Installation)
   3. [Dataset](#Dataset)
   4. [Model training](#training) 
   5. [Test](#Test)
5. [Contact](#Contact)

## Overview <a name="overview"></a>
**This repository contains open-source files for paper:**
<p align="center">
  <img src="https://raw.githubusercontent.com/BioMorphic-Intelligence-Lab/Whisker-3D-Localization/master/images/overview-git.png" width="95%" />
</p>

<b>A Biomorphic Whisker Sensor for Aerial Tactile Applications</b>, Chaoxiang Ye, Guido de Croon, and Salua Hamaza. <br>
2024 IEEE International Conference on Robotics and Automation (ICRA 2024). <br>

## PCB design <a name="design"></a>
<p align="center">
  <img src="https://raw.githubusercontent.com/BioMorphic-Intelligence-Lab/Whisker-3D-Localization/master/images/PCB-git.png" width="60%" />
</p>

Including KiCAD files and the manufacturer's files. The manufacturer's files encompass the gerber file, Bill of Materials (BOM), and position file. The primary electronic components consist of barometers and microcontrollers. To optimize sensing ability and PCB size, we recommend utilizing the BMP390 along with the STM32F070F6. In the event of a microcontroller substitution, we recommend choosing for one with a minimum of 32Kbytes flash memory.
## Data reading <a name="reading"></a>
<p align="center">
  <img src="https://raw.githubusercontent.com/BioMorphic-Intelligence-Lab/Whisker-3D-Localization/master/images/system-git.png" width="90%" />
</p>

Including all programs utilizing the STM32 to read data from three BMP390s. The SPI bus is employed for communication between the STM32 and the BMP390, where the chip select pins are sequentially lowered to read sensor data in sequence. Additionally, a UART is utilized for communication between the STM32 and the PC.

We use the In-system programming (ISP) to download the program into the STM32. Initially, the BOOT0 pin necessitates a pull-up, which entails soldering an additional wire on the PCB, connecting BOOT0 to any of the leads linked to the 3.3V (PWR-layer). Subsequently, employ the MCU ISP software to flash the "whiskeropt2.0.hex" file from the Data Reading folder onto the STM32, ensuring the baud rate is set to 115200. Please be aware that when reading data, it is imperative to configure the baud rate in accordance with the parameter specified in the "usart.c" file. In this instance, we have set it to 230400.
## 3D-Localization <a name="3D-Localization"></a>
### Architecture <a name="Architecture"></a>
<p align="center">
  <img src="https://raw.githubusercontent.com/BioMorphic-Intelligence-Lab/Whisker-3D-Localization/master/images/architecture-git.png" width="90%" />
</p>

### Installation <a name="Installation"></a>
We implemented this code, under the following packages:
* Python 3.8.17
* Pytorch 2.0.1
* Numpy 1.24.3
* Scikit-learn 1.2.2

Scikit-learn is exclusively utilized for selecting hyperparameters in the grid search process.


### Dataset <a name="Dataset"></a>
The dataset was split into training, validation, and test sets. The training set contains 6,068,046 frames, while both the validation and test sets have 1,504,834 frames each. The validation set is solely employed for hyperparameter selection. We show the training dataset as an example:
<p align="center">
  <img src="https://raw.githubusercontent.com/BioMorphic-Intelligence-Lab/Whisker-3D-Localization/master/images/trainingset.png" width="90%" />
</p>

### Model training <a name="training"></a>
The training set was randomly shuffled in each epoch. All models were using the Adam optimizer.
Below, we provide our optimal hyperparameters determined through the grid search method:
<p align="center">
  <img src="https://raw.githubusercontent.com/BioMorphic-Intelligence-Lab/Whisker-3D-Localization/master/images/hyper-parameter.png" width="80%" />
</p>

### Test <a name="Test"></a>

## Contact <a name="Contact"></a>
If you have any questions, feel free to contact us through email (C.Ye@tudelft.nl). Enjoy!
