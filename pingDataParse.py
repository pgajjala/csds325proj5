# importing the required module
import statistics

CHUNK_SIZE = 4098

ipAddressDict = {}
delayDict = {}
averageDelayDict ={}


def readFile(stream, separator):
  buffer = ''
  while True: 
    chunk = stream.read(CHUNK_SIZE) 
    if not chunk:
      yield buffer
      break
    buffer += chunk
    while True:
      try:
        part, buffer = buffer.split(separator, 1)
      except ValueError:
        break
      else:
        yield part

def findPings(pingDataFile):
    for ping in readFile(pingDataFile, separator='time start: '):
        if ping.find("PING ") != -1:
            startTime, remaining = ping.split("PING ", 1)
            application, ip, remaining = remaining.split(' ', 2)
            ipAddressDict[application] = ip[1:-1]
            remaining, stats = remaining.split('---', 1)
            delayArray = []
            
            while remaining.find("\n") != -1:
                currResponse,remaining = remaining.split("\n", 1)
                if currResponse.find(" time=") != -1:
                    currResponse,time = currResponse.split(" time=", 1)
                    delayArray.append(float(time[:-3]))

            if application in delayDict:
                delayDict[application] += delayArray
            else:
                delayDict[application] = delayArray           

def parseDelays():
    for website in delayDict.keys():
        if len(delayDict[website]) > 0 :
            print(website + "," + str(statistics.mean(delayDict[website])) + "," + str(statistics.stdev(delayDict[website])))
        else:
            print(website + ",0,0")

pingDataFile = open('../raw_data/pingData.txt')
findPings(pingDataFile)
parseDelays()
