#include "stm32f10x.h"
#include "car.h"
#include "delay.h"
#include "control.h"
#include "echo.h"
#include "infrared.h"
int main(void)
{
	float a=0.0;
	char len;
	control_init(); 
  SysTick_Init();//延时初始化
	echo_init();
	infrared_init();
	//Usart1_Init();
	
	while(1)
	{ len='0';
		a=(((float)Get_Adc(ADC_Channel_1))/4096)*3.3;
		if(a>=0.95){
			len = '1';
		}
		USART_SendData(USART1,len);						
		while(USART_GetFlagStatus(USART1, USART_FLAG_TC) == RESET);	
		static_pole();
		Delay_ms(2000);
	}
	
}

//每次timer之后 
void TIM3_IRQHandler(void)
{
	if(TIM_GetITStatus(TIM3,TIM_IT_Update) != RESET)
	{
		TIM_ClearITPendingBit(TIM3, TIM_IT_Update);
	}
}
void USART1_IRQHandler(void)
{
	int order= 0 ;	
	if(USART_GetITStatus(USART1,USART_IT_RXNE)==SET)
	{
		  order = USART_ReceiveData(USART1);
			USART_ClearITPendingBit(USART1,USART_IT_RXNE);
			USART_ClearFlag(USART1,USART_IT_RXNE);

			switch(order)
			{
				case 0x00000031://前进 
					up();
					break;
				case 0x00000032://倒车 
					down();
					break;
			}
		
	}
}
	
