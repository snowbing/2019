#include "car.h" 
#include "delay.h"
int carSpeedPeriod = 0;

void car_init(int i)
{
	//和转方向相关的引脚 
	 GPIO_InitTypeDef GPIO_InitStructure;
 	 RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOD, ENABLE);
 	 GPIO_InitStructure.GPIO_Pin =GPIO_Pin_1| GPIO_Pin_2 | GPIO_Pin_3 | GPIO_Pin_4;
 	 GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
 	 GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;//推挽输出? 
 	 GPIO_Init(GPIOD, &GPIO_InitStructure);
 	 //和timer相关的引脚
	  RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);
	  RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB,ENABLE);
	  RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3,ENABLE); 
	  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_6|GPIO_Pin_7;
	  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;//抄呼吸灯 
	  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	  GPIO_Init(GPIOA,&GPIO_InitStructure);
	  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0|GPIO_Pin_1;	  
	  GPIO_Init(GPIOB,&GPIO_InitStructure);
	
	TIM_TimeBaseInitTypeDef T;
	
	carSpeedPeriod+= i;
	T.TIM_Period  = carSpeedPeriod;
	T.TIM_Prescaler = 719;
	T.TIM_ClockDivision = 0;
	T.TIM_CounterMode = TIM_CounterMode_Up;
	T.TIM_RepetitionCounter = 0	;
	TIM_TimeBaseInit(TIM3,&T);
	TIM_Cmd(TIM3,ENABLE);
	TIM_ITConfig(TIM3,TIM_IT_Update,ENABLE);
	
	TIM_OCInitTypeDef O;
	O.TIM_OCMode = TIM_OCMode_PWM2;
	O.TIM_Pulse =5;
	O.TIM_OutputState = TIM_OutputState_Enable;
	O.TIM_OCPolarity=TIM_OCPolarity_Low;
	TIM_OC1Init(TIM3,&O);
	TIM_OC2Init(TIM3,&O);
	TIM_OC3Init(TIM3,&O);
	TIM_OC4Init(TIM3,&O);
	  
	NVIC_InitTypeDef NVIC_InitStructure;
	NVIC_InitStructure.NVIC_IRQChannel = TIM3_IRQn ;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0;
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 0;
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	NVIC_Init(&NVIC_InitStructure); 
	   } 
	   
	   
// 控制车子的运作方向	   
void gogogo(int direction)
{
	//前进 
	if(direction == 1)
	{
		carSpeedPeriod = 0;
		car_init(30);
		GPIO_WriteBit(GPIOD, GPIO_Pin_2,Bit_SET);
		GPIO_WriteBit(GPIOD, GPIO_Pin_4,Bit_SET);
		GPIO_WriteBit(GPIOD, GPIO_Pin_1,Bit_RESET);
		GPIO_WriteBit(GPIOD, GPIO_Pin_3,Bit_RESET);
	}
	//停车 
	else if(direction == 0)
	{
		RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3,DISABLE); 
		TIM_Cmd(TIM3,DISABLE);
	}
	//后退 
	else if(direction == -1)
	{
		carSpeedPeriod = 0;
		car_init(30);
		GPIO_WriteBit(GPIOD, GPIO_Pin_2,Bit_RESET);
		GPIO_WriteBit(GPIOD, GPIO_Pin_4,Bit_RESET);
		GPIO_WriteBit(GPIOD, GPIO_Pin_1,Bit_SET);
		GPIO_WriteBit(GPIOD, GPIO_Pin_3,Bit_SET);
	}
}
	
//转向,没有考虑回正 
void turnx(int direction)
{
	//左转 
	if(direction == 1)
	{
		GPIO_WriteBit(GPIOD, GPIO_Pin_1,Bit_SET);
		GPIO_WriteBit(GPIOD, GPIO_Pin_3,Bit_SET);
		GPIO_WriteBit(GPIOD, GPIO_Pin_2,Bit_SET);
		GPIO_WriteBit(GPIOD, GPIO_Pin_4,Bit_SET);
	}
	//右转 
	if(direction == 2)
	{
		GPIO_WriteBit(GPIOD, GPIO_Pin_1,Bit_RESET);
		GPIO_WriteBit(GPIOD, GPIO_Pin_3,Bit_RESET);
		GPIO_WriteBit(GPIOD, GPIO_Pin_2,Bit_RESET);
		GPIO_WriteBit(GPIOD, GPIO_Pin_4,Bit_RESET);
	}
}
void turn(int direction)
{
	//左转 
	if(direction == 1)
	{
		turnx(1); 
		Delay_ms(1000);
		gogogo(1);//回轮 
	}
	//右转 
	else if(direction == 2)
	{
		turnx(2);
		Delay_ms(1000);
		gogogo(1);
	}	
}

//重新初始化周期 ，暂时废弃
void changeSpeedx(int i)
{
	
	TIM_TimeBaseInitTypeDef T;
	carSpeedPeriod += i;
	T.TIM_Period  = carSpeedPeriod;
	T.TIM_Prescaler = 719;
	T.TIM_ClockDivision = 0;
	T.TIM_CounterMode = TIM_CounterMode_Up;
	T.TIM_RepetitionCounter = 0	;
	TIM_TimeBaseInit(TIM3,&T);
	TIM_Cmd(TIM3,ENABLE);
	TIM_ITConfig(TIM3,TIM_IT_Update,ENABLE);
}
//改变速度,通过改变周期 
void changeSpeed(int i)
{
	if(carSpeedPeriod > 2)//不能再小了 
	car_init(i*2);
}

