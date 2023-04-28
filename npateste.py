import numpy as np
import ncpol2sdpa as nc

def npatest(p,level):

	Ax = np.array([p[0],p[1]])
	By = np.array([p[2],p[3]])

	AxBy = np.array([[p[4], p[5]],[p[6],p[7]]])	
	

	n_A = 2 # Observáveis dicotômicas da parte A
	n_B = 2 # Observáveis dicotômicas da parte B
	
	A = nc.generate_operators('A', n_A, hermitian=True)
	B = nc.generate_operators('B', n_B, hermitian=True)
	
	subs = {A[i] ** 2 :1 for i in range(n_A)} # Unitary
	subs.update({B[i] ** 2 :1 for i in range(n_B)}) # Unitary
	
	subs.update({A[i]*B[j]:B[j]*A[i] for i in range(n_A) for j in range(n_B)}) #Commutativity
	
	
	cons =[
		A[0]-Ax[0],
		A[1]-Ax[1],
		B[0]-By[0],
		B[1]-By[1],
		A[0]*B[0]-AxBy[0][0],
		A[0]*B[1]-AxBy[0][1],
		A[1]*B[0]-AxBy[1][0],
		A[1]*B[1]-AxBy[1][1],]
		
		
		
	sdp = nc.SdpRelaxation(A+B) # Monomio extra caso queira avaliar almost quantum (1 = 1+AB caso esta linha seja incluída)
	sdp.get_relaxation(level, objective=-0, substitutions=subs, momentequalities=cons)
	sdp.solve(solver='mosek')
	
	return sdp.status	
	

		
		
