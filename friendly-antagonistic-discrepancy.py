text_file = open('self-interest_variant_discrepancies.txt', 'w')

def friendly_o_si1(x, S, o1, o2):
    if len(o1) - 1 >= x:
        return o1[x]
    o1 += ((x + 1) - len(o1))*[0]
    S = [i for i in S if i <= x] # valid subtraction set
    if S != []:
        all_moves = [friendly_o_si2(x - a, S, o1, o2) + a for a in S]
        v = max(all_moves)
        o1[x] = v
        return v
    else:
        o1[x] = 0
        return 0
    
def friendly_o_si2(x, S, o1, o2):
    if len(o2) - 1 >= x:
        return o2[x]
    o2 += ((x + 1) - len(o2))*[0]
    S = [i for i in S if i <= x] # valid subtraction set
    if S != []:
        S_prime = [a for a in S if friendly_o_si2(x - a, S, o1, o2) + a == friendly_o_si1(x, S, o1, o2)]
        a_prime = max(S_prime, key = lambda a: friendly_o_si1(x - a, S, o1, o2)) # argmax for friendly
        v = friendly_o_si1(x - a_prime, S, o1, o2)
        o2[x] = v
        return v
    else:
        o2[x] = 0
        return 0
    
def antagonistic_o_si1(x, S, o1, o2):
    if len(o1) - 1 >= x:
        return o1[x]
    o1 += ((x + 1) - len(o1))*[0]
    S = [i for i in S if i <= x] # valid subtraction set
    if S != []:
        all_moves = [antagonistic_o_si2(x - a, S, o1, o2) + a for a in S]
        v = max(all_moves)
        o1[x] = v
        return v
    else:
        o1[x] = 0
        return 0
    
def antagonistic_o_si2(x, S, o1, o2):
    if len(o2) - 1 >= x:
        return o2[x]
    o2 += ((x + 1) - len(o2))*[0]
    S = [i for i in S if i <= x] # valid subtraction set
    if S != []:
        S_prime = [a for a in S if antagonistic_o_si2(x - a, S, o1, o2) + a == antagonistic_o_si1(x, S, o1, o2)]
        a_prime = min(S_prime, key = lambda a: antagonistic_o_si1(x - a, S, o1, o2)) # argmin for antagonistic
        v = antagonistic_o_si1(x - a_prime, S, o1, o2)
        o2[x] = v
        return v
    else:
        o2[x] = 0
        return 0

def discrepancy(x, S, o1, o2, o1_1, o2_1):
    s = False
    friendly1 = friendly_o_si1(x, S, o1, o2)
    friendly2 = friendly_o_si2(x, S, o1_1, o2_1)
    antagonistic1 = antagonistic_o_si1(x, S, o1, o2) 
    antagonistic2 = antagonistic_o_si2(x, S, o1, o2)
    difference = (friendly1 - friendly2) - (antagonistic1 - antagonistic2)
    return difference != 0


def build_possible_discrepancy(S):
    k = int(min(S)/(max(S) - min(S)))
    return (k + 2)*min(S) + (k)*max(S)

# caching outcome function values
fo1 = []
fo2 = []
ao1 = []
ao2 = []

n = 50 # search space

# stores discrepancies and heap sizes where they occur
heap_breaks = [[0 for i in range(n)] for j in range(n)]
subtraction_sets = []

# actually filling in heap_breaks and subtraction_sets
for i in range(2, n):
    for j in range(i + 1, n):
        S = (i, j)
        fo1 = []
        fo2 = []
        ao1 = []
        ao2 = []
        max_x = build_possible_discrepancy(S)
        for x in range(0, max_x + 1):
            d = discrepancy(x, S, fo1, fo2, ao1, ao2)
            if d:
                heap_breaks[i][j] = x
                subtraction_sets.append(S)
                break

subtraction_sets.sort(key=lambda x: heap_breaks[x[0]][x[1]]) # sort subtraction sets according to size of heap

chunk = 30 # number of subdivisions of subtraction_sets (by size)
sorted_subtraction_sets = [[] for i in range((len(subtraction_sets) // chunk) + 1)]

for i in range(len(subtraction_sets)):
    S = subtraction_sets[i]
    sorted_subtraction_sets[i // chunk].append(S)

for Ss in sorted_subtraction_sets:
    text_file.write(str(Ss) + "\n")