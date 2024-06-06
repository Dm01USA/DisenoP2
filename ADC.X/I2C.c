/*
 * File:   I2C.c
 * Author: dmore
 *
 * Created on 2 de junio de 2024, 14:53
 */


#include <p33FJ128MC802.h>

#include "xc.h"
#include "I2C.h"

void I2C_INIT(void){
    I2C1CONbits.I2CEN=1;//habilita el I2C
    IFS1bits.MI2C1IF=0;
    //I2CBRG=(((1/FSCL)-DELAY)*(FCY))-2
    //DELAY=110nS a 130nS
    //I2CBRG=37
    I2C1BRG=37;//400KHZ FSCL
    


}
void I2C_START(void){
    IFS1bits.MI2C1IF=0;
    I2C1CONbits.SEN=1;
    while(IFS1bits.MI2C1IF==0);
}

void I2C_STOP(void){
    IFS1bits.MI2C1IF=0;
    I2C1CONbits.PEN=1;
    while(IFS1bits.MI2C1IF==0);
}


void I2C_ACK(void){
    IFS1bits.MI2C1IF=0;
    I2C1CONbits.ACKEN=1;
    I2C1CONbits.ACKDT=0; 
    while(IFS1bits.MI2C1IF==0);
}
void I2C_NACK(void){
    IFS1bits.MI2C1IF=0;
    I2C1CONbits.ACKEN=1;
    I2C1CONbits.ACKDT=1; 
    while(IFS1bits.MI2C1IF==0);
}

void I2C_TX(char Data){
    IFS1bits.MI2C1IF=0;
    I2C1TRN=Data;
    I2CTRN=Data;
    
    while(IFS1bits.MI2C1IF==0);
}

void I2C_RX(void){
    IFS1bits.MI2C1IF=0;
    I2C1CONbits.RCEN=1;
    
    while(IFS1bits.MI2C1IF==0);
    return I2C1RCV;
    
}

