from sklearn.datasets import fetch_openml      #mnist 파일을 받아온다.
mnist = fetch_openml('mnist_784',version =1)   
mnist.keys()

import numpy as np
data = mnist['data']
target = mnist['target']
print(np.unique(target))  #지금 여기서 mnist 데이터는 (1,784)의 크기로 나옴을 알 수 있음 그리그 문자형임
target = target.astype(int) #타겟은 문자형이므로 수치형으로 바꿔주는 것이 필요
print(np.unique(target))
#학습/테스트 셋 설정
train_data = data[0:50000]       #총 70000개 중 50000개를 훈련 데이터, 20000개를 테스트 데이터로 설정
train_target = target[0:50000]
test_data = data[50000:70000]
test_target = target[50000:70000]
print(train_data[0].shape)

from scipy.special import expit  #expit은 sigmoid를 의미한다
def active_sigmoid(value):
  return expit(value)

def diff_active_sigmoid(value): #시그모이드 미분
  diff = expit(value) * (1-expit(value))
  return diff

output = np.unique([0,1,2,3,4,5,6,7,8,9])  #target의 고유 원소들만 추출함 0~9까지가 담겨있음

class MLP(): #다층 퍼셉트론 class 생성
  def __init__(self,hidden,learning_rate,dataset,iteration,output,target): #파라미터들 선언
    self.hidden = hidden
    self.learning_rate = learning_rate
    self.dataset = dataset
    self.iteration = iteration
    self.output = output
    self.target = target

  def first_weight(self,dataset,output):
    U1 = np.random.uniform(-1.0,1.0,size=(self.hidden,len(dataset)))
    U2=  np.random.uniform(-1.0,1.0,size=(len(output),self.hidden))
    return U1,U2
    
  def train(self,U1,U2,data):
    zsum = np.dot(U1,data) #(hidden x 1)
    act_zsum = active_sigmoid(zsum)
    osum = np.dot(U2,act_zsum)
    act_osum = active_sigmoid(osum)
    return act_zsum, act_osum,zsum,osum


  def cal_gredient(self,U1,U2,act_osum,act_zsum,target,dataset,zsum,osum):
    err = np.zeros(len(output))  
    onehot_target = np.zeros(len(output))
    onehot_target[target] = 1
    err = act_osum - onehot_target
    err = err.reshape(10,1)
    
    err1 = np.multiply(err,diff_active_sigmoid(osum).reshape(10,1))
    act_zsum_t = act_zsum.reshape(1,self.hidden)
    gred2 = np.dot(err1,act_zsum_t)
    #gred2= err1.dot(act_zsum.T)
    ob_z = diff_active_sigmoid(zsum).reshape(self.hidden,1)
    err2 = np.multiply(np.dot(U2.transpose(),err1),ob_z) #(50*1)x(50*1)
    data = dataset.reshape(1,len(dataset))
    gred1 = np.dot(err2,data)
    return gred1, gred2
  
 

  def fit(self,dataset):
    for i in range(self.iteration):
      U1,U2 =self.first_weight(self.dataset[1],self.output)

      predict = np.ones(len(dataset))
      for j in range(len(dataset)):
        act_zsum,act_osum,zsum,osum = self.train(U1,U2,self.dataset[j])
        gred1, gred2 = self.cal_gredient(U1,U2,act_osum,act_zsum,self.target[j],self.dataset[j],zsum,osum)
        predict[j] = np.argmax(act_osum)
        U1 =U1- self.learning_rate * gred1
        U2 =U2- self.learning_rate * gred2
    return self.target,predict
   
  
    


train = MLP(500,0.01,train_data,8000,output,train_target)
target,predict=train.fit(train_data)
print(target)
print(predict)


#2번 세부 네트워크 구조 생성 (은닉층은 1개)

#1. 초기 가중치 설정
import numpy as np
weight_1 = np.random.uniform(-1.0,1.0,size=(500,784))   #첫번 째 층 가중치를 무작위로 생성  bias는 1로 고정한다   은닉층 개수는 50개
weight_2 = np.random.uniform(-1.0,1.0,size= (10,500)) #두번 째 은닉층 가중치를 무작위로 생성 bias는 마찬가지로 1로 고정한다  출력은 10개 중 하나
output = np.unique([0,1,2,3,4,5,6,7,8,9])  #target의 고유 원소들만 추출함 0~9까지가 담겨있음


#2. 활성화 함수 설정
from scipy.special import expit  #expit은 sigmoid를 의미한다
def active_sigmoid(value):
  return expit(value)

def diff_active_sigmoid(value): #시그모이드 미분
  diff = expit(value) * (1-expit(value))
  return diff

def active_relu(value):  #relu
  relu = max(0,value)
  return relu


def diff_active_relu(value):  #relu미분
  if (value>0):
      diff = 1
  elif (value<0):
      diff = 0
  return diff

#3. 퍼셉트론 생성
def classifier(dataset,target,weight1,weight2,learning_rate,activation,activation_diff,output_count):
  end_value = 0
  iter = 0
  error_count = 0
  zsum = np.zeros(len(dataset))
  osum = np.zeros(len(output_count))  #output_count는 단순히 출력층 개수를 의미하는 것임
  pred = np.zeros(len(target))
  final_pred = np.zeros(len(output_count))
  diff_2 = np.zeros(len(zsum))
  x = np.zeros(len(osum))
  
  while (end_value==0):   #무한 반복문 생성
    for i in range(len(dataset)):  #zsum,osum 구하기
      onehot_output = np.zeros(len(output_count))  #원핫 인코딩을 위한 array 생성
      zsum = np.dot(weight1,dataset[i])   #(800*1) zsum구하기
      osum = np.dot(weight2,activation(zsum))    #(10*800) osum구하기 
      o = activation(osum)     #predict (10*1)
      x = target[i]  #target[i] 인덱스를 추출
      onehot_output[x] = 1   #원핫 인코딩 시켜줌
      onehot_output = onehot_output.astype(int)
      #print('예측:',np.argmax(o))
      #print('타깃:',target[i])
      if (np.argmax(o) != target[i]):
        del2 = np.multiply((onehot_output-o),activation_diff(osum)) #(10x1)*(10x800)
        del2 = del2.reshape(10,1)
        zsum_t = zsum.reshape(1,500)
        delta2 = np.dot(del2,zsum_t) #(10,100)
        eta = np.dot(np.transpose(del2),weight2)
        eta_t = eta.transpose() #(800x1)
        zsum = zsum.reshape(500,1)
        del1 = np.multiply(eta_t, activation_diff(zsum))
        delta1 = np.dot(del1,x)
        weight2 -= learning_rate * delta2
        print(weight2)
        weight1 -= learning_rate * delta1
        #print(weight2)
        error_count+=1
      iter+=1
    if (error_count==0):
      end_value = 0
  return pred2[i]

x = classifier(train_data,train_target,weight_1,weight_2,0.01,active_sigmoid,diff_active_sigmoid,output)




  
