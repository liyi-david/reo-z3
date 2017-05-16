from reo import *

sync = Connector()
sync.connect('Sync', 'A', 'B')

lossy = Connector()
lossy.connect('Lossy', 'A', 'B')

result, counterexample, smt = lossy.isRefinementOf(sync, 5)

print(result)
