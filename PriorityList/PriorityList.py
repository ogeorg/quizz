import random

class PriorityList:
    
    def __init__(self, min_level=0, max_level=9):
        self.size = 0
        self.values = {}
        self.min_level = min_level
        self.max_level = max_level
    
    def __len__(self):
        return self.size
    
    def insert(self, priority, value):
        """
        Inserts a value at certain priority
        """
        priority = self.constraint_priority(priority)
        if not self.values.has_key(priority):
            values_p = self.values[priority] = []
        else:
            values_p = self.values[priority]
            
        values_p.append(value)
        self.size += 1
    
    def remove_index(self, index):
        pass
    
    def get_random_index(self):
        """
        Gets a random index
        """
        r = random.randint(0, self.size - 1)
        return r

    def raise_index(self, index):
        """
        Moves the question to a lower priority
        """
        self.__raiselower_index(index, +1)
    
    def lower_index(self, index):
        self.__raiselower_index(index, -1)
    
    def rotate_index(self, index):
        self.__raiselower_index(index, 0)
    
    def __raiselower_index(self, index, delta):
        (priority, subindex) = self.get_priority_subindex(index)
        
        # remove from former location
        priority_list = self.values[priority]
        value = priority_list[subindex]
        del priority_list[subindex]
        if not priority_list:
            del self.values[priority]
        self.size -= 1
        
        # put into new location
        priority = self.constraint_priority(priority + delta)
        self.insert(priority, value)
    
    def constraint_priority(self, priority):
        if priority < self.min_level: 
            priority = self.min_level
        if priority > self.max_level: 
            priority = self.max_level
        return priority
    
    def get_priority_subindex(self, index):
        """
        Gets a pair (priority, subindex).
        
        subindex is the position of the index within the priority
        """
        if index >= self.size:
            raise IndexError()
                
        keys = self.values.keys()
        keys.sort()
        pi = 0
        for key in keys:
            values_p = self.values[key]
        # for values_p in self.values.itervalues():
            if pi + len(values_p) > index:
                return (key, index - pi)
            else:
                pi += len(values_p)
        
    def get_value(self, index):
        """
        Gets a value
        """
        (priority, subindex) = self.get_priority_subindex(index)
        return self.values[priority][subindex]
    
    def get_priorities_statistics(self):
        """
        Yields a list of priorities and their number of elements
        """
        res = {}
        for (key, list) in self.values.iteritems():
            res[key] = len(list)
        return res
    
    def get_priorities_statistics_str(self):
        """
        Yields a list of priorities and their number of elements (as a text
        
        """
        res = ""
        for (key, list) in self.values.iteritems():
            res += "%s: %d\n" % (key, len(list))
        return res
    
    def __str__(self):
        res = ""
        for (key, list) in self.values.iteritems():
            res += "-- %s --\n" % key
            values_p = self.values[key]
            res += ", ".join(values_p) + "\n"

        return res
        

if __name__ != "__main__":
    pass
