import subprocess
import numpy as np
import json

with open("specs.json", "r") as f:
    specs = json.load(f)
    path_to_polyfem_bin = specs["path_to_polyfem_bin"]
    thickness_bounds = specs["thickness_bounds"]
    inplaneRes_bounds = specs["inplaneRes_bounds"]

thickness = [ 2.**( - i ) for i in range( thickness_bounds[0], thickness_bounds[1]  ) ]
inplaneRes = [ 2.**( -i ) for i in range(inplaneRes_bounds[0], inplaneRes_bounds[1] ) ]
poissonRatios = [0.0] 

for H in inplaneRes:
    for h in thickness:
        for nu in poissonRatios:
            strnu = str(nu)
            strnu = strnu.replace(".", "")
            file3D =  "pointplate3D_h2-" + str(int(-np.log2(h))) + "_H2-" + str(int(-np.log2(H)))

            popen = subprocess.Popen("mkdir resultsPolyFEM_hexahedral/" + file3D + "_nu" + strnu + "_hexahedral_single", stdout = subprocess.PIPE, shell = True )
            popen.wait()
            popen = subprocess.Popen(path_to_polyfem_bin + " -j json/run_" + file3D + "_nu" + strnu + "_hexahedral_single.json", stdout = subprocess.PIPE, shell = True )
            popen.wait()
            output = popen.stdout.read()
            print( output )
