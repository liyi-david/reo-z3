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

        return Merge(constraints)
