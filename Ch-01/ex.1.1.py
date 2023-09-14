import math

a = [4, 3]
b = [5, 5]
c = [1, 10]


def length(vector: list):
    sq_len = 0
    for i in range(0, len(vector)):
        sq_len += math.pow(vector[i], 2)
    return math.sqrt(sq_len)


def dot_product(vector1: list, vector2: list):
    if len(vector1) != len(vector2):
        return "Unmatching dimensionality"
    result = 0
    for i in range(0, len(vector1)):
        result += vector1[i] * vector2[i]
    return result


cos_a_b = dot_product(a, b) / (length(a) * length(b))
print("cos(a,b):", cos_a_b)

cos_a_c = dot_product(a, c) / (length(a) * length(c))
print("cos(a,c):", cos_a_c)

cos_b_c = dot_product(b, c) / (length(b) * length(c))
print("cos(b,c):", cos_b_c)
