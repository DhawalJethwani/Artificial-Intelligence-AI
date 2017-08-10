import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report

src="./../Text_Files/testAns.txt"
dest="./../Text_Files/predicted_tags.txt"

tags = set()
predicted_tags = []
actual_tags = []

with open(src,"r") as f1, open(dest,"r") as f2:
	for line in (l.rstrip() for l in f1):
		if len(line):
			actual_tags.append(line.split()[1])
			tags.add(line.split()[1])
	for line in (l.rstrip() for l in f2):
		if len(line):
			predicted_tags.append(line.split()[1])

tags = sorted(list(tags))
predicted_tags = np.array(predicted_tags)
actual_tags = np.array(actual_tags)

simple_conf_matrix = confusion_matrix(actual_tags,predicted_tags)

conf_matrix = pd.DataFrame(columns = tags, index = tags)


for x,y in zip(simple_conf_matrix,tags):
	conf_matrix[y] = x

print conf_matrix
print "\n   Classification Report: \n" + classification_report(actual_tags,predicted_tags)

f1.close()
f2.close()
