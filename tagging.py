import pickle
from math import log10
import os
src="./../Text_Files/test.txt"

pkl="./../Models/tagger.pkl"
pk=open(pkl,"rb")
emission=pickle.load(pk)
prior=pickle.load(pk)
transition=pickle.load(pk)
pk.close()

predicted_tags=[]
word_list=[]
mv=1e100
all_tags=set()
for key in transition.keys():
    all_tags.add(key)
    for k in transition[key].keys():
        all_tags.add(k)
for key in emission.keys():
    all_tags.add(key)
with open(src,"r") as f:
    lastline=""
    for line in f:
        line=line.rstrip()
        lastline=lastline.rstrip()
        if len(line)!=0:
            l=line.split()
            ll=lastline.split()
            word_list.append(l[0])
            if len(lastline)==0:
                T1=[]
                T2=[]
                T1.append({})
                T2.append({})
                for tag in prior.keys():
                    try:
                        T2[len(word_list)-1][tag]=0
                        T1[0][tag]=log10(prior[tag])+log10(emission[tag][l[0]])
                    except Exception as e:
                        T1[0][tag]=-mv
                        pass
            else:
                word=len(word_list)-1
                T1.append({})
                T2.append({})
                for tag in all_tags:
                    maxi=-mv
                    max_tag=""
                    for ptag in all_tags:
                        try:
                            p=T1[word-1][ptag]+log10(transition[ptag][tag])
                        except:
                            p=-mv
                        if p>=maxi:
                            maxi=p
                            max_tag=ptag
                    try:
                        T1[word][tag]=maxi+log10(emission[tag][word_list[-1]])
                    except:
                        T1[word][tag]=-mv
                    T2[word][tag]=max_tag
        else:
            max_tag=""
            maxi=-mv
            x=[0 for i in range(len(word_list))]
            predicted_tags.append(x)
            for i in all_tags:
                if maxi < T1[len(word_list)-1][i]:
                    maxi=T1[len(word_list)-1][i]
                    max_tag=i
            words=len(word_list)
            x[words-1]=word_list[words-1]+" "+max_tag
            for i in range(words-1,0,-1):
                wt=x[i].split(' ')
                x[i-1]=word_list[i-1]+" "+T2[i][wt[1]]
            word_list=[]
        lastline=line
f.close()

os.remove("./../Models/tagger.pkl")
src="./../Text_Files/predicted_tags.txt"
with open(src,'w') as m:
    for sentence in predicted_tags:
        for wt in sentence:
            wt=wt.split()
            m.write(wt[0]+"\t"+wt[1]+"\n")
        m.write("\n")
m.close()
