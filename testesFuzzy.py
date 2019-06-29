import numpy as np 
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Generate universe variables
#   * Quality and service on subjective ranges [0, 10]
#   * Tip has a range of [0, 25] in units of percentage points
x_qual = np.arange(0,30,1)
x_serv =np.arange(0,30,1)
x_tip  = np.arange(0,30,1)

# Generate fuzzy membership functions
qual_lo = fuzz.trapmf(x_qual, [0, 0, 5, 10])
qual_md = fuzz.trapmf(x_qual, [5, 10, 15, 20])
qual_hi = fuzz.trapmf(x_qual, [15, 20, 30, 35])
serv_lo = fuzz.trapmf(x_serv, [0, 0, 15, 20])
serv_md = fuzz.trapmf(x_serv,  [5, 15, 20, 25])
serv_hi = fuzz.trapmf(x_serv, [15, 20, 30, 35])
tip_lo = fuzz.trapmf(x_tip,  [0, 0, 15, 20])
tip_md = fuzz.trapmf(x_tip,  [5, 15, 20, 25])
tip_hi = fuzz.trapmf(x_tip, [15, 20, 30, 35])

# Visualize these universes and membership functions
fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

ax0.plot(x_qual, qual_lo, 'b', linewidth=1.5, label='Bad')
ax0.plot(x_qual, qual_md, 'g', linewidth=1.5, label='Decent')
ax0.plot(x_qual, qual_hi, 'r', linewidth=1.5, label='Great')
ax0.set_title('Food quality')
ax0.legend()


ax1.plot(x_serv, serv_lo, 'b', linewidth=1.5, label='Poor')
ax1.plot(x_serv, serv_md, 'g', linewidth=1.5, label='Acceptable')
ax1.plot(x_serv, serv_hi, 'r', linewidth=1.5, label='Amazing')
ax1.set_title('Service quality')
ax1.legend()


ax2.plot(x_tip, tip_lo, 'b', linewidth=1.5, label='Low')
ax2.plot(x_tip, tip_md, 'g', linewidth=1.5, label='Medium')
ax2.plot(x_tip, tip_hi, 'r', linewidth=1.5, label='High')
ax2.set_title('Tip amount')
ax2.legend()
# Turn off top/right axes
for ax in (ax0, ax1, ax2):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
plt.tight_layout()
plt.show()