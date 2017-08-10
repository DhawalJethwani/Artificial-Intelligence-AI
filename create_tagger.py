import pickle

src="./../Text_Files/train.txt"

emission={}
transition={}
prior={}
sentence=0

with open(src,"r") as f:
	lastline=""
	for line in f:
		line=line.rstrip()
		lastline=lastline.rstrip()
		if len(line)!=0:
			l=line.split()
			ll=lastline.split()
			if len(lastline)==0:
				if l[1] in prior.keys():
					prior[l[1]]+=1
				else:
					prior[l[1]]=1
			else:
				if ll[1] not in transition.keys():
					transition[ll[1]]={}
				if l[1] in transition[ll[1]].keys():
					transition[ll[1]][l[1]]+=1
				else:
					transition[ll[1]][l[1]]=1
			if l[1] not in emission.keys():
				emission[l[1]]={}
			if l[0] in emission[l[1]].keys():
				emission[l[1]][l[0]]+=1
			else:
				emission[l[1]][l[0]]=1
		else:
			sentence+=1
		lastline=line

for i in prior.keys():
	prior[i]=float(prior[i])/sentence

for i in transition.keys():
	taga2b=0
	for j in transition[i].keys():
		taga2b+=transition[i][j]
	for j in transition[i].keys():
		transition[i][j]=float(transition[i][j])/float(taga2b)

for i in emission.keys():
	tag2tkn=0
	for j in emission[i].keys():
		tag2tkn+=emission[i][j]
	for j in emission[i].keys():
		emission[i][j]=float(emission[i][j])/float(tag2tkn)

pkl="./../Models/tagger.pkl"
pk=open(pkl,"wb")
pickle.dump(emission,pk)
pickle.dump(prior,pk)
pickle.dump(transition,pk)
pk.close()
