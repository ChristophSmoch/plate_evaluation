import subprocess
import numpy as np
import json

with open("specs.json", "r") as f:
    specs = json.load(f)
    path_to_gmsh_bin = specs["path_to_gmsh_bin"]
    path_to_polyfem_bin = specs["path_to_polyfem_bin"]
    thickness_bounds = specs["thickness_bounds"]
    inplaneRes_bounds = specs["inplaneRes_bounds"]
    outofplaneRes_bounds = specs["outofplaneRes_bounds"]
    shift_angles = specs["shift"]["shift_angles"]
    randomshift = specs["shift"]["randomshift"]

thickness = [ 2.**( - i ) for i in range( thickness_bounds[0], thickness_bounds[1] ) ]
inplaneRes = [ 2.**( -i ) for i in range(inplaneRes_bounds[0], inplaneRes_bounds[1] ) ]
outofplaneRes = [ 2**( i ) for i in range(outofplaneRes_bounds[0] , outofplaneRes_bounds[1]  ) ]

poissonRatios = [0.0] 

for H in inplaneRes:
    for h in thickness:
        for g in outofplaneRes:
            for nu in poissonRatios:
                for alpha in shift_angles:
                    strnu = str(nu)
                    strnu = strnu.replace(".", "")
                    basefile3D =  "pointplate3D_h2-" + str(int(-np.log2(h))) + "_H2-" + str(int(-np.log2(H))) + "_g2+" + str(int(np.log2(g)) )
                    file3D = basefile3D + "_nu" + strnu + "_hexahedral_shift" + str(alpha)
                    if randomshift:
                        file3D += "_random"
                    print(file3D)
                    popen = subprocess.Popen("mkdir resultsPolyFEM_hexahedral/" + file3D , stdout = subprocess.PIPE, shell = True )
                    popen.wait()
                    popen = subprocess.Popen(path_to_polyfem_bin + " -j json/run_" + file3D + ".json", stdout = subprocess.PIPE, shell = True )
                    popen.wait()
                    output = popen.stdout.read()
                    print( output )
