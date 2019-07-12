#include "car.h" 
#include "delay.h"
int carSpeedPeriod = 0;

void car_init(int i,int j)
{
	//和转方向相关的引脚 
	 GPIO_InitTypeDef GPIO_InitStructure;
 	 RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOD, ENABLE);//shi neng duan kou shi zhong
 	 GPIO_InitStructure.GPIO_Pin =GPIO_Pin_1;
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
	
	carSpeedPeriod+= i;//i=199
	T.TIM_Period  = carSpeedPeriod;
	T.TIM_Prescaler = 7199;
	T.TIM_ClockDivision = 0;
	T.TIM_CounterMode = TIM_CounterMode_Up;
	T.TIM_RepetitionCounter = 0	;
	TIM_TimeBaseInit(TIM3,&T);
	TIM_Cmd(TIM3,ENABLE);
	TIM_ITConfig(TIM3,TIM_IT_Update,ENABLE);
	
	TIM_OCInitTypeDef O;
	O.TIM_OCMode = TIM_OCMode_PWM2;
	O.TIM_Pulse =j;//she zhi zhan kong bi
	O.TIM_OutputState = TIM_OutputState_Enable;
	O.TIM_OCPolarity=TIM_OCPolarity_Low;
	TIM_OC1Init(TIM3,&O);
	
	  
	NVIC_InitTypeDef NVIC_InitStructure;
	NVIC_InitStructure.NVIC_IRQChannel = TIM3_IRQn ;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0;
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 0;
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	NVIC_Init(&NVIC_InitStructure); 
	  
} 	   

void static_pole(){
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3,DISABLE); 
	TIM_Cmd(TIM3,DISABLE);
}

void up(){
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3,ENABLE); 
	TIM_Cmd(TIM3,ENABLE);
	car_init(199,15);
}

void down(){
	//TIM_SetCompare2(TIM3,25);
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3,ENABLE); 
	TIM_Cmd(TIM3,ENABLE);
	car_init(199,25);
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


