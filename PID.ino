#include "PID.h"
#include "config.h"

//------------------------------------------ㅡAXIS-------------------------------------

axis::axis(float Kp_1, float Kp_2, float ki, float kd) {  //각 비례 값 받아오기
  this -> Kp_1 = Kp_1;
  this -> Kp_2 = Kp_2;
  this -> Ki = Ki;
  this -> Kd = Kd;
}

void axis::set_angle_target(float angle_target){ //타겟 각도 받기
  this->angle_target = angle_target;
}


void axis::set_angle_current(float angle_current){   //현재 각도 받기
  this->angle_current = angle_current;
}


void axis:: set_current_rate(float current_rate){  //현재 각속도 받기
  this -> current_rate = current_rate;
}


float axis::cal_angle_err() {   //각도 오류 계산
  e_tmp = angle_err;
  angle_err =  angle_target - angle_current;

}


float axis::P_angle(){  //p비례 값을 활용해 각속도 타깃 생성
  p_tmp=  p_angle;
  p_angle= (angle_err)  * (Kp_1); 
  }



#ifdef FLEX_T   //시간 받아와서 dt계산 텀
float axis::cal_dt() {
  float t = millis() / 1000;

  this -> dt = t - (this -> t_tmp);
  this -> t_tmp = t;

  return this -> dt;
}
#endif

#ifdef FIX_T
float axis::cal_dt() {
  this -> dt = FIX_T / 1000

  return this -> dt;
  }
#endif


float axis:: cal_rate_err(){  //각속도 에러 계산
  r_tmp = rate_err;
  rate_err =(p_angle) - (current_rate);
}


float axis::cal_inte() {    //적분 항
  inte = (current_rate) * (dt);
  return inte;
}

float axis::cal_diff() {  //미분 항
  diff  = ((current_rate) - (p_tmp)) / (dt);
  return this -> diff;
}

float axis::cal_PID() {   //최종 PID계산
  this-> PID_val = (kp_2) * (cal_rate_err()) + (ki) * (cal_inte()) + (kd) * (cal_diff());
  return PID_val;
}

float axis::get_PID(){  //PID값 호출
  return PID_val;
}

float axis::get_kp_1(){   //비례 값 호출
  return Kp_1;
}

float axis::get_Kp_2(){
  return Kp_2
}

float axis::get_ki(){
  return ki;
}

float axis::get_kd(){
  return kd;
}

float axis::get_angle_err(){
  return angle_err;
}

void axis::set_const(double kp_1, double Kp_2, double ki, double kd ){
  this -> Kp_1 = Kp_1;
  this -> kP_2 = kP_2;
  this -> Ki = Ki;
  this -> Kd = Kd;
}






double target_angle[3]={0,0,0};
double current_angle[3]={0,0,0};
double final_pid[3]={0,0,0};
double current_rate[3]= {0,0,0};
float Kp_1[3] = {0,0,0};
float Kp_2[3] = {0,0,0};
float Ki[3] = {0,0,0};
float Kd[3] = {0,0,0};

static unsigned long t_prev = 0;
unsigned long t_now = micros();
double dt = (t_now - t_prev)/1000000.0;
t_prev = t_now;

//roll pid
final_pid[0] = pid_control(current_angle[0],target_angle[0],Kp_1[0],Kp_2[0],Ki[0],Kd[0]);

//pitch pid
final_pid[1] = pid_control(current_angle[1],target_angle[1],Kp_1[1],Kp_2[1],Ki[1],Kd[1]);


double pid_control(double current_angle,double target_angle, double Kp_1,double Kp_2,double Ki, double Kd, double current_rate){
  double angle_error;
  double Target_rate;
  double P_rate, I_rate, D_rate;
  double Rate_error_previous;
  double Rate_error;
  double pid_sum;
  angle_error= target_angle- current_angle;
  Target_rate= Kp_1 * angle_error;  //에러에 대한 P적용 각속도 형성
  
  //각속도 PID제어 
  Rate_error= Target_rate - current_rate;
  P_rate = Kp_2 * Rate_error;
  I_rate += Ki * Rate_error * dt;
  D_rate = Kd * (Rate_error- Rate_error_previous)/dt;
  pid_sum = P_rate + I_rate + D_rate;
  Rate_error_previous = Rate_error;
  return pid_sum;
}
