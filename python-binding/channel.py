import sys

#sys.path.append("C://Users//xiyue//Source//Repos//z3//build//python")
from z3 import *

def Merge(constraints):
    assert len(constraints) > 0

    result = None
    for c in constraints:
        if result is None:
            result = c
        else:
            result = And(result, c)

    return result

def Lossy_seq(index, bound):
    seq = []
    temp = index
    for i in range(bound):
        seq.append(temp % 2)
        temp = (temp - (temp % 2)) / 2
        
    return seq

class Channel:
    @staticmethod
    def Sync(nodes, bound):
        assert len(nodes) == 2
        constraints = []
        for i in range(bound):
            constraints += [ nodes[0]['data'][i] == nodes[1]['data'][i] ]
            constraints += [ nodes[0]['time'][i] == nodes[1]['time'][i] ]

        return Merge(constraints)

    @staticmethod
    def Fifo1(nodes, bound):
        assert len(nodes) == 2
        constraints = []
        for i in range(bound):
            constraints += [ nodes[0]['data'][i] == nodes[1]['data'][i] ]
            constraints += [ nodes[0]['time'][i] <  nodes[1]['time'][i] ]
            if i:
                constraints += [ nodes[0]['time'][i] > nodes[1]['time'][i-1] ]

        return Merge(constraints)
    
    @staticmethod
    def Lossy(nodes, bound):
        assert len(nodes) == 2
        result = None
        for i in range(2**bound):
            constraints = []
            seq_lossy   = Lossy_seq(i, bound)
            num_index   = 0
            for j in range(bound):
                if seq_lossy[j]:
                    constraints += [ nodes[0]['data'][j] == nodes[1]['data'][num_index] ]
                    constraints += [ nodes[0]['time'][j] == nodes[1]['time'][num_index] ]
                    num_index   += 1
            if result is None:
                result = Merge(constraints)
            else:
                result = Or(result, Merge(constraints))
        
        return result
    
    @staticmethod
    def Merge1(nodes, bound):
        assert len(nodes) == 3
        constraints = []
        
        for i in range(bound):
            
