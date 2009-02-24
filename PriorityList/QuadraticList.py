from PriorityList import PriorityList
import random

class QuadraticList(PriorityList):
    def __init__(self):
        PriorityList.__init__(self)
        
    def get_random_index(self):
        """
        Gets a random index
        """
        r = random.random()
        r = r * r * self.size
        r = int(r)
        return r
