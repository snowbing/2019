#include "stm32f10x.h"
#include "car.h"
#include "delay.h"
#include "bluetooth.h"
#include "echo.h"
int go_flag=0;
int echo_flag=0;
int main(void)
{
	

	bluetooth_init(); 
    SysTick_Init();//延时初始化
	echo_init(); 

	
	
	while(1)
	{
		
			Delay_ms(500); 
			/*if(get_length()<0.005)
			{
				if(go_flag ==1)//ignore back
				{
						gogogo(0);
				}
				
			}
			else if(go_flag == 1)
			{
				gogogo(1);
			}*/
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
//每次TIM5满后,开始一次超声波测距 
void TIM5_IRQHandler(void)
{
	/*if(TIM_GetITStatus(TIM5,TIM_IT_Update) != RESET)
	{
		TIM_ClearITPendingBit(TIM5, TIM_IT_Update);
		if(go_flag&&echo_flag)	//如果开启了回声功能 
			if(get_length()<0.005)
			{
			turnx(1);	
			Delay_ms(1500);
			turnx(2);
			}
		
	}*/
}
void USART1_IRQHandler(void)
{
	int order =0;	
	if(USART_GetITStatus(USART1,USART_IT_RXNE)==SET)
	{
		order = USART_ReceiveData(USART1);
		USART_ClearITPendingBit(USART1,USART_IT_RXNE);
		USART_ClearFlag(USART1,USART_IT_RXNE);
			switch(order)
			{
				case 1:case'1'://前进 
					go_flag=1;
					gogogo(1);
					break;
				case 2:case '2'://倒车 
					go_flag=2; 
					gogogo(-1);
					break;
				case 3:case'3'://加速 
					changeSpeed(-1);
					break;
				case 4:case '4'://减速 
					changeSpeed(1);
					break;
				case 5:case '5'://左转 
					//go_flag=1;
					turnx(1);
					break;
				case 6:case'6'://右转 
					//go_flag=1;
					turnx(2);
					break;
				case 7:case'7'://停车 
					gogogo(0);
					go_flag=0;
					break;
				case 8:case'8'://开启超声波
					echo_flag=1;
					break;
				case 9:case '9'://关闭超声 
					echo_flag=0;
					break; 
			}
		
	}

}
	
