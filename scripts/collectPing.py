import os
import csv
import time

def ping():
    with open('top-100.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                website = row[1]
                os.system("echo time start: "+ str(time.time()) + " >> ../raw_data/pingData.txt")
                os.system("ping -c 5 " + website + "  >> ../raw_data/pingData.txt")


starttime = time.time()
for i in range(100):
    print(i)
    ping()
    time.sleep(1)