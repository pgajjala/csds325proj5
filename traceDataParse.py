# importing the required module
import statistics
import ipaddress

CHUNK_SIZE = 4098

numHopsDict = {}
ipAddressDelayDict = {}
hopDepthDict = {}
ipAddressDepthDict = {}
websiteDelayDict = {}
delays = []

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

def findNumHops(pingDataFile):
    for ping in readFile(pingDataFile, separator='time start: '):
        if ping.find("traceroute to ") != -1:
            startTime, remaining = ping.split("traceroute to ", 1)
            application, remaining = remaining.split(' ', 1)
            discard,remaining = remaining.split("\n", 1)
            count = 0
            while remaining.find("\n") != -1:
                count += 1
                discard,remaining = remaining.split("\n", 1)

            if application in numHopsDict:
                numHopsDict[application].append(count)
            else:
                numHopsDict[application] = [count]     

def findHopDelays(pingDataFile):
    for ping in readFile(pingDataFile, separator='time start: '):
        if ping.find("traceroute to ") != -1:
            startTime, remaining = ping.split("traceroute to ", 1)
            application, remaining = remaining.split(' ', 1)
            traceInfo,remaining = remaining.split("\n", 1)
            count = 0
            while remaining.find("\n") != -1:
                count += 1
                line,remaining = remaining.split("\n", 1)
                discard, line = line.split("  ", 1)
                while line.find("  ") != -1:
                    curr, line = line.split("  ", 1)
                    while curr[0] == "*": #ignore hidden hops
                        discard, curr = curr.split(" ", 1)
                    if curr.find(" ms") != -1: #contains a time measurement
                        time, curr = curr.split(" ", 1)
                        delays.append(float(time))
                        if currIp in ipAddressDelayDict:
                            ipAddressDelayDict[currIp].append(float(time))
                        else:
                            ipAddressDelayDict[currIp] = [float(time)]

                        
                        if application in websiteDelayDict:
                            websiteDelayDict[application].append(float(time))
                        else:
                            websiteDelayDict[application] = [float(time)]

                        if count in hopDepthDict:
                            hopDepthDict[count].append(float(time))
                        else:
                            hopDepthDict[count] = [float(time)]

                        if currIp in ipAddressDepthDict:
                            ipAddressDepthDict[currIp].append(count)
                        else:
                            ipAddressDepthDict[currIp] = [count]

                        if curr != "ms":
                            if curr == "ms *" or curr == "ms !X" or curr == "ms !Z": #ignore hidden hops
                                continue
                            discard, address, ip = curr.split(" ", 2)
                            currIp = ip[1:-1]
                    else: #does not contain a time measurement
                        address, ip = curr.split(" ", 1)
                        currIp = ip[1:-1]
                        
def parseNumHops():
    for website in numHopsDict.keys():
        if len(numHopsDict[website]) > 0 :
            print(website + "," + str(statistics.mean(numHopsDict[website])) + "," + str(statistics.stdev(numHopsDict[website])))
        else:
            print(website + ",0,0")

def parseHopDepth():
    for depth in hopDepthDict.keys():
        print(str(depth) + "," + str(statistics.mean(hopDepthDict[depth])) + "," + str(statistics.stdev(hopDepthDict[depth])))

def printDelays():
    for delay in delays:
        print(delay)

def parseDelayByIp():
    for ip in ipAddressDelayDict.keys():
        stdDevDelay = 0
        stdDevDepth = 0
        if len(ipAddressDelayDict[ip]) > 1:
            stdDevDelay = statistics.stdev(ipAddressDelayDict[ip])
            stdDevDepth = statistics.stdev(ipAddressDepthDict[ip])
        print(ip + "," + str(statistics.mean(ipAddressDelayDict[ip])) + "," + str(stdDevDelay) 
            + "," + str(statistics.mean(ipAddressDepthDict[ip])) + "," + str(stdDevDepth))

def parseDelayByWebsite():
    for website in websiteDelayDict.keys():
        stdDevDelay = 0
        if len(websiteDelayDict[website]) > 1:
            stdDevDelay = statistics.stdev(websiteDelayDict[website])
        print(website + "," + str(statistics.mean(websiteDelayDict[website])) + "," + str(stdDevDelay))


pingDataFile = open('../raw_data/traceData.txt')
findNumHops(pingDataFile)
findHopDelays(pingDataFile)
print("Enter desired analysis (a value between 2.2.2 and 2.2.6, detailed in report.pdf): ")
userInput = input()
if userInput == "2.2.2":
    parseNumHops()
elif userInput == "2.2.3":
    printDelays()
elif userInput == "2.2.4":
    parseDelayByWebsite()
elif userInput == "2.2.5":
    parseDelayByIp()
elif userInput == "2.2.6":
    parseHopDepth()
