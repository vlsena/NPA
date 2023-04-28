## Código para estimar o volume de do nível Q_N da
## hierarquia NPA para um dado número "n" de pontos

import hopsy
import numpy as np
from sorting import sorteio
from npateste import npatest
from tqdm import tqdm


'''
-------------------------------------------------------------------------
INPUT:
n: número de pontos a serem sorteados dentro do politopo não sinalizante
x: nível "p" da hierarquia NPA a ser analisado
y: nível "q" da hierarquia NPA a ser analisado
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

def estima_volume(n,x,y):

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
        dados = open(str(n)+"_pontos_em_Q1+AB_e_Q"+ str(y) + ".txt", "a")
        linhas = list()

        discrepantes = open('pontos_discrepantes.txt', 'a')
        ############################################################


        optimal = npatest(np.zeros(8),1)
        cx = 0
        cy = 0

        for i in tqdm(range(len(A0))):

            P = np.array([A0[i],A1[i],B0[i],B1[i],A0B0[i],A0B1[i],A1B0[i],A1B1[i]]) # pega cada ponto

            if npatest(P,x) == optimal: cx += 1 # e analiza se está no nível x da hierarquia NPA
            if npatest(P,y) == optimal: cy += 1 # e analiza se está no nível y da hierarquia NPA
            if npatest(P,x) != npatest(P,y):
                discrepantes.write(str(A0[i]) + ' ' + str(A1[i]) + ' ' + str(B0[i]) + ' ' + str(B1[i])+ ' ' + str(A0B0[i]) + ' ' + str(A0B1[i]) + ' ' + str(A1B0[i]) + ' ' + str(A1B1[i]) +  ' Q' + str(x) + ':' + npatest(P,x) + ' Q' + str(y) + ':' + npatest(P,y) +  ' \n')
            else: pass


            linhas.append(str(A0[i]) + ' ' + str(A1[i]) + ' ' + str(B0[i]) + ' ' + str(B1[i])+ ' ' + str(A0B0[i]) + ' ' + str(A0B1[i]) + ' ' + str(A1B0[i]) + ' ' + str(A1B1[i]) +  ' ' + npatest(P,x) + ' ' + npatest(P,y) +  ' \n') # armazenamento de dados



        dados.writelines(linhas)  # armazenamento de dados 

        #print(linhas)

        print('Q' + str(x),100*(cx/len(A0)))
        print('Q' + str(y),100*(cy/len(A0)))

        resultadox = 100*(cx/len(A0))
        resultadoy = 100*(cy/len(A0))

        dados.write('stop')
        dados.write('\n')
        dados.write('O conjunto Q' + str(x) + ' da hierarquia NPA corresponde a ' + str(resultadox)+'%' + ' do politopo não-sinalizante no cenário (2,2,2) \n')
        dados.write('O conjunto Q' + str(y) + ' da hierarquia NPA corresponde a ' + str(resultadoy)+'%' + ' do politopo não-sinalizante no cenário (2,2,2)')

