import arff
from math import exp,log
import matplotlib.pyplot as plt
src='/home/dhawal/Documents/AI Lab4/Classification_Datasets/diabetes.arff'

def load_arff():
    dataset = arff.load(open(src,'rb'))
    return dataset

def class_to_binary(data,column):
    for row in data:
        if row[column]=="tested_positive":
            row[column]=1
        else:
            row[column]=0

def predict(row,coeff):
    ycap=float(coeff[0])
    for i in range(len(row)-1):
        ycap+=float(row[i])*coeff[i+1]
    return 1/(1+exp(-ycap))

def class_estimator(val):
    if val>0.5:
        return 1
    else:
        return 0

def coeff_grad_des(data, l_rate, iter):
    coeff = [0.0 for i in range(len(data[0]))]
    m=len(data)
    for i in range(iter):
        J=0.0
        for row in data:
            sg_ycap = predict(row,coeff)
            error = sg_ycap - float(row[-1])
            J+=float(row[-1])*log(sg_ycap)+(1-float(row[-1]))*(log(1-sg_ycap))
            coeff[0] = coeff[0] - l_rate * error/m
            for k in range(len(row)-1):
                coeff[k + 1] = coeff[k + 1] - l_rate * error * float(row[k])/m
        J=-J/m
        print("Iteration-%d : J Value = %f") %(i+1,J)
    return coeff

dataset=load_arff()
data=dataset[u'data']
class_to_binary(data,-1)
coeff=coeff_grad_des(data,0.015,600)
print coeff
correct=0
x=[]
xd=[]
for i in range(len(data)):
    print class_estimator(predict(data[i],coeff)),data[i][-1]
    if class_estimator(predict(data[i],coeff))==data[i][-1]:
        correct+=1
    if len(x)==0 or len(xd)==0:
        if class_estimator(predict(data[i],coeff))==0:
            x = [[data[0][j]] for j in range(len(data[0])-1)]
        else :
            xd = [[data[0][j]] for j in range(len(data[0])-1)]
    else:
        if class_estimator(predict(data[i],coeff))==0:
            for j in range(len(data[0])-1):
                x[j].append(data[i][j])
        else :
            for j in range(len(data[0])-1):
                xd[j].append(data[i][j])
print("\nAccuracy : %f") %(float(correct)/float(len(data)))
#for i in range(len(data)-1):
    #plt.plot(x[i],[0.0 for j in range(len(x[i]))],"ro",xd[i],[1.0 for j in range(len(xd[i]))],"b+")
    #plt.show()
plt.plot(x[0],x[1],"ro",xd[0],xd[1],"b+")
plt.show()
