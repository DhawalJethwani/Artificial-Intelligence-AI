import arff
src='/home/dhawal/Documents/AI Lab4/data1.arff'

def load_arff():
    dataset = arff.load(open(src,'rb'))
    return dataset

def unicode_column_to_int(data,column):
    for row in data:
        row[column] = float(row[column])

def data_minmax(data):
    minmax=[]
    col=[]
    for i in range(len(data[0])):
        col.append([row[i] for row in data])
        min_val=min(col[i])
        max_val=max(col[i])
        minmax.append([min_val,max_val])
    return minmax

def normalize(data):
    minmax=data_minmax(data)
    for i in range(len(data[0])):
        for j in range(len(data)):
            data[j][i]=(data[j][i]-minmax[i][0])/(minmax[i][1]-minmax[i][0])

def predict(row,coeff):
    ycap=coeff[0]
    for i in range(len(row)-1):
        ycap+=row[i]*coeff[i+1]
    return ycap

def coeff_grad_des(data, l_rate, iter):
    coeff = [0.0 for i in range(len(data[0]))]
    m=len(data)
    for i in range(iter):
        J=0.0
        for row in data:
            ycap = predict(row,coeff)
            error = ycap - row[-1]
            coeff[0] = coeff[0] - l_rate * error/m
            for k in range(len(row)-1):
                coeff[k + 1] = coeff[k + 1] - l_rate * error * row[k]/m
            J+=error**2
        J=J/(2*m)
        print("Iteration-%d : J Value = %f") %(i+1,J/10000)
    return coeff

dataset=load_arff()
data=dataset[u'data']
print(data)
#unicode_column_to_int(data,3)
#minmax=data_minmax(data)
#normalize(data)
coeff=coeff_grad_des(data,0.00001,20000)
print "\n"
for i in range(len(coeff)):
    print ("Theta[%d]:%f") %(i,coeff[i])
print "\n"
for i in range(len(data)):
    print ("Predicted:%f Actual:%f") %(predict(data[i],coeff),data[i][-1])
    #print ("Predicted:%f Actual:%f") %((minmax[-1][1]-minmax[-1][0])*predict(data[i],coeff)+minmax[-1][0],(minmax[-1][1]-minmax[-1][0])*data[i][-1]+minmax[-1][0])
