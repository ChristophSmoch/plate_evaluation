import numpy as np
import json
from readHDF import readFromHdf

with open("specs.json", "r") as f:
    specs = json.load(f)
    path_to_polyfem_bin = specs["path_to_polyfem_bin"]
    thickness_bounds = specs["thickness_bounds"]
    inplaneRes_bounds = specs["inplaneRes_bounds"]
    outofplaneRes_bounds = specs["outofplaneRes_bounds"]

thickness = [ 2.**( - i ) for i in range( thickness_bounds[0], thickness_bounds[1] ) ]
inplaneRes = [ 2.**( -i ) for i in range(inplaneRes_bounds[0], inplaneRes_bounds[1]) ]
outofplaneRes = [ 2.**( i ) for i in range(outofplaneRes_bounds[0], outofplaneRes_bounds[1]) ]
poissonRatios = [0.0] 

def getpolyfem_tetrahedral_Vectors(file3D, H, h, g, nu):
    strnu = str(nu)
    strnu = strnu.replace(".", "")
    g_real = h * g
    # file3D = "pointplate3D_h2-" + str(int(-np.log2(h)))+  "_H2-" + str(int(-np.log2(H))) + "_g2+" + str(int(np.log2(g)))  + "_nu" + strnu + "_tetrahedral"
    points = readFromHdf("resultsPolyFEM_tetrahedral/" + file3D + "/result.hdf", h)
    return(points)

def getpolyfem_hexahedral_Vectors(H, h, g, nu):
    strnu = str(nu)
    strnu = strnu.replace(".", "")
    g_real = h * g
    file3D = "pointplate3D_h2-" + str(int(-np.log2(h)))+  "_H2-" + str(int(-np.log2(H))) + "_g2+" + str(int(np.log2(g)))  + "_nu" + strnu + "_hexahedral"
    points = readFromHdf("resultsPolyFEM_hexahedral/" + file3D + "/result.hdf", h)
    return(points)


npts_sqrt = 7



dict_ref = []

H = 2.**(-7)
g = 1.
for h in thickness:
    for nu in poissonRatios:
        strnu = str(nu)
        strnu = strnu.replace(".", "")
        try:
            file3D =  "pointplate3D_h2-" + str(int(-np.log2(h))) + "_H2-" + str(int(-np.log2(H))) + "_g2+" + str(int(np.log2(g))) + "_nu" + strnu + "_tetrahedral_quartic"
            with open("resultsPolyFEM_tetrahedral/" + file3D + "/stats.json", "r") as f:
                data = json.load(f)
                solve_time_PolyFEM = data["time_solving"]
                max_disp = data["err_linf"]
            vec = getpolyfem_tetrahedral_Vectors(file3D, H, h, g, nu)

            data = {"name": file3D,
                "H": H,
                "h": h,
                "g": g,
                "nu": nu,
                "max_disp": max_disp,
                "solve_time": solve_time_PolyFEM,
                "solvec": list(vec)}
            dict_ref.append(data)
        except IOError:
            print("Cannot find " + file3D)

        
                    

polyfem_ref_json = json.dumps(dict_ref)

with open("polyfem_ref_data.json", "w") as outfile:
    outfile.write(polyfem_ref_json)
