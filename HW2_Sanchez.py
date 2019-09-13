import linecache

#open original input to get information
originalFile = open('inputFile.txt', 'r')

#creates a copy
modifiedFile = open('modifiedInput.txt', 'w')

#removes comment by ignoring lines that start with #
comment = '#'

for line in originalFile:
    if comment not in line:
        modifiedFile.write(line)

#close files
originalFile.close()
modifiedFile.close()

# number of fragments
cLine = 1
fragmentnumber = linecache.getline('modifiedInput.txt', cLine)
fragmentnumber = int(fragmentnumber, 4)

# query costs for each fragment,converted to float
cLine = 2
queryCost = linecache.getline('modifiedInput.txt', cLine)

queryCost = queryCost.split(", ")

i = 0
for value in queryCost:
    queryCost[i] = float(value)
    i = i + 1

#update costs
cLine = 3
updateCost = linecache.getline('modifiedInput.txt', cLine)

#converts value to float
updateCost = updateCost.split(", ")

i = 0
for value in updateCost:
    updateCost[i] = float(value)
    i = i + 1

#number of sites
cLine = 4
Sites = linecache.getline('modifiedInput.txt', cLine)
Sites = int(Sites, 10)
print("Number of sites: " + str(Sites))

#list for query probabilities
queryProb = []

cLine = 5
target = cLine + fragmentnumber

while cLine < target:
    queryProbLine = linecache.getline('modifiedInput.txt', cLine)
    queryProbLine = queryProbLine.split(", ")

    i = 0
    for value in queryProbLine:
        queryProbLine[i] = float(value)
        queryProb.append(queryProbLine[i])
        i = i + 1

    cLine = cLine + 1


#list for update probabilities
updateProb = []
target = cLine + fragmentnumber

while cLine < target:
    updateProbLine = linecache.getline('modifiedInput.txt', cLine)
    updateProbLine = updateProbLine.split(", ")

    i = 0
    for value in updateProbLine:
        updateProbLine[i] = float(value)
        updateProb.append(updateProbLine[i])
        i = i + 1

    cLine = cLine + 1


# query and update matrix
queryProb = [queryProb[i: i + Sites] for i in range(0, len(queryProb), Sites)]
updateProb = [updateProb[i: i + Sites] for i in range(0, len(updateProb), Sites)]


#computation cost
expectedCost = 0;
for fragment in range(fragmentnumber):
    print("\nComputing optimal allocation for fragment " + str(fragment))

    #combo check
    for i in range(0,  2  ** Sites ):
        i = bin(i)[2:].zfill(Sites)
        i = list(map(int, i))

        for site in range(0, Sites):

            writeCost = round((updateCost[fragment] * ( i[site] )* updateProb[fragment][site]),1)

            readCost = round((queryProb[fragment][site] * (1 - i[site]) * queryCost[fragment]),1)

            expectedCost = round((readCost + writeCost + expectedCost), 1)

        print("x = " + str(list(i)) + ", expected cost = " + str(expectedCost))
        expectedCost = 0

#print("Optimal replication = "+ min(str(list(i))) + ", min cost = " + min(str(expectedCost)))
