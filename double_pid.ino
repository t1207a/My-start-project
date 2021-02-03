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
