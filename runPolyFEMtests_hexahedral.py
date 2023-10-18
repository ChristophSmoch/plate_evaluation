import os
import numpy as np
import json

with open("specs.json", "r") as f:
    specs = json.load(f)
    path_to_polyfem_bin = specs["path_to_polyfem_bin"]
    thickness_bounds = specs["thickness_bounds"]
    inplaneRes_bounds = specs["inplaneRes_bounds"]
    outofplaneRes_bounds = specs["outofplaneRes_bounds"]

thickness = [ 2.**( - i ) for i in range( thickness_bounds[0], thickness_bounds[1] + 1 ) ]
inplaneRes = [ 2.**( -i ) for i in range(inplaneRes_bounds[0], inplaneRes_bounds[1] + 1) ]
outofplaneRes = [ 2.**( -i ) for i in range(outofplaneRes_bounds[0] - 1, outofplaneRes_bounds[1] ) ]
poissonRatios = [0.0] 

for H in inplaneRes:
    for h in thickness:
        for g in outofplaneRes:
            g_real = h * g
            for nu in poissonRatios:
                strnu = str(nu)
                strnu = strnu.replace(".", "")
                file3D =  "pointplate3D_h2-" + str(int(-np.log2(h))) + "_H2-" + str(int(-np.log2(H))) + "_g2-" + str(int(-np.log2(g_real)) + 1)
                os.system("mkdir resultsPolyFEM_hexahedral/" + file3D + "_nu" + strnu + "_hexahedral")
                os.system("../polyfem/build/PolyFEM_bin -j json/run_" + file3D + "_nu" + strnu + "_hexahedral" + ".json")
