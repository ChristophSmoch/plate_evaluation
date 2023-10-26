import numpy as np
import json

with open("specs.json", "r") as f:
    specs = json.load(f)
    path_to_gmsh_bin = specs["path_to_gmsh_bin"]
    path_to_polyfem_bin = specs["path_to_polyfem_bin"]
    thickness_bounds = specs["thickness_bounds"]
    inplaneRes_bounds = specs["inplaneRes_bounds"]
    outofplaneRes_bounds = specs["outofplaneRes_bounds"]
    shift_bounds = specs["shift_bounds"]

thickness = [ 2.**( - i ) for i in range( thickness_bounds[0], thickness_bounds[1] ) ]
inplaneRes = [ 2.**( -i ) for i in range(inplaneRes_bounds[0], inplaneRes_bounds[1] ) ]
outofplaneRes = [ 2**( i ) for i in range(outofplaneRes_bounds[0] , outofplaneRes_bounds[1]  ) ]
shift_factor = [2.**( - i ) for i in range(shift_bounds[0], shift_bounds[1])]

poissonRatios = [0.0] 

dict_polyfem = []
for H in inplaneRes:
    for h in thickness:
        for nu in poissonRatios:
            strnu = str(nu)
            strnu = strnu.replace(".", "")

            for g in outofplaneRes:
                for s in shift_factor:
                    try:
                        print("H = " + str(H))
                        file3D =  "regularplate3D_h2-" + str(int(-np.log2(h))) + "_H2-" + str(int(-np.log2(H))) + "_g2+" + str(int(np.log2(g))) + "_nu" + strnu + "_hexahedral_shift2-" + str(int(-np.log2(s)))
                        with open("resultsPolyFEM_hexahedral/" + file3D + "/stats.json", "r") as f:
                            data = json.load(f)
                            solve_time_PolyFEM = data["time_solving"]
                            max_disp = data["err_linf"]

                        data = {"name": file3D,
                            "H": H,
                            "h": h,
                            "g": g,
                            "nu": nu,
                            "max_disp": max_disp,
                            "solve_time": solve_time_PolyFEM,
                            "shift": s * H / np.sqrt(2),
                            "shift_angle": np.math.atan(s*H/(h * np.sqrt(2))) / (2*np.math.pi) * 360
                        }
                        dict_polyfem.append(data)
                    except IOError:
                        print("Cannot find " + file3D)
                        

polyfemjson = json.dumps(dict_polyfem)

with open("polyfem_hexahedral_shifted_data.json", "w") as outfile:
    outfile.write(polyfemjson)

 