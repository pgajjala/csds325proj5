import os
import csv
import time

def ping():
    with open('top-100.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                website = row[1]
                os.system("echo time start: "+ str(time.time()) + " >> ../raw_data/traceData.txt")
                os.system("traceroute " + website + " >> ../raw_data/traceData.txt")


starttime = time.time()
for i in range(100):
    print(i)
    ping()
    time.sleep(1)