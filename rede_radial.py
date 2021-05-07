import numpy as np, math, time, os, datetime, matplotlib.pyplot as plt
import pandas as pd


inicio = time.time()


def fasor(R, theta):

    Re = R*math.cos(theta*math.pi/180)
    Im = R*math.sin(theta**math.pi/180)
    Z = complex(Re, Im)
    return Z


def forward_sweep( barras, linhas, Vbus, a0, a1, a2, b0, b1, b2, f ):

 NB = len(barras)
 Nbr = len(linhas)
 cam_max = max(barras[:,1]) #camada mais profunda
 SL = np.zeros(NB)*complex(0,0)
 Sbr = np.zeros(Nbr)*complex(0,0)
 Sloss = np.zeros(NB)*complex(0,0)
 
 
 for c in range(cam_max, 0, -1):# da camada mais profunda até a superior
   
     for i in range(0,NB):#procurando barras ligadas na camada C
   
      if( int(barras[i,1]) == c ):
        
        SL[i] = 1000*carga_zip_freq(barras[i,2], barras[i,3], abs(Vbus[i]), abs(V_SE), a0, a1, a2, b0, b1, b2, f, kp)
        #SL[i] = 1000*complex(barras[i,2], barras[i,3])#carga da barra
        bus = int(barras[i,0])
        
        for j in range(0, Nbr):# procurando barras a montante
        
          if( linhas[j,2] == bus ):
          
            bus_up = int(linhas[j,1])
            branch = int(linhas[j,0])
            Sloss[i] = (math.pow( abs(SL[i]) / abs(Vbus[i]), 2))*complex( linhas[branch,3], linhas[branch,4]) 
            Sbr[branch] = SL[i] + Sloss[i]#fluxo no ramo = carga da barra + perda no ramo

            for k in range( 0, Nbr ):# procurando barras a jusante
            
              if( int(linhas[k,1]) == bus):
              
               bus_down = int(linhas[k,2])
               branch_down = int(linhas[k,0])
               Sbr[branch] = Sbr[branch] + Sbr[branch_down]
 return Sbr


def backward_sweep( V_SE, barras, linhas, Sbr ):

 NB = len(barras)
 Nbr = len(linhas)
 cam_max = max(barras[:,1]) #camada mais profunda
 Vbus = V_SE*np.ones(NB)
 Vbus[0] = V_SE

 for c in range(0,cam_max):# da camada superior até a mais profunda
 
    for i in range(0,NB):#procurando barras ligadas na camada C
    
      if( barras[i,1] == c ):
      
        bus = int(barras[i,0])
        
        for j in range(0,Nbr):# procurando barras a jusante
        
          if( linhas[j,1] == bus ):
          
            bus_down = int(linhas[j,2])
            Vbus[bus_down] = Vbus[bus] - complex( linhas[j,3], linhas[j,4] ) * complex.conjugate( Sbr[j] / Vbus[bus] )
 return Vbus


def sum_power( Vbus_old, TOL, max_iter, barras, linhas, a0, a1, a2, b0, b1, b2, f, kp ):
    
    Sbr = forward_sweep( barras, linhas, Vbus_old, a0, a1, a2, b0, b1, b2, f )
    Vbus = backward_sweep( V_SE, barras, linhas, Sbr )
    error = max( abs( abs(Vbus) - abs(Vbus_old) ) )
    iter = 0
    #print('                    Processamento                       ')
    #print('                                                        ')
    #print('Tolerância admitida:', TOL)
    #print('')
    #print('iteração           erro')
    #print(iter,                 error)
    while( error >= TOL):
        
        Vbus_old = Vbus
        Sbr = forward_sweep( barras, linhas, Vbus_old, a0, a1, a2, b0, b1, b2, f )
        Vbus = backward_sweep( V_SE, barras, linhas, Sbr )
        error = max(abs( abs(Vbus) - abs(Vbus_old) ))
        iter = iter + 1
        #print(iter,                 error) #Eu removi

    return Vbus, Sbr, iter, error   

def carga_zip(Pnom, Qnom, V, Vnom, a0, a1, a2, b0, b1, b2):
    P = Pnom * ( a0 + a1*(V/Vnom) + a2*math.pow( (V/Vnom), 2 ) )
    Q = Qnom * ( b0 + b1*(V/Vnom) + b2*math.pow( (V/Vnom), 2 ) )
    S = complex(P,Q)
    return S

def carga_zip_freq(Pnom, Qnom, V, Vnom, a0, a1, a2, b0, b1, b2, f, kp):
    P = Pnom * ( a0 + a1*(V/Vnom) + a2*math.pow( (V/Vnom), 2 ) )
    Q = Qnom * ( b0 + b1*(V/Vnom) + b2*math.pow( (V/Vnom), 2 ) )
    kf = ( 1 + kp*( f-60 )/60 )
    S = 0.7*complex(P,Q) + 0.3*complex(P,Q)*kf
    return S


