from reo import *

c1 = Connector()
c1.connect('Sync', 'A', 'M')
c1.connect('Fifo1', 'M', 'B')
c1.connect('Fifo1', 'M', 'C')


c2 = Connector()
c2.connect('Fifo1', 'A', 'N')
c2.connect('Sync', 'N', 'B')
c2.connect('Sync', 'N', 'C')

result, counterexample, smt = c2.isRefinementOf(c1, 10)

print(result)
