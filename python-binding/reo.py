from z3 import *
from channel import *
from lib import *


class Connector:
    def __init__(self):
        self.channels = []

    def connect(self, channel, *nodes):
        self.channels += [(channel, nodes)]
        return self

    def isRefinementOf(self, abstraction, bound):
        assert isinstance(abstraction, Connector)
        nodes = {}

        solver = Solver()

        # step 1. generate variables for the refinement
        for chan in self.channels:
            # generate constraint for variables (if not existing)
            for nd in chan[1]:
                if nd not in nodes:
                    nodes[nd] = {
                        'time': [Real(nd + '_t_' + str(i)) for i in range(bound)],
                        'data': [Int(nd + '_d_' + str(i)) for i in range(bound)]
                        }

                    # generate time constraints
                    solver.add(nodes[nd]['time'][0] >= 0)
                    for i in range(bound - 1):
                        solver.add(nodes[nd]['time'][i] <= nodes[nd]['time'][i + 1])

            # generate constraint for channels
            channelDecl = eval('Channel.' + chan[0])
            paramnodes = map(lambda name: nodes[name], chan[1])
            solver.add(channelDecl(paramnodes, bound))


        # step 2. deal with the abstraction
        # create constants if needed
        for chan in abstraction.channels:
            foralls = []
            for nd in chan[1]:
                if nd not in nodes:
                    nodes[nd] = {
                        'time': [Const(nd + '_t_' + str(i), Int) for i in range(bound)],
                        'data': [Const(nd + '_d_' + str(i), Int) for i in range(bound)]
                        }

                    foralls += nodes[nd]['time']
                    foralls += nodes[nd]['data']

                    # generate time constraints
                    # TODO:

            # generate constraint for channels
            channelDecl = eval('Channel.' + chan[0])
            paramnodes = map(lambda name: nodes[name], chan[1])

            constr = Not(channelDecl(paramnodes, bound))
            if len(foralls) > 0:
                constr = ForAll(foralls, constr)

            solver.add(constr)


        result = solver.check()
        if str(result) == 'sat':
            return False, solver.model(), solver.to_smt2()
        else:
            return True, None, solver.to_smt2()
        pass


if __name__ == "__main__":
    sync = Connector()
    sync.connect('Sync', 'A', 'B')

    fifo1 = Connector()
    fifo1.connect('Sync', 'A', 'B')

    fifo1.isRefinementOf(sync, 10)
