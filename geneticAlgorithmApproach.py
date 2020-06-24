import math
import random
from permutationApproach import totalDistance

popSize = 500
bestYet = -1

def createOrder(numCities):
    order = []
    indices = list(range(numCities))
    for i in range(numCities):
        index = random.choice(indices)
        order.append(index)
        indices.remove(index)
    return order

def calculateFitness(cities, population, domain, yRange):
    currentBest = domain ** 2 + yRange ** 2
    bestOrder = population[0]
    fitnessList = []

    for i in range(len(population)):
        d = totalDistance(population[i], cities)

        if d < currentBest:
            currentBest = d
            bestOrder = population[i][:]

        fitnessList.append(scoreFitness(d))
    return fitnessList, bestOrder, currentBest


def normalizeFitness(fitnessList):
    totalFitness = sum(fitnessList)

    for i in range(len(fitnessList)):
        fitnessList[i] = fitnessList[i] / totalFitness


def scoreFitness(distance):
    return 1 / (pow(distance, 8) + 1)

def nextGeenration(fitnessList, population):
    newPopulation = []
    for i in range(popSize):
        order1 = chooseOrder(fitnessList, population)
        order2 = chooseOrder(fitnessList, population)
        order = crossOver(order1, order2)
        newPopulation.append(order)
    return newPopulation

def chooseOrder(fitnessList, population):
    spot = random.random()
    index = 0

    while spot > 0:
        spot -= fitnessList[index]
        index += 1
    index -= 1
    return population[index]

def unique(arr):
    d = dict()
    missing = []
    for i in range(len(arr)):
        d[i] = 0

    for i in arr:
        d[i] += 1

    for key in d.keys():
        if d[key] == 0:
            missing.append(key)

    missingCount = 0
    for i in range(len(arr)):
        if d[arr[i]] > 1:
            d[arr[i]] -= 1
            arr[i] = missing[missingCount]
            d[arr[i]] += 1
            missingCount += 1

    return arr

def crossOver(order1, order2):
    halfIndex = random.randint(0, len(order1) - 1)
    newOrder = []

    for i in range(halfIndex):
        newOrder.append(order1[i])

    for j in range(halfIndex, len(order2)):
        newOrder.append(order2[j])

    unique(newOrder)

    return newOrder

def bestOrder(cities, numGenerations):
    numCities = len(cities)
    population = [createOrder(numCities) for i in range(popSize)]
    fitnessList, recordOrder, recordDistance = calculateFitness(cities, population, 10000, 10000)

    count = 0
    while count < numGenerations:
        normalizeFitness(fitnessList)
        population = nextGeenration(fitnessList, population)

        fitnessList, bestOrder, bestDistance = calculateFitness(cities, population, 10000, 10000)

        if bestDistance < recordDistance:
            recordDistance = bestDistance
            recordOrder = bestOrder[:]

        count += 1

    return recordOrder

# def swap(arr, index1, index2):
#    val = arr[index1]
#    arr[index1] = arr[index2]
#    arr[index2] = val

# def mutate(order, rate):
#    for i in range(10):
#        if random.random() < rate:
#            index1 = random.randint(0, len(order) - 1)
#            index2 = (index1 + 1) % len(order)
#            print(index1, index2)
#            swap(order, index1, index2)
#    return order



