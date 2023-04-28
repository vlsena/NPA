import hopsy
import numpy as np

# A frunção recebe os valores das matrizes "A" e "b" que definem o espaço a ser sorteado; "d" é a dimensão do espaço. 

# Você também pode inserir uma "seed" em "rng = hopsy.RandomNumberGenerator()" da seguinte forma "seed=**". ** deve ser um número entre 42 e 46, isso alterará a configuração do sorteio

def sorteio(A,b,n_points): 
	# o problema completo é definido pela distribuição alvo
	# e pelo domínio restrito, definido pela desigualdade "Ax <= b"
	problem = hopsy.Problem(A, b)

	# the run object contains and constructs the markov chains. in the default case, the
	# Run object will have a single chain using the Hit-and-Run proposal algorithm and is
	# set to produce 10,000 samples.
	st_point = hopsy.compute_chebyshev_center(problem) # this function computes the Chebyshev center of the polytope and uses it one as a starting point
	mc = hopsy.MarkovChain(problem, proposal=hopsy.GaussianHitAndRunProposal, starting_point=st_point)
	rng = hopsy.RandomNumberGenerator()

	# call sample on the mc and rng objects 
	acceptance_rate, states = hopsy.sample(mc,rng, n_samples=n_points, thinning=2)
	
	
	return np.array(states)
