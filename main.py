from QuizzReader import QuizzReader
from PriorityList.QuadraticList import QuadraticList

reader = QuizzReader()
reader.read("data/quizz1.xml")

list = QuadraticList()

for q in reader.q_list:
    list.insert(5, q)

print len(list)
print list.get_priorities_statistics()

while True:
    pos = list.get_random_index()
    q = list.get_value(pos)
    ans = raw_input("%s > " % q.question)

    if ans == ".": 
        break
    elif ans.lower() == q.answer.lower():
        print "Correct"
        list.raise_index(pos)
    else:
        print "Wrong, answer is %s" % q.answer
        list.lower_index(pos)
        
    print list.get_priorities_statistics()
        
        
        