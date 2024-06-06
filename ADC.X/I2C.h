#ifndef XC_HEADER_TEMPLATE_H
#define	XC_HEADER_TEMPLATE_H

#include <xc.h> // include processor files - each processor file is guarded.  

void I2C_INIT(void);
void I2C_START(void);
void I2C_STOP(void);
void I2C_ACK(void);
void I2C_NACK(void);
void I2C_TX(char Data);
void I2C_RX(void);


#endif	/* XC_HEADER_TEMPLATE_H */
