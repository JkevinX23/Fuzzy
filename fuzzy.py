import numpy as np 
import skfuzzy as fuzz
import matplotlib.pyplot as plt
def getfMax(rule3,rule5,rule6,rule8,rule9,emprest_hig):
    t1 = np.fmax(rule3,rule5)
    t2 = np.fmax(t1,rule6)
    t3 = np.fmax(t2,rule8)
    t4 = np.fmax(t3,rule9)
    t5 = np.fmin(t4,emprest_hig)
    return t5
'''
Emprestimos para negativados..

'''
x_saldoMedio = np.arange(-200, 1250, 1)
x_historicoPag = np.arange(-200, 1250, 1)
x_emprestimo  = np.arange(0, 100, 1)

saldo_low = fuzz.trapmf(x_saldoMedio, [-200,-200, -100, 0])
saldo_med = fuzz.trapmf(x_saldoMedio, [-100, 0, 500, 1000])
saldo_hig = fuzz.trapmf(x_saldoMedio, [500, 1000, 1250, 1250])

historic_low = fuzz.trapmf(x_historicoPag, [-200, -200 ,-100, 0])
historic_med = fuzz.trapmf(x_historicoPag, [-100, 0, 100, 500])
historic_hig = fuzz.trapmf(x_historicoPag, [100, 500, 1250,1250])

emprest_low = fuzz.trapmf(x_emprestimo, [0, 0, 0, 50])
emprest_med = fuzz.trapmf(x_emprestimo, [0, 50, 50, 100])
emprest_hig = fuzz.trapmf(x_emprestimo, [50, 100, 100, 100])

'''
REGRAS:::
SALDO LOW [IF  SALDO < (-100) ]
SALDO MED [IF  SALDO > -100 AND SALDO < 1000]
SALDO HIG [IF  SALDO > 1000]

HISTORIC LOW [<100]
HISTORIC MED [ >100 AND <500]
HISTORIC HIG [ >500]

EMPREST LOW [ NAO OFERECER ]
EMPREST MED [ OFERECER COM RESTIÇÃO ]
EMPREST HIG [ OFERECER ]

'''


# Visualize these universes and membership functions

fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

ax0.plot(x_saldoMedio, saldo_low, 'b', linewidth=1.5, label='Baixo')
ax0.plot(x_saldoMedio, saldo_med, 'g', linewidth=1.5, label='Neutro')
ax0.plot(x_saldoMedio, saldo_hig, 'r', linewidth=1.5, label='Alto')
ax0.set_title('Saldo médio dos últimos meses')
ax0.legend()


ax1.plot(x_historicoPag, historic_low, 'b', linewidth=1.5, label='Ruim pagador')
ax1.plot(x_historicoPag, historic_med, 'g', linewidth=1.5, label='Neutro')
ax1.plot(x_historicoPag, historic_hig, 'r', linewidth=1.5, label='Bom pagador')
ax1.set_title('Histórico de pagamento')
ax1.legend()


ax2.plot(x_emprestimo, emprest_low, 'b', linewidth=1.5, label='Baixo')
ax2.plot(x_emprestimo, emprest_med, 'g', linewidth=1.5, label='Parcial')
ax2.plot(x_emprestimo, emprest_hig, 'r', linewidth=1.5, label='Total')
ax2.set_title('Linha de crédito oferecida')
ax2.legend()
# Turn off top/right axes
for ax in (ax0, ax1, ax2):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
plt.tight_layout()
plt.show()

##########################################################################
user_saldo = 50
user_hist = -50
###########################################################################
value_saldo_low = fuzz.interp_membership(x_saldoMedio,saldo_low, user_saldo)
value_saldo_med = fuzz.interp_membership(x_saldoMedio,saldo_med, user_saldo)
value_saldo_hig = fuzz.interp_membership(x_saldoMedio,saldo_hig, user_saldo)

