#!/usr/bin/python
import random

def objectiveFn ( vec ):
  return sum( [x*x for x in vec] )

def randomVec( minmax ):
  return [(kv[0] + ((kv[1] - kv[0]) * random.random())) for i,kv in enumerate( minmax )];

def search( searchSpace, maxIter ):
  best = None
  for i in range( maxIter ):
    candidate = {} 
    candidate['vector'] = randomVec( searchSpace )
    candidate['cost'] = objectiveFn( candidate['vector'] )
    best = candidate if best == None or candidate['cost'] < best['cost'] else best
    print "iteration="+`i`, "best="+`best['cost']`
  return best;

best = search( [(-5,5) for x in range(2)], 100 )

print "Best Solution: c="+`best['cost']`, "v="+`best['vector']`