def monta_ybus(barras,linhas):
    NB = len(barras)
    Nbr = len(linhas)
    s = (NB,NB)
    Ybus = np.zeros(s)*complex(0,0)

    #Fora da diagonal principal
    for i in range(0,Nbr-1):
        Ybus[ int(linhas[i][1]) ][ int(linhas[i][2]) ] = 1/complex( linhas[i][3], linhas[i][4] )
        Ybus[ int(linhas[i][2]) ][ int(linhas[i][1]) ] = Ybus[ int(linhas[i][1]) ][ int(linhas[i][2]) ]


    #Na diagonal principal
    for m in range( 0,NB):
        for n in range(0, Nbr):
            if int(linhas[n][1]) == m:
                Ybus[m][m] = Ybus[m][m] + (1/complex( linhas[n][3], linhas[n][4] ) ) + linhas[n][5]
            elif int(linhas[n][2]) == m:
                Ybus[m][m] = Ybus[m][m] + (1/complex( linhas[n][3], linhas[n][4] ) ) + linhas[n][5]
        
    return Ybus        



def loop_freq( t0, tf, t_start, t_end, h ):

  n = int((tf - t0)/h)
  t = np.zeros(n)
  f = np.ones(n)*60
    
  for i in range(0,n-1):
	
    t[i+1] = t[i] + h
	    
    if( t[i] >= 0 and t[i] < 2 ):
		
	    f[i] = 60
		
    elif( t[i] >= 2 and t[i] < 4 ):
		
	    f[i] = -0.81*t[i] + 61.62#0.81*t[i] + 58.37
		
    elif( t[i] >= 4 and t[i] < 16 ):
		
	    f[i] = 58.38#61.62#
		
    elif( t[i] >= 16 and t[i] < 18 ):
		
        f[i] = 0.81*t[i] + 45.42#-0.81*t[i] + 74.58#
		
    elif( t[i] >= 18 and t[i] <= 20 ):
		
        f[i] = 60
		
	
  return t, f
	
# Leitura dos dados salvos em excel
barras = np.array(pd.read_excel("barras.xlsx", index_col=0))
linhas = np.array(pd.read_excel("linhas.xlsx", index_col=0))


V_SE = fasor(12660,0)
Vbus_old = V_SE * np.ones(len(barras))
TOL = 0.001 * 12660
max_iter = 50
a0 = 0 
a1 = 0.22
a2 = 0.78
b0 = 1
b1 = 0
b2 = 0
f_at = 58
kp = 0.9
t0= 0

tf = 20
t_start = 3
t_end = 6
h = 0.01
#f_af
#Processamento 
[t, f] = loop_freq( t0, tf, t_start, t_end, h )
Vbus_t = np.zeros((len(barras),len(t)))*complex(0,0)
Sbr_t  = np.zeros((len(linhas),len(t)))*complex(0,0)

for j in range(0, len(t)):
    
    [Vbus, Sbr, iter, error] = sum_power( Vbus_old, TOL, max_iter, barras, linhas, a0, a1, a2, b0, b1, b2, f[j], kp )
    	
    for i in range(0, len(barras)):
       Vbus_t[i][j] = Vbus[i]
		    	
    for k in range(0, len(linhas)):
       Sbr_t[k][j] = Sbr[k]

    	
#Saída
#print('')
#print('Iterações necessárias para a convergência:', iter )

tempo = time.time() - inicio
print('Duração: %s segundos' %round(tempo, 3))

print('')
#print('                     Tensões nas barras                           ' )
#print('')
#print('Barra                             V[pu]')
#for i in range(0,len(barras)):
#    print( i,            abs(Vbus[i])/abs(V_SE) )
    
#print('')
#print('                     Potência ativa nos ramos                           ' )
#print('')
#print('De  Para                             P[kW]')
#for i in range(0,len(linhas)):
#    print( linhas[i,1], linhas[i,2],           Sbr[i].real/1000 )
    
#print('')
#print('                     Potência reativa nos ramos                           ' )
#print('')
#print('De  Para                             Q[kvar]')
#for i in range(0,len(linhas)):
#    print( linhas[i,1], linhas[i,2],           Sbr[i].imag/1000 )

now = datetime.datetime.now().strftime(r"%d-%b-%y_%H:%M:%S")
if not os.path.isdir("./imagens"):
    os.mkdir("./imagens/")
pathname = f"./imagens/{now}/"
os.mkdir(pathname)

plt.figure()
#plt.subplot(211)
plt.plot(t, f, 'b-')
plt.xlabel('t[s]')
plt.ylabel('frequência [Hz]')
plt.grid(True)
plt.savefig(f"{pathname}f.png")

plt.figure()
#plt.subplot(212)
plt.plot(t, abs(Vbus_t[31,:])/12660, 'r:')
plt.xlabel('t[s]')
plt.ylabel('V [pu]')
plt.grid(True)
plt.savefig(f"{pathname}Vbus_t.png")


#plt.subplots_adjust(left=0.125,
#                    bottom=0.1, 
#                    right=0.9, 
#                    top=0.9, 
#                    wspace=0.2, 
#                    hspace=0.35)

plt.figure()
#plt.subplot(212)
plt.plot(t, (Sbr_t[0,:]).real/1000, 'g--')
plt.xlabel('t[s]')
plt.ylabel('P [kW]')
plt.grid(True)
plt.ylim([3000, 3500])
plt.savefig(f"{pathname}Sbr_t.png")


#plt.show()