#include "stm32f10x.h"

void infrared_init(void);
u16 Get_Adc(u8 ch);
u16 Get_Adc_Average(u8 ch,u8 times);
void infr_clock_init(void);
void Usart1_Init(void);
