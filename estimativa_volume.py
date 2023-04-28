## Código para estimar o volume de do nível Q_N da
## hierarquia NPA para um dado número "n" de pontos

import hopsy
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from sorting import sorteio
from npateste import npatest


'''
-------------------------------------------------------------------------
INPUT:
n: número de pontos a serem sorteados dentro do politopo não sinalizante
N: nível da hierarquia NPA
-------------------------------------------------------------------------

Este código sorteia "n" pontos dentro do politopo não-sinalizante e verifica quantos
estão dentro no conjunto Q_N da hierarquia NPA

-------------------------------------------------------------------------
OUTPUT:
* Um arquivo com o nome "dados_de_n_pontos_para_o_volume_de_Q_N.txt"
* Em cada linha, tem-se:
	+ Os pontos sorteados
	+ O status do ponto: 'optimal' para pertencente a Q_N e 'dual_ceas_infer' para não pertencente
	+ O volume de Q_N em relação ao politopo não-sinalizante
-------------------------------------------------------------------------
'''

def sorteio_em_NS(n,N):

	A = np.array([[-0.25, -0.  , -0.25, -0.  , -0.25, -0.  , -0.  , -0.  ],
	       [-0.25, -0.  ,  0.25, -0.  ,  0.25, -0.  , -0.  , -0.  ],
	       [ 0.25, -0.  , -0.25, -0.  ,  0.25, -0.  , -0.  , -0.  ],
	       [ 0.25, -0.  ,  0.25, -0.  , -0.25, -0.  , -0.  , -0.  ],
	       [-0.25, -0.  , -0.  , -0.25, -0.  , -0.25, -0.  , -0.  ],
	       [-0.25, -0.  , -0.  ,  0.25, -0.  ,  0.25, -0.  , -0.  ],
	       [ 0.25, -0.  , -0.  , -0.25, -0.  ,  0.25, -0.  , -0.  ],
	       [ 0.25, -0.  , -0.  ,  0.25, -0.  , -0.25, -0.  , -0.  ],
	       [-0.  , -0.25, -0.25, -0.  , -0.  , -0.  , -0.25, -0.  ],
	       [-0.  , -0.25,  0.25, -0.  , -0.  , -0.  ,  0.25, -0.  ],
	       [-0.  ,  0.25, -0.25, -0.  , -0.  , -0.  ,  0.25, -0.  ],
	       [-0.  ,  0.25,  0.25, -0.  , -0.  , -0.  , -0.25, -0.  ],
	       [-0.  , -0.25, -0.  , -0.25, -0.  , -0.  , -0.  , -0.25],
	       [-0.  , -0.25, -0.  ,  0.25, -0.  , -0.  , -0.  ,  0.25],
	       [-0.  ,  0.25, -0.  , -0.25, -0.  , -0.  , -0.  ,  0.25],
	       [-0.  ,  0.25, -0.  ,  0.25, -0.  , -0.  , -0.  , -0.25]])
	       

	b = (1/4)*np.array([[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1]])

	
	sorteio_NS = sorteio(A,b,n)


	A0 = sorteio_NS[0][:,0]
	A1 = sorteio_NS[0][:,1]
	B0 = sorteio_NS[0][:,2]
	B1 = sorteio_NS[0][:,3]
	A0B0 = sorteio_NS[0][:,4]
	A0B1 = sorteio_NS[0][:,5]
	A1B0 = sorteio_NS[0][:,6]
	A1B1 = sorteio_NS[0][:,7]

	############## Para armazenamento de dados #################    
	dados = open(str(n) + "_pontos_em_Q"+ str(N)+".txt", "a")
	linhas = list()
	############################################################


	optimal = npatest(np.zeros(8),1)
	c = 0
	 
	for i in range(len(A0)):

	    P = np.array([A0[i],A1[i],B0[i],B1[i],A0B0[i],A0B1[i],A1B0[i],A1B1[i]]) # pega cada ponto

	    if npatest(P,N) == optimal: c += 1 # e analiza se está no nível N da hierarquia NPA
	    else: continue   
	    
	    
	    linhas.append(str(A0[i]) + ' ' + str(A1[i]) + ' ' + str(B0[i]) + ' ' + str(B1[i])+ ' ' + str(A0B0[i]) + ' ' + str(A0B1[i]) + ' ' + str(A1B0[i]) + ' ' + str(A1B1[i]) +  ' ' + npatest(P,N) +  ' \n') # armazenamento de dados
	    
	    
	dados.writelines(linhas)  # armazenamento de dados 
	  
	print(100*(c/len(A0)))

	resultado = 100*(c/len(A0))

	dados.write('stop')
	dados.write('\n')
	dados.write('O conjunto Q' + str(N) + ' da hierarquia NPA corresponde a ' + str(resultado)+'%' + ' do politopo não-sinalizante no cenário (2,2,2)')
	
	return print('O conjunto Q' + str(N) + ' da hierarquia NPA corresponde a ' + str(resultado)+'%' + ' do politopo não-sinalizante no cenário (2,2,2)')

