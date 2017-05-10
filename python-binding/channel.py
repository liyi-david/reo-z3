import sys

# sys.path.append("C://Users//xiyue//Source//Repos//z3//build//python")
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
    def Lossy1(nodes, idx, num, bound):
        assert len(nodes) == 2
        if bound == num:
            return True
        constraints_0 = []
        constraints_1 = []
        constraints_0 += [ nodes[0]['data'][idx] != nodes[1]['data'][num]]
        constraints_0 += [ nodes[0]['time'][idx] != nodes[1]['time'][num]]
        constraints_1 += [ nodes[0]['data'][idx] == nodes[1]['data'][num]]
        constraints_1 += [ nodes[0]['time'][idx] == nodes[1]['time'][num]]
        return Or(And(Merge(constraints_0), Lossy1(nodes, idx + 1, num, bound)),
                  And(Merge(constraints_1), Lossy1(nodes, idx + 1, num + 1, bound)))

    @staticmethod
    def SyncDrain(nodes, bound):
        assert len(nodes) == 2
        constraints = []
        for i in range(bound):
            constraints += [nodes[0]['time'][i] == nodes[1]['time'][i]]

        return Merge(constraints)
    
    @staticmethod
    def Merge1(nodes, bound):
        assert len(nodes) == 3
        if bound == idx_1 + idx_2:
            return True
        constraints_1 = []
        constraints_2 = []
        constraints_1 += [ nodes[0]['data'][idx_1] == nodes[2]['data'][idx_1 + idx_2]]
        constraints_1 += [ nodes[0]['time'][idx_1] == nodes[2]['time'][idx_1 + idx_2]]
        constraints_1 += [ nodes[0]['time'][idx_1] <  nodes[1]['time'][idx_2]]
        constraints_2 += [ nodes[1]['data'][idx_2] == nodes[2]['data'][idx_1 + idx_2]]
        constraints_2 += [ nodes[1]['time'][idx_2] == nodes[2]['time'][idx_1 + idx_2]]
        constraints_2 += [ nodes[1]['time'][idx_2] <  nodes[0]['time'][idx_1]]
        return Or(And(Merge(constraints_1), Merge1(nodes, idx_1 + 1, idx_2, bound)),
                  And(Merge(constraints_2), Merge1(nodes, idx_1, idx_2 + 1, bound)))
    
