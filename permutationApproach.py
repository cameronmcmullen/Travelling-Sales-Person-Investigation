import math

def bestPermutation(cities):
    ordering = list(range(len(cities)))
    recordDistance = totalDistance(ordering, cities)
    bestOrder = ordering[:]

    while True:
        # Find largest i such that p[i] < p[i + 1]
        largest_i = -1
        for i in range(len(ordering) - 1):
            if ordering[i] < ordering[i + 1]:
                largest_i = i

        if largest_i == -1:
            break

        # Find largest j such that p[i] < p[j]
        largest_j = 0
        for j in range(len(ordering)):
             if ordering[largest_i] < ordering[j]:
                 largest_j  = j

        # Swap p[largest_i] and p[largest_j]
        pj = ordering[largest_j]
        ordering[largest_j] = ordering[largest_i]
        ordering[largest_i] = pj

        # Reverse P[largest_i + 1 ... n]
        ordering = ordering[:largest_i + 1] + list(reversed(ordering[largest_i + 1:]))

        currDist = totalDistance(ordering, cities)
        if currDist < recordDistance:
            recordDistance = currDist
            bestOrder = ordering[:]

    return bestOrder

# order = list(range(10))
# bestPermutation(order)

def totalDistance(ord, cities):
    # make the list of coordinates of each city
    coordinates = [cities[index].center for index in ord]

    # get distance between each city using the ordering
    dist = 0
    for i in range(len(ord) - 1):
        dist += distance(coordinates[i], coordinates[i + 1])
    return dist

def distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)
