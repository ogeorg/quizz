from PriorityList.QuadraticList import QuadraticList
# import PriorityList.QuadraticList

list = QuadraticList()
list.insert(10, "abc10")
list.insert(2, "abc2")
list.insert(2, "def2")
list.insert(1, "abc1")
list.insert(1, "abc1b")
list.insert(10, "abc10")
list.insert(2, "abc2")
list.insert(2, "def2")
list.insert(1, "abc1")
list.insert(1, "abc1b")
list.insert(10, "abc10")

print len(list)
print list

r = list.get_random_index()

list.lower_index(0)
print list

list.lower_index(0)
print list

list.lower_index(4)
print list

list.rotate_index(0)
print list

size = len(list)
counts = []
for i in range(size):
    counts.append(0)

SAMPLES = 100000
for i in range(SAMPLES):
    r = list.get_random_index()
    counts[r] += 1
    
for i in range(size):
    print "%d : %f" % (i, float(counts[i]) / SAMPLES)

print "END"