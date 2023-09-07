import math

query = [1, 1]
doc1 = [3, 5]
doc2 = [4, 1]

sq_length1 = 0
sq_length2 = 0

for index in range(0, len(query)):
    sq_length1 += math.pow((doc1[index] - query[index]), 2)

for index in range(0, len(query)):
    sq_length2 += math.pow((doc2[index] - query[index]), 2)

print("1: ", math.sqrt(sq_length1))
print("2: ", math.sqrt(sq_length2))
