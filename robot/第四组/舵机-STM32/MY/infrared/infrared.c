#include "infrared.h"
#include "delay.h"

void infr_clock_init(void)//每经过一段时间,就自动开始测距 
{
	TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructer;
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM5, ENABLE);
	TIM_TimeBaseInitStructer.TIM_Period=19999;// 定时周期为 7200 0000 *2 2s
	TIM_TimeBaseInitStructer.TIM_Prescaler=7199; 
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
	//NVIC_Init(&NVIC_InitStructer);
	TIM_Cmd(TIM5,ENABLE);
}	

void infrared_init(void){
	GPIO_InitTypeDef GPIO_InitStructure;
	ADC_InitTypeDef ADC_InitStructure;
	
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA|RCC_APB2Periph_ADC1, ENABLE);
	RCC_ADCCLKConfig(RCC_PCLK2_Div6);
	
	GPIO_InitStructure.GPIO_Pin =GPIO_Pin_0;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AIN; 
	GPIO_Init(GPIOA, &GPIO_InitStructure);
	 
	//ADC_DeInit(ADC1); 
  ADC_InitStructure.ADC_Mode = ADC_Mode_Independent; 
  ADC_InitStructure.ADC_ScanConvMode = DISABLE; 
  ADC_InitStructure.ADC_ContinuousConvMode = DISABLE; 
  ADC_InitStructure.ADC_ExternalTrigConv = ADC_ExternalTrigConv_None;
	ADC_InitStructure.ADC_DataAlign = ADC_DataAlign_Right;
	ADC_InitStructure.ADC_NbrOfChannel=1;
	ADC_Init(ADC1, &ADC_InitStructure);
	ADC_Cmd(ADC1, ENABLE);
	ADC_ResetCalibration(ADC1);
	
	while(ADC_GetResetCalibrationStatus(ADC1));
	ADC_StartCalibration(ADC1);
	while(ADC_GetCalibrationStatus(ADC1));
}

void Usart1_Init(void)
{
	NVIC_InitTypeDef NVIC_InitStructure;
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_4);
  GPIO_InitTypeDef GPIO_InitStructure;
  RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);
  RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOE, ENABLE);
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_5;
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
  GPIO_Init(GPIOB, &GPIO_InitStructure);
  GPIO_Init(GPIOE, &GPIO_InitStructure);
	
	 USART_InitTypeDef U;
	 //NVIC_PriorityGroupConfig(NVIC_PriorityGroup_4);
	 RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1,ENABLE);
 	 RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);

	GPIO_InitStructure.GPIO_Pin=GPIO_Pin_9;           // ???? PIN
        //GPIO_InitStructure.GPIO_Mode=GPIO_Mode_Out_PP; // ????
GPIO_InitStructure.GPIO_Speed = GPIO_Speed_10MHz;
        GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;  // ??????
        //GPIO_InitStructure.GPIO_Speed=GPIO_Speed_50MHz;        // ????
        GPIO_Init(GPIOA,&GPIO_InitStructure);        // ?? IO



 	 GPIO_InitStructure.GPIO_Pin =GPIO_Pin_10;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_10MHz;
 	 GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING;
 	  	 GPIO_Init(GPIOA, &GPIO_InitStructure);

	NVIC_InitStructure.NVIC_IRQChannel = USART1_IRQn ;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1;
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
	NVIC_Init(&NVIC_InitStructure); 

	USART_DeInit(USART1);
	U.USART_BaudRate = 9600;
	U.USART_WordLength = USART_WordLength_8b;
	U.USART_StopBits = USART_StopBits_1;
	U.USART_Parity = USART_Parity_No;
	U.USART_HardwareFlowControl = USART_HardwareFlowControl_None;
	U.USART_Mode=USART_Mode_Rx|USART_Mode_Tx;
	USART_Init(USART1,&U);
	USART_Cmd(USART1,ENABLE);
}
u16 Get_Adc(u8 ch){
	ADC_RegularChannelConfig(ADC1, ADC_Channel_0, 1, ADC_SampleTime_239Cycles5 );
	ADC_SoftwareStartConvCmd(ADC1, ENABLE); 
	while(!ADC_GetFlagStatus(ADC1, ADC_FLAG_EOC ));
	ADC_ClearFlag(ADC1, ADC_FLAG_EOC);
	return ADC_GetConversionValue(ADC1); 
}

u16 Get_Adc_Average(u8 ch,u8 times){
	u32 temp_val=0;
	u8 t;
	for(t=0;t<times;t++){
		temp_val+=Get_Adc(ch);
		Delay_ms(5);
	}
	return temp_val/times;
}