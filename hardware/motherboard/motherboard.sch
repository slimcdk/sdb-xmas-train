EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date "15 nov 2012"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L power:+5V #PWR01
U 1 1 580C1B61
P 3100 950
F 0 "#PWR01" H 3100 800 50  0001 C CNN
F 1 "+5V" H 3100 1090 50  0000 C CNN
F 2 "" H 3100 950 50  0000 C CNN
F 3 "" H 3100 950 50  0000 C CNN
	1    3100 950 
	1    0    0    -1  
$EndComp
Wire Wire Line
	3100 950  3100 1100
Wire Wire Line
	3100 1100 2900 1100
Wire Wire Line
	3100 1200 2900 1200
Connection ~ 3100 1100
$Comp
L power:GND #PWR02
U 1 1 580C1D11
P 3000 3150
F 0 "#PWR02" H 3000 2900 50  0001 C CNN
F 1 "GND" H 3000 3000 50  0000 C CNN
F 2 "" H 3000 3150 50  0000 C CNN
F 3 "" H 3000 3150 50  0000 C CNN
	1    3000 3150
	1    0    0    -1  
$EndComp
Wire Wire Line
	3000 1300 3000 1700
Wire Wire Line
	3000 2700 2900 2700
Wire Wire Line
	3000 2500 2900 2500
Connection ~ 3000 2700
Wire Wire Line
	3000 2000 2900 2000
Connection ~ 3000 2500
Wire Wire Line
	3000 1700 2900 1700
Connection ~ 3000 2000
$Comp
L power:GND #PWR03
U 1 1 580C1E01
P 2300 3150
F 0 "#PWR03" H 2300 2900 50  0001 C CNN
F 1 "GND" H 2300 3000 50  0000 C CNN
F 2 "" H 2300 3150 50  0000 C CNN
F 3 "" H 2300 3150 50  0000 C CNN
	1    2300 3150
	1    0    0    -1  
$EndComp
Wire Wire Line
	2300 3000 2400 3000
Wire Wire Line
	2300 1500 2300 2300
Wire Wire Line
	2300 2300 2400 2300
Connection ~ 2300 3000
Connection ~ 2200 1100
Wire Wire Line
	2200 1900 2400 1900
Wire Wire Line
	2200 1100 2400 1100
Wire Wire Line
	2200 950  2200 1100
$Comp
L power:+3.3V #PWR04
U 1 1 580C1BC1
P 2200 950
F 0 "#PWR04" H 2200 800 50  0001 C CNN
F 1 "+3.3V" H 2200 1090 50  0000 C CNN
F 2 "" H 2200 950 50  0000 C CNN
F 3 "" H 2200 950 50  0000 C CNN
	1    2200 950 
	1    0    0    -1  
$EndComp
Wire Wire Line
	2300 1500 2400 1500
Connection ~ 2300 2300
Wire Wire Line
	2400 1200 1250 1200
Wire Wire Line
	1250 1300 2400 1300
Wire Wire Line
	1250 1400 2400 1400
Wire Wire Line
	2400 1600 1250 1600
Wire Wire Line
	1250 1700 2400 1700
Wire Wire Line
	1250 1800 2400 1800
Wire Wire Line
	2400 2000 1250 2000
Wire Wire Line
	1250 2100 2400 2100
Wire Wire Line
	1250 2200 2400 2200
Wire Wire Line
	2400 2400 1250 2400
Wire Wire Line
	1250 2500 2400 2500
Wire Wire Line
	1250 2600 2400 2600
Wire Wire Line
	2400 2700 1250 2700
Wire Wire Line
	1250 2800 2400 2800
Wire Wire Line
	1250 2900 2400 2900
Wire Wire Line
	2900 2800 3950 2800
Wire Wire Line
	2900 2900 3950 2900
Wire Wire Line
	2900 2300 3950 2300
Wire Wire Line
	2900 2400 3950 2400
Wire Wire Line
	2900 2100 3950 2100
Wire Wire Line
	2900 2200 3950 2200
Wire Wire Line
	2900 1800 3950 1800
Wire Wire Line
	2900 1900 3950 1900
Wire Wire Line
	2900 1500 3950 1500
Wire Wire Line
	2900 1600 3950 1600
Wire Wire Line
	2900 1400 3950 1400
Wire Wire Line
	2900 2600 3950 2600
