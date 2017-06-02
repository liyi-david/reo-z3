from reo import *

c1 = Connector()
c1.connect('Sync'     , 'A', 'D')
c1.connect('Sync'     , 'D', 'C')
c1.connect('Sync'     , 'B', 'E')
c1.connect('Sync'     , 'E', 'C')
c1.connect('SyncDrain', 'E', 'G')
c1.connect('SyncDrain', 'D', 'H')
c1.connect('Fifo1e'   , 'F', 'G')
c1.connect('Fifo1'    , 'G', 'H')
c1.connect('Sync'     , 'H', 'F')

c2 = Connector()
c2.connect('Sync'     , 'A', 'D')
c2.connect('Lossy'     , 'D', 'C')
c2.connect('Sync'     , 'B', 'E')
c2.connect('Lossy'     , 'E', 'C')
c2.connect('SyncDrain', 'E', 'G')
c2.connect('SyncDrain', 'D', 'H')
c2.connect('Fifo1e'   , 'F', 'G')
c2.connect('Fifo1'    , 'G', 'H')
c2.connect('Sync'     , 'H', 'F')

result1, counterexample1, smt1 = c2.isRefinementOf(c1, 5)
result2, counterexample2, smt2 = c1.isRefinementOf(c2, 5)

print(result1)
print(result2)