value_hist_low = fuzz.interp_membership(x_saldoMedio,historic_low, user_hist)
value_hist_med = fuzz.interp_membership(x_saldoMedio,historic_med, user_hist)
value_hist_hig = fuzz.interp_membership(x_saldoMedio,historic_hig, user_hist)
############################################################################
'''

1. IF SALDO_LOW && HISTORIC LOW    -EMPREST LOW
2. IF SALDO_LOW && HISTORIC MEDIUM -EMPREST LOW
3. IF SALDO_LOW && HISTORIC HIGH   -EMPREST HIGH

4. IF SALDO_MED && HISTORIC LOW    -EMPREST MED
5. IF SALDO_MED && HISTORIC MED    -EMPREST HIGH
6 .IF SALDO_MED && HISTORIC HIGH   -EMPREST HIGH

7. IF SALDO_HIGH && HISTORIC LOW   -EMPREST MED
8. IF SALDO_HIGH && HISTORIC MED   -EMPREST HIGH
9. IF SALDO_HIGH && HISTORIC HIGH  -EMPREST HIGH

not - 1, 2 
med - 4, 7
yes - 3, 5, 6, 8, 9
'''

rule1 = np.fmin(value_saldo_low,value_hist_low)
rule2 = np.fmin(value_saldo_low,value_hist_med)
rule3 = np.fmin(value_saldo_low,value_hist_hig)
rule4 = np.fmin(value_saldo_med,value_hist_low)
rule5 = np.fmin(value_saldo_med,value_hist_med)
rule6 = np.fmin(value_saldo_med,value_hist_hig)
rule7 = np.fmin(value_saldo_hig,value_hist_low)
rule8 = np.fmin(value_saldo_hig,value_hist_med)
rule9 = np.fmin(value_saldo_hig,value_hist_hig)

activate_emprest_low = np.fmin(rule1,np.fmax(rule2,emprest_low))
activate_emprest_med = np.fmin(rule4,np.fmax(rule7,emprest_med))
activate_emprest_hig = getfMax(rule3,rule5,rule6,rule8,rule9,emprest_hig)

print(activate_emprest_low)
print(activate_emprest_med)
print(activate_emprest_hig)

emp0 = np .  zeros_like ( x_emprestimo )


 # PLOTZÃO
fig2 , ax3 = plt .  subplots ( figsize = ( 8 , 3 ))

ax3 .  fill_between ( x_emprestimo , emp0 , activate_emprest_low , facecolor = 'b' , alpha = 0.7 )
ax3 .  plot ( x_emprestimo , emprest_low , 'b' , linewidth = 0.5 , linestyle = '--' , )
ax3 .  fill_between ( x_emprestimo , emp0 , activate_emprest_med , facecolor = 'g' , alpha = 0.7 )
ax3 .  plot ( x_emprestimo , emprest_med , 'g' , linewidth = 0.5 , linestyle = '--' )
ax3 .  fill_between ( x_emprestimo , emp0 , activate_emprest_hig , facecolor = 'r' , alpha = 0.7 )
ax3 .  plot ( x_emprestimo , emprest_hig , 'r' , linewidth = 0.5 , linestyle = '--' )
ax3 .  set_title ( 'Emprestimo sugerido' )

# Turn off top/right axes
for ax in (ax3, ):
    ax .  spines [ 'top' ] .  set_visible ( False )
    ax .  spines [ 'right' ] .  set_visible ( False )
    ax .  get_xaxis () .  tick_bottom ()
    ax .  get_yaxis () .  tick_left ()

plt .  tight_layout ()
plt.show()



######################################################3
agregado = np.fmax(activate_emprest_hig,np.fmax(activate_emprest_med,activate_emprest_low))
emprest = fuzz.defuzz(x_emprestimo,agregado,'centroid')
emprest_activate = fuzz.interp_membership(x_emprestimo,agregado,emprest)


fig , ax0 = plt .  subplots ( figsize = ( 8 , 3 ))


ax0.plot(x_emprestimo, emprest_low, 'b', linewidth=1.5,linestyle = '--')
ax0.plot(x_emprestimo, emprest_med, 'g', linewidth=1.5, linestyle = '--' )
ax0.plot(x_emprestimo, emprest_hig, 'r', linewidth=1.5, linestyle = '--' )
ax0.set_title('Linha de crédito oferecida')
ax0 .  fill_between ( x_emprestimo , emp0 , agregado , facecolor = 'Orange' , alpha = 0.7 )
ax0 .  plot ([ emprest , emprest ], [ 0 , emprest_activate ], 'k' , linewidth = 1.5 , alpha = 0.9 )


# Turn off top/right axes
for ax in ( ax0 ,):
    ax .  spines [ 'top' ] .  set_visible ( False )
    ax .  spines [ 'right' ] .  set_visible ( False )
    ax .  get_xaxis () .  tick_bottom ()
    ax .  get_yaxis () .  tick_left ()

plt .  tight_layout ()
plt.show()