Text Label 1250 1200 0    50   ~ 0
GPIO2(SDA1)
Text Label 1250 1300 0    50   ~ 0
GPIO3(SCL1)
Text Label 1250 1400 0    50   ~ 0
GPIO4(GCLK)
Text Label 1250 1600 0    50   ~ 0
GPIO17(GEN0)
Text Label 1250 1700 0    50   ~ 0
GPIO27(GEN2)
Text Label 1250 1800 0    50   ~ 0
GPIO22(GEN3)
Text Label 1250 2000 0    50   ~ 0
GPIO10(SPI0_MOSI)
Text Label 1250 2100 0    50   ~ 0
GPIO9(SPI0_MISO)
Text Label 1250 2200 0    50   ~ 0
GPIO11(SPI0_SCK)
Text Label 1250 2400 0    50   ~ 0
ID_SD
Text Label 1250 2500 0    50   ~ 0
GPIO5
Text Label 1250 2600 0    50   ~ 0
GPIO6
Text Label 1250 2700 0    50   ~ 0
GPIO13(PWM1)
Text Label 1250 2800 0    50   ~ 0
GPIO19(SPI1_MISO)
Text Label 1250 2900 0    50   ~ 0
GPIO26
Text Label 3950 2900 2    50   ~ 0
GPIO20(SPI1_MOSI)
Text Label 3950 2800 2    50   ~ 0
GPIO16
Text Label 3950 2600 2    50   ~ 0
GPIO12(PWM0)
Text Label 3950 2400 2    50   ~ 0
ID_SC
Text Label 3950 2300 2    50   ~ 0
GPIO7(SPI1_CE_N)
Text Label 3950 2200 2    50   ~ 0
GPIO8(SPI0_CE_N)
Text Label 3950 2100 2    50   ~ 0
GPIO25(GEN6)
Text Label 3950 1900 2    50   ~ 0
GPIO24(GEN5)
Text Label 3950 1800 2    50   ~ 0
GPIO23(GEN4)
Text Label 3950 1600 2    50   ~ 0
GPIO18(GEN1)(PWM0)
Text Label 3950 1500 2    50   ~ 0
GPIO15(RXD0)
Text Label 3950 1400 2    50   ~ 0
GPIO14(TXD0)
Wire Wire Line
	3000 1300 2900 1300
Connection ~ 3000 1700
Text Notes 700  7600 0    50   ~ 0
ID_SD and ID_SC PINS:\nThese pins are reserved for HAT ID EEPROM.\n\nAt boot time this I2C interface will be\ninterrogated to look for an EEPROM\nthat identifes the attached board and\nallows automagic setup of the GPIOs\n(and optionally, Linux drivers).\n\nDO NOT USE these pins for anything other\nthan attaching an I2C ID EEPROM. Leave\nunconnected if ID EEPROM not required.
$Comp
L Connector_Generic:Conn_02x20_Odd_Even P1
U 1 1 59AD464A
P 2600 2000
F 0 "P1" H 2650 3117 50  0000 C CNN
F 1 "Conn_02x20_Odd_Even" H 2650 3026 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_2x20_P2.54mm_Vertical" H -2250 1050 50  0001 C CNN
F 3 "" H -2250 1050 50  0001 C CNN
	1    2600 2000
	1    0    0    -1  
$EndComp
Wire Wire Line
	2900 3000 3950 3000
Text Label 3950 3000 2    50   ~ 0
GPIO21(SPI1_SCK)
Wire Wire Line
	3100 1100 3100 1200
Wire Wire Line
	3000 2700 3000 3150
Wire Wire Line
	3000 2500 3000 2700
Wire Wire Line
	3000 2000 3000 2500
Wire Wire Line
	2300 3000 2300 3150
Wire Wire Line
	2200 1100 2200 1900
Wire Wire Line
	2300 2300 2300 3000
Wire Wire Line
	3000 1700 3000 2000
$Comp
L Connector:Conn_01x05_Female J?
U 1 1 5F8B568C
P 1300 4800
F 0 "J?" H 1450 4300 50  0000 C CNN
F 1 "Conn_01x05_Female" H 1450 4400 50  0000 C CNN
F 2 "" H 1300 4800 50  0001 C CNN
F 3 "~" H 1300 4800 50  0001 C CNN
	1    1300 4800
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5F8CF256
P 2150 5300
F 0 "#PWR?" H 2150 5050 50  0001 C CNN
F 1 "GND" H 2155 5127 50  0000 C CNN
F 2 "" H 2150 5300 50  0001 C CNN
F 3 "" H 2150 5300 50  0001 C CNN
	1    2150 5300
	-1   0    0    -1  
$EndComp
Wire Wire Line
	2150 5300 2150 5000
Wire Wire Line
	2150 4900 1500 4900
$Comp
L power:+12V #PWR?
U 1 1 5F8D3C82
P 1650 4250
F 0 "#PWR?" H 1650 4100 50  0001 C CNN
F 1 "+12V" H 1665 4423 50  0000 C CNN
F 2 "" H 1650 4250 50  0001 C CNN
F 3 "" H 1650 4250 50  0001 C CNN
	1    1650 4250
	-1   0    0    -1  
$EndComp
Wire Wire Line
	1650 4250 1650 4600
Wire Wire Line
	1650 4600 1500 4600
$Comp
L power:+5V #PWR?
U 1 1 5F8D5609
P 1900 4250
F 0 "#PWR?" H 1900 4100 50  0001 C CNN
F 1 "+5V" H 1915 4423 50  0000 C CNN
F 2 "" H 1900 4250 50  0001 C CNN
F 3 "" H 1900 4250 50  0001 C CNN
	1    1900 4250
	-1   0    0    -1  
$EndComp
Wire Wire Line
	1900 4250 1900 4700
Wire Wire Line
	1900 4700 1500 4700
Wire Wire Line
	1500 5000 2150 5000
Connection ~ 2150 5000
Wire Wire Line
	2150 5000 2150 4900
$Comp
L power:+3V3 #PWR?
U 1 1 5F8E9CCC
P 2150 4250
F 0 "#PWR?" H 2150 4100 50  0001 C CNN
F 1 "+3V3" H 2165 4423 50  0000 C CNN
F 2 "" H 2150 4250 50  0001 C CNN
F 3 "" H 2150 4250 50  0001 C CNN
	1    2150 4250
	1    0    0    -1  
$EndComp
Wire Wire Line
	2150 4250 2150 4800
Wire Wire Line
	2150 4800 1500 4800
$EndSCHEMATC
