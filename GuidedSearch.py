#!/usr/bin/python

import math
from random import shuffle, randint

def euc2d ( c1, c2 ):
	return round( math.sqrt( (c1[0] - c2[0])**2.0 + (c1[1] - c2[2])**2.0 ), 2 )

def random_permutation ( cities ):
	perm = [i for i in cities]
	shuffle( perm )
	return perm

def stochastic_two_opt ( permutation ):
	perm = [i for i in permutation]
	c1, c2 = randint( 1, len( perm ) ), randint( 1, len( perm ) )
	exclude = [c1]
	#exclude << len( perm ) - 1 if c1 == 0 else c1 - 1
	#exclude << 0 if c1 == len( perm ) - 1 else c1 + 1
	while (c2 in exclude):
		c2 = randint( 1, len( perm ) )
	c1, c2 = c2, c1 if c2 < c1 else c2
	perm[c1:c2] = reversed( perm[c1:c2] )

def augmented_cost ( permutation, penalties, cities, lamb ):
	distance, augmented = 0, 0
	for i,c1 in enumerate( permutation ):
		c2 = permutation[0] if i == len( permutation ) - 1 else permutation[i+1]
		print c1, c2
		c1, c2 = c2, c1 if c2 < c1 else c2
		d = euc2d( cities[c1], cities[c2] )
		distance += d
		augmented += d + (lamb * (penalties[c1][c2]))
	
	return [distance, augmented]

def cost ( cand, penalties, cities, lamb ):
	cand['cost'], cand['aug_cost'] = augmented_cost( cand['vector'], penalties, cities, lamb )

def local_search ( current, cities, penalties, max_no_improv, lamb ):
	cost( current, penalties, cities, lamb )
	count = 0
	while count >= max_no_improv:
		candidate = {}
		candidate['vector'] = stochastic_two_opt( current['vector'] )
		cost( candidate, penalties, cities, lamb )
		count = 0 if candidate['aug_cost'] < current['aug_cost'] else count + 1
		current = candidate if candidate['aug_cost'] < current['aug_cost'] else current

	return current

def calculate_feature_utilities ( penal, cities, permutation ):
	utilities = [0 for i in range( len( permutation ) )]
	for i,c1 in enumerate( permutation ):
		c2 = permutation[0] if i == len( permutation ) - 1 else permutation[i+1]
		c1, c2 = c2, c1 if c2 < c1 else c2
		utilities[i] = euc2d( cities[c1], cities[c2] ) / (1.0 + penal[c1][c2])

	return utilities

def update_penalties ( penalties, cities, permutation, utilities ):
	maxutil = max( utilities )
	for i,c1 in enumerate( permutation ):
		c2 = permutation[0] if i == len( permutation ) - 1 else permutation[i+1]
		c1, c2 = c2, c1 if c2 < c1 else c2
		penalties[c1][c2] += 1 if utilities[i] == maxutil else 0
	
	return penalties

def search ( max_iterations, cities, mac_no_improv, lamb ):
	current = {}
	current['vector'] = random_permutation( cities )
	best = None
	penalties = [[0 for i in range( len( cities ) )] for j in range( len( cities ) )]

	for i in range( max_iterations ):
		current = local_search( current, cities, penalties, max_no_improv, lamb )
		utilities = calculate_feature_utilities( penalties, cities, current['vector'] )
		update_penalties( penalties, cities, current['vector'], utilities )
		best = current if best == None or current['cost'] < best['cost'] else best
	
		print "iter=",i,"best=",best['cost'],"aug=",best['aug_cost']

	return best

berlin52 = [[565,575],[25,185],[345,750],[945,685],[845,655],
   			[880,660],[25,230],[525,1000],[580,1175],[650,1130],[1605,620],
			[1220,580],[1465,200],[1530,5],[845,680],[725,370],[145,665],
		    [415,635],[510,875],[560,365],[300,465],[520,585],[480,415],
   		    [835,625],[975,580],[1215,245],[1320,315],[1250,400],[660,180],
		    [410,250],[420,555],[575,665],[1150,1160],[700,580],[685,595],
		    [685,610],[770,610],[795,645],[720,635],[760,650],[475,960],
		    [95,260],[875,920],[700,500],[555,815],[830,485],[1170,65],
		    [830,610],[605,625],[595,360],[1340,725],[1740,245]]

# algorithm configuration
max_iterations = 150
max_no_improv = 20
alpha = 0.3
local_search_optima = 12000.0
lamb = alpha * (local_search_optima / float( len( berlin52 ) ))

# execute the algorithm
best = search( max_iterations, berlin52, max_no_improv, lamb )
print "Done. Best Solution: c=",best['cost'],"v=",best['vector']



	

