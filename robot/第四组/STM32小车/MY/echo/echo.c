#include "echo.h"
#include "delay.h"
int toofar=0;
int psc = 71;	//分频系数  72 000 000 /72 =1us , *1000 0=10ms(1.5米)意味足够远,不予考虑 

void echo_clock_close(void)//暂时废弃 
{
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM5, DISABLE);
	TIM_ITConfig(TIM5,TIM_IT_Update,DISABLE);

}
void echo_clock_init(void)//每经过一段时间,就自动开始超声波测距 
{
	TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructer;
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM5, ENABLE);
	TIM_TimeBaseInitStructer.TIM_Period=19999;// 定时周期为 7200 0000 *2 2s
	TIM_TimeBaseInitStructer.TIM_Prescaler=7100; 
	TIM_TimeBaseInitStructer.TIM_ClockDivision=0; 
	TIM_TimeBaseInitStructer.TIM_CounterMode=TIM_CounterMode_Up;
	TIM_TimeBaseInitStructer.TIM_RepetitionCounter = 0	;
	TIM_TimeBaseInit(TIM5,&TIM_TimeBaseInitStructer);

	TIM_ITConfig(TIM5,TIM_IT_Update,ENABLE);
	NVIC_InitTypeDef NVIC_InitStructer;
	NVIC_InitStructer.NVIC_IRQChannelPreemptionPriority=2;
	NVIC_InitStructer.NVIC_IRQChannelSubPriority=1;
	NVIC_InitStructer.NVIC_IRQChannel=TIM5_IRQn;
	NVIC_InitStructer.NVIC_IRQChannelCmd=ENABLE;
	NVIC_Init(&NVIC_InitStructer);
	TIM_Cmd(TIM5,ENABLE);
}	

/* 初始化模块的 GPIO 以及初始化定时器 TIM2*/
void echo_init(void)
{
	echo_clock_init();
	TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructer;
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE);
	TIM_TimeBaseInitStructer.TIM_Period=9999;// 定时周期为 10000
	TIM_TimeBaseInitStructer.TIM_Prescaler=psc; 
	TIM_TimeBaseInitStructer.TIM_ClockDivision=0; 
	TIM_TimeBaseInitStructer.TIM_CounterMode=TIM_CounterMode_Up;
	TIM_TimeBaseInitStructer.TIM_RepetitionCounter = 0	;
	TIM_TimeBaseInit(TIM2,&TIM_TimeBaseInitStructer);

	TIM_ITConfig(TIM2,TIM_IT_Update,ENABLE);
	NVIC_InitTypeDef NVIC_InitStructer;
	NVIC_InitStructer.NVIC_IRQChannelPreemptionPriority=2;
	NVIC_InitStructer.NVIC_IRQChannelSubPriority=2;
	NVIC_InitStructer.NVIC_IRQChannel=TIM2_IRQn;
	NVIC_InitStructer.NVIC_IRQChannelCmd=ENABLE;
	NVIC_Init(&NVIC_InitStructer);
	TIM_Cmd(TIM2,DISABLE);// 关闭定时器使能




	GPIO_InitTypeDef GPIO_InitStructer;
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);
	/*TRIG 信号 */
	GPIO_InitStructer.GPIO_Speed=GPIO_Speed_50MHz;
	GPIO_InitStructer.GPIO_Mode=GPIO_Mode_Out_PP;
	GPIO_InitStructer.GPIO_Pin=GPIO_Pin_8;
	GPIO_Init(GPIOB, &GPIO_InitStructer);
	/*ECOH 信号 */
	GPIO_InitStructer.GPIO_Mode=GPIO_Mode_IN_FLOATING;
	GPIO_InitStructer.GPIO_Pin=GPIO_Pin_9;
	GPIO_Init(GPIOB, & GPIO_InitStructer);
}
 	
 	
double get_length(void)
{
	double length=0;
	long int t;
	double time; 
		GPIO_SetBits(GPIOB,GPIO_Pin_8); 
		Delay_us(20); 
		GPIO_ResetBits(GPIOB,GPIO_Pin_8);  
		while(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_9)==RESET);
		TIM_Cmd(TIM2,ENABLE);// 回响信号到来，开启定时器计数
		while(GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_9)==SET);
		TIM_Cmd(TIM2,DISABLE);// 关闭定时器
		if(!toofar)	//没有完成一次计数周期,即距离不是很远 
		{
			t=TIM_GetCounter(TIM2);// 获取 TIM2 寄存器中的计数值
			time = t/1000000; //往返时间,单位s 
			length =  340*time/2; //单程长度,单位m 
			TIM2->CNT=0; // 将 TIM2 计数寄存器的计数值清零
		}
		else
		{
			toofar = 0; 
			length =99;	//足够远,不用考虑 
			TIM2->CNT=0; // 将 TIM2 计数寄存器的计数值清零
		}
	return length;
}
void TIM2_IRQHandler(void) // 中断，当距离足够远时,设置toofar = 1,不必再计算 
{
	if(TIM_GetITStatus(TIM2,TIM_IT_Update)!=RESET)
	  {
		TIM_ClearITPendingBit(TIM2,TIM_IT_Update);// 清除中断标志
		toofar = 1; 
	  }
}
