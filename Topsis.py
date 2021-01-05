import pandas as pd
import numpy
import sys
l=len(sys.argv)


if len(sys.argv) < 5:
    print ("Error !! Require 5 number of parameters including python file")
    print ("example: python topsis.py inputfile.csv “1,1,1,2” “+,+,-,+” result.csv")
    exit(0)
    

csv = pd.read_csv(sys.argv[1])
if len(csv.columns )< 3:
    print("Error !! Input file must contain 3 or more colums")
    exit(0)
weights=sys.argv[2].split(',')  
impact=sys.argv[3].split(',')

if (len(csv.columns)-1!=len(weights)) or (len(csv.columns)-1!=len(impact)) or len(impact)!=len(weights):
    print("Number of weights, number of impacts and number of columns (from 2nd to last columns) must be same")
    exit(0)

features = len(csv.columns)-1
root_sum_square = []
normalized_performance_value=[]

for i in range(features):
    col=list(csv.iloc[:,i+1])
    col_2=[i**2 for i in col ]
    a=sum(col_2)
    b=a**(1/2)
    root_sum_square.append(b)
    temp = [i/b for i in col ]
    temp_ = [j*float(weights[i]) for j in temp]
    normalized_performance_value.append(temp_)
    
    
ideal_best=[]
ideal_worst=[]
index=0
for i in range(len(normalized_performance_value)):
    if(impact[i]=='+'):
        ideal_best.append(max(normalized_performance_value[i]))
        ideal_worst.append(min(normalized_performance_value[i]))
    if(impact[i]=='-'):
        ideal_best.append(min(normalized_performance_value[i]))
        ideal_worst.append(max(normalized_performance_value[i]))
    
        

decision_matrix=numpy.transpose(normalized_performance_value)

ideal_best_distance=[]
for i in range(len(decision_matrix)):
    val=0
    a=decision_matrix[i]
    for j in range(len(a)):
        val=val+((a[j]-ideal_best[j])**2)
    ideal_best_distance.append(val**(1/2))

ideal_worst_distance=[]
for i in range(len(decision_matrix)):
    val=0
    a=decision_matrix[i]
    for j in range(len(a)):
        val=val+((a[j]-ideal_worst[j])**2)
    ideal_worst_distance.append(val**(1/2))

score=[]
for i in range(len(ideal_worst_distance)):
    score.append(ideal_worst_distance[i]/(ideal_worst_distance[i]+ideal_best_distance[i]))
    
rank=[]
for i in range(len(score)):
    rank_=1
    for j in range(len(score)):
        if i!=j:
            if(score[j]>score[i]):
                rank_=rank_+1
    rank.append(rank_)
    

df=[]
for i in range(len(csv.columns)):
    df.append(list(csv.iloc[:,i]))
df.append(score)
df.append(rank)
df=numpy.transpose(df)
   
res = pd.DataFrame(df)
res.columns=list(csv.columns) + ['Topsis Score','Rank']
res.to_csv(sys.argv[4], index = False) 

print("TOPSIS generated")