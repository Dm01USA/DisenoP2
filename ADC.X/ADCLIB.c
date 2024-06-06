/*
 * File:   ADCLIB.c
 * Author: dmore
 *
 * Created on 25 de mayo de 2024, 20:51
 */


#include "xc.h"
#include "ADCLIB.h"

void ADC_INIT(void){
    AD1PCFGL=0;//
    AD1CON2bits.VCFG=0b000;
    AD1CON1bits.AD12B  = 1;	
    AD1CON2bits.CHPS  = 0;
    AD1CON3bits.ADRC=0;
    AD1CON1bits.ASAM=1;
    AD1CHS0bits.CH0SA=0b000; //canal 0
    AD1CON3bits.ADCS=1;
    AD1CON3bits.SAMC=1;
    AD1CON1bits.SSRC=0b000;
    AD1CON1bits.ADON=1;
    AD1CON1bits.FORM=0b10;
    
    //ADCS=(TAD/TCY)-1
    //TCY=1/FCY
    //TCY=1/16379000
    //TCY=6.1053X10-8
    //ADCS=1
    //TAD PARA 12 BITS 117.6NS
    
    


}