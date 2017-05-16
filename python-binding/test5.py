from reo import *

c1 = Connector()
c1.connect('Sync'    , 'A', 'G')
c1.connect('Lossy'   , 'G', 'D')
c1.connect('Lossy'   , 'G', 'E')
c1.connect('SyncDrain', 'G', 'F')
c1.connect('Merger'   , 'D', 'E', 'F')
c1.connect('Sync'     , 'D', 'B')
c1.connect('Sync'     , 'E', 'C')

c2 = Connector()
c2.connect('Sync'     , 'A', 'G')
c2.connect('Sync'     , 'G', 'D')
c2.connect('Lossy'   , 'G', 'E')
c2.connect('SyncDrain', 'G', 'F')
c2.connect('Merger'   , 'D', 'E', 'F')
c2.connect('Sync'     , 'D', 'B')
c2.connect('Sync'     , 'E', 'C')

result1, counterexample1, smt1 = c2.isRefinementOf(c1, 5)
result2, counterexample2, smt2 = c1.isRefinementOf(c2, 5)

print(result1)
print(result2)