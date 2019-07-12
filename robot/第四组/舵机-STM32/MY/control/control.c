#include "control.h"
void control_init()
{
	 GPIO_InitTypeDef GPIO_InitStructure;
	 USART_InitTypeDef U;
	 NVIC_InitTypeDef NVIC_InitStructure;
	
	 RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);
   RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOE, ENABLE);
   GPIO_InitStructure.GPIO_Pin = GPIO_Pin_5;
   GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
   GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
   GPIO_Init(GPIOB, &GPIO_InitStructure);
   GPIO_Init(GPIOE, &GPIO_InitStructure);
	
	 
	 NVIC_PriorityGroupConfig(NVIC_PriorityGroup_4);
	 RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1,ENABLE); 
 	 RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);

	 GPIO_InitStructure.GPIO_Pin=GPIO_Pin_9;        
    //GPIO_InitStructure.GPIO_Mode=GPIO_Mode_Out_PP; 
	 //GPIO_InitStructure.GPIO_Speed = GPIO_Speed_10MHz;
   GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;  
    //GPIO_InitStructure.GPIO_Speed=GPIO_Speed_50MHz;        
   GPIO_Init(GPIOA,&GPIO_InitStructure);  
	
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
	 U.USART_Mode = USART_Mode_Rx|USART_Mode_Tx;
	 USART_Init(USART1,&U);
	 USART_ITConfig(USART1,USART_IT_RXNE,ENABLE);
	 USART_Cmd(USART1,ENABLE);
 } 

