__author__ = 'nparslow'

import json

import numpy as np
import matplotlib.pyplot as plt

results = {}

with open("/home/nparslow/Documents/AutoCorrige/vocabulary/perl/vocd_longi_results.txt", 'r') as infile:
    results = json.load(infile)

print results


student2time2score = {}
for stud_time in results:
    stud, time = stud_time.split("_")
    if stud not in student2time2score: student2time2score[stud] = {}
    student2time2score[stud][time] = results[stud_time]





#x = np.arange(0, 5, 0.1);
#y = np.sin(x)
#plt.plot(x, y)

fig = plt.figure()


for student in student2time2score:
    xs = [x for x in ["1", "2", "3", "4"] if x in student2time2score[student]]
    ys = [student2time2score[student][x] for x in xs]
    print student, ys
    plt.plot(xs, ys)


plt.show()

#plt.boxplot([res_by_level[x] for x in ['A', 'B', 'C', 'D', 'E']])
#plt.show()