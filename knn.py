"""
To run the classifier:
python3 knn.py <# of neighbors> <training file name> <test file name>
"""

import bisect
import csv
import sys

def knn(kNeighbors, train, test):
    with open('result.csv', 'w', newline = '') as result:
        resultWriter = csv.writer(result)
        resultWriter.writerow(['ImageId', 'Label'])

        if kNeighbors <= 0:
            return

        labels = []

        for imageId, testNumber in enumerate(test, 1):
            nearestNeighbors = [[], []]
            nearestNeighborsCounts = {}

            for trainNumber in train:
                distance = 0

                for testPixel, trainPixel in zip(testNumber, trainNumber[1:]):
                    distance += (int(testPixel) - int(trainPixel))**2
                distance **= 0.5
                if len(nearestNeighbors[0]) < kNeighbors or distance < nearestNeighbors[1][-1]:
                    if len(nearestNeighbors[0]) == kNeighbors:
                        if nearestNeighborsCounts[nearestNeighbors[0][-1]] == 1:
                            nearestNeighborsCounts.pop(nearestNeighbors[0][-1])
                        else:
                            nearestNeighborsCounts[nearestNeighbors[0][-1]] -= 1
                        nearestNeighbors[0].pop()
                        nearestNeighbors[1].pop()
                    if trainNumber[0] in nearestNeighborsCounts:
                        nearestNeighborsCounts[trainNumber[0]] += 1
                    else:
                        nearestNeighborsCounts[trainNumber[0]] = 1

                    index = bisect.bisect_left(nearestNeighbors[1], distance)

                    nearestNeighbors[0].insert(index, trainNumber[0])
                    nearestNeighbors[1].insert(index, distance)

            maxLabelCount = [None, 0]

            while maxLabelCount[0] == None:
                for label, count in nearestNeighborsCounts.items():
                    if count > maxLabelCount[1]:
                        maxLabelCount = [label, count]
                    elif count == maxLabelCount[1]:
                        if nearestNeighborsCounts[nearestNeighbors[0][-1]] == 1:
                            nearestNeighborsCounts.pop(nearestNeighbors[0][-1])
                        else:
                            nearestNeighborsCounts[nearestNeighbors[0][-1]] -= 1
                        nearestNeighbors[0].pop()
                        nearestNeighbors[1].pop()
                        maxLabelCount = [None, 0]

                        break

            resultWriter.writerow([imageId, maxLabelCount[0]])
            print("Finished Image Id: ", imageId, flush = True)

def main():
    kNeighbors = int(sys.argv[1])
    trainFileName = sys.argv[2]
    testFileName = sys.argv[3]

    with open(trainFileName, 'r') as trainFile, open(testFileName, 'r') as testFile:
        trainReader = csv.reader(trainFile)
        testReader = csv.reader(testFile)

        trainList = list(trainReader)
        testList = list(testReader)
        
    knn(kNeighbors, trainList[1:], testList[1:])

if __name__ == '__main__':
    main()
