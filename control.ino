#include "config.h"
#include "control.h"

//------------------------------------------ㅡMOTOR_CONTROL-------------------------------------

motor_control::motor_control(int pin_num, int motor_mum, bool dir){
  int temp = motor_num;
  this -> pin_num = pin_num;
  this -> dir = dir;
  this -> motor_num = motor_num;
  this -> x_sign = (bool)(temp%2);
  this -> y_sign = (bool)((temp-(temp%2))/2);
}

void motor_control::cal_output(axis &x, axis &y) {
  this -> output_val += ( (this-> x_sign ? -1 * x.cal_PID() : x.cal_PID() ) + (this-> y_sign ? -1 * y.cal_PID() : y.cal_PID() ) );
}

void motor_control::output() {
//servo라이브러리로 BLDC모터 제어
}
