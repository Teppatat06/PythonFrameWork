import numpy as np
import pyDOE2
import random
from OptimizationTestFunctions import Fletcher, plot_3d
import matplotlib.pyplot as plt
from scipy import optimize as opt

def cossit(x1,x2):


    fact1 = np.sin(x1) * np.sin(x2);
    fact2 = np.exp(abs(100 - np.sqrt(x1 ** 2 + x2 * 2) / np.pi))
    y = -0.0001 * (abs(fact1 * fact2) + 1) ** 0.1
    return y





parent_dir = "D:\\PUN\\OPT_GV\\"
script_dir = parent_dir + "script\\"



# Beta-test
# sampling point
ccd = pyDOE2.ccdesign(3, [0, 0], alpha='orthogonal',face='cci')

# Training data
seed = 100
lhs  = pyDOE2.lhs(3, samples=seed, criterion='correlation', iterations=None)
lhs = np.array(lhs)

alldesign = [[0 for i in range(3)] for j in range(len(ccd) + 1)]
sampling_scale = [0 for i in range(len(ccd) + 1)]
sampling_sweep_angle = [0 for i in range(len(ccd) + 1)]
sampling_number_of_blade= [0 for i in range(len(ccd) + 1)]
response= [0 for i in range(len(ccd) + 1)]

count = 0
for norm_mem in ccd:
    alldesign[count+1][0] = norm_mem[0]
    alldesign[count + 1][1] = norm_mem[1]
    alldesign[count + 1][2] = norm_mem[2]
    count += 1


grid_x, grid_y = np.mgrid[-1:1:100j, -1:1:200j]



#output = random.random()


##  RSM
### decode data to physical information

### solve cubic equation by using encode data
####Pseudo Inverse (PSI): Eigen Value Decomposition or SVD
####Coeff = PSI*OBJ <<< equation!!!

## OPT

