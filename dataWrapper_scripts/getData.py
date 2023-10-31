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

def getpesoptVectors(H, nu):
    strnu = str(nu)
    strnu = strnu.replace(".", "")
    file2D = "pointplate2D_h1e-1_H2-" + str(int(-np.log2(H))) + "_nu" + strnu
    points = []
    with open("results_2D/" + file2D + "/deformedShell.vtk", "r") as f:
        isPoint = False
        pointCounter = 0
        
        for line in f:
            if pointCounter >= 3 * (4 + 49):
                break
            if line.startswith("0"):
                #print(line)
                isPoint = True
            if isPoint:
                
                line = line.split(" ")
                line = line[:-1]
                for x in line:
                    x = float(x)
                    if pointCounter >= 3 * (4 + 49):
                        break
                    if pointCounter >= 3 * 4:
                        points.append(x)
                    pointCounter += 1
        
        for i in range(len(points)):
            if i % 3 == 0 or i % 3 == 1:
                points[i] = 0
    points = 10. * np.array(points)
    return(points)

def getpolyfem_tetrahedral_Vectors(H, h, g, nu):
    strnu = str(nu)
    strnu = strnu.replace(".", "")
    g_real = h * g
    file3D = "pointplate3D_h2-" + str(int(-np.log2(h)))+  "_H2-" + str(int(-np.log2(H))) + "_g2+" + str(int(np.log2(g)))  + "_nu" + strnu + "_tetrahedral"
    points = readFromHdf("resultsPolyFEM_tetrahedral/" + file3D + "/result.hdf", h)
    return(points)

def getpolyfem_hexahedral_Vectors(H, h, g, nu):
    strnu = str(nu)
    strnu = strnu.replace(".", "")
    g_real = h * g
    file3D = "pointplate3D_h2-" + str(int(-np.log2(h)))+  "_H2-" + str(int(-np.log2(H))) + "_g2+" + str(int(np.log2(g)))  + "_nu" + strnu + "_hexahedral"
    points = readFromHdf("resultsPolyFEM_hexahedral/" + file3D + "/result.hdf", h)
    return(points)

def getpolyfem_prism_Vectors(H, h, g, nu):
    strnu = str(nu)
    strnu = strnu.replace(".", "")
    g_real = h * g
    file3D = "pointplate3D_h2-" + str(int(-np.log2(h)))+  "_H2-" + str(int(-np.log2(H))) + "_g2+" + str(int(np.log2(g)))  + "_nu" + strnu + "_prism"
    points = readFromHdf("resultsPolyFEM_prism/" + file3D + "/result.hdf", h)
    return(points)

npts_sqrt = 7
def refSols():            
    refSol2D = np.zeros((len(thickness), len(poissonRatios), 3 *(49)))
    refSol3D = np.zeros((len(thickness), len(poissonRatios), 3 * 3 * (49)))


    for h in thickness:
        for nu in poissonRatios:
            refSol2D[thickness.index(h)][poissonRatios.index(nu)] = getpesoptVectors(2**(-8), nu)
            strnu = str(nu)
            strnu = strnu.replace(".", "")
            g_real = h * 1.
            # Path to reference solution:
            # file3D = "pointplate3D_h2-" + str(int(-np.log2(h)))+  "_H2-" + str(7) + "_g2-" + str(int(-np.log2(g_real)) + 1)  + "_nu" + strnu + "_cubic"
            # points = []
            # with open("resultsPolyFEM/" + file3D + "/sol.txt", "r") as f:
            #     pointCounter = 0
                
            #     for line in f:
            #         if pointCounter < 3 * (4 + npts_sqrt**2):
            #             line = line.split(" ")
            #             line = line[:-1]
            #             for x in line:
            #                 x = float(x)
            #                 points.append(x)
            #         else:
            #             break
            #         pointCounter += 1

            # points = np.array(points)
            # refSol3D[thickness.index(h)][poissonRatios.index(nu)] = points
       
    return refSol2D, refSol3D
refpesopt, refpolyfem = refSols()

dict_pesopt = []
dict_polyfem_tet = []
dict_polyfem_hex = []
dict_polyfem_prism = []
for H in inplaneRes:
    for h in thickness:
        for nu in poissonRatios:
            strnu = str(nu)
            strnu = strnu.replace(".", "")

            refvec = []
            with open("polyfem_ref_data.json", "r") as f:
                refdata = json.load(f)
                for d in refdata:
                    if d["h"] == h and d["nu"] == nu:
                        refvec = d["solvec"]
                        break
            refpolyfem = np.array(refvec)

            file2D = "pointplate2D_h1e-1_H2-" + str(int(-np.log2(H))) + "_nu" + strnu
            try:
                with open("results_2D/" + file2D + "/convergenceTimeSolve.dat", "r") as f:
                    for lines in f:
                        if lines.startswith("0"):
                            refstep, value = lines.split(" ")
                            solve_time_PESOPT = float(value)
                vec =   getpesoptVectors(H,nu)
            
                l2_2D =  np.linalg.norm(vec - refpesopt[thickness.index(h)][poissonRatios.index(nu)])
                l2_3D =  np.linalg.norm(vec - refpolyfem[3 * 98:])

                linf_2D = np.linalg.norm(vec - refpesopt[thickness.index(h)][poissonRatios.index(nu)], ord = np.inf)
                linf_3D = np.linalg.norm(vec - refpolyfem[3 * 98:], ord = np.inf)
                max_disp = np.linalg.norm(vec , ord = np.inf)

                data = {"name": file2D,
                        "H": H,
                        "h": h,
                        "nu": nu,
                        "max_disp": max_disp,
                        "solve_time": solve_time_PESOPT,
                        "l2_2D": l2_2D,
                        "l2_3D": l2_3D,
                        "linf_2D": linf_2D,
                        "linf_3D": linf_3D,
                        "l2_3D_mid": l2_3D,
                        "linf_3D_mid": linf_3D,
                        "solvec": list(vec)}
                dict_pesopt.append(data)
            except IOError:
                print("Cannot find " + file2D)

            for g in outofplaneRes:
                g_real = h * g
                try:
                    print("tet")
                    file3D =  "pointplate3D_h2-" + str(int(-np.log2(h))) + "_H2-" + str(int(-np.log2(H))) + "_g2+" + str(int(np.log2(g))) + "_nu" + strnu + "_tetrahedral"
                    with open("resultsPolyFEM_tetrahedral/" + file3D + "/stats.json", "r") as f:
                        data = json.load(f)
                        solve_time_PolyFEM = data["time_solving"]
                        max_disp = data["err_linf"]
                    vec = getpolyfem_tetrahedral_Vectors(H, h, g, nu)
                    l2_2D =  np.linalg.norm(vec[3 * 2 * 49:] - refpesopt[thickness.index(h)][poissonRatios.index(nu)])
                    l2_3D =  np.linalg.norm(vec - refpolyfem) / 3.

                    linf_2D =  np.linalg.norm(vec[3 * 2 * 49:] - refpesopt[thickness.index(h)][poissonRatios.index(nu)], ord = np.inf)
                    linf_3D =  np.linalg.norm(vec - refpolyfem, ord = np.inf)

                    l2_3D_mid =  np.linalg.norm(vec[3 * 2 * 49:] - refpolyfem[3 * 98:]) / 3.
                    linf_3D_mid =  np.linalg.norm(vec[3 * 2 * 49:] - refpolyfem[3 * 98:], ord = np.inf)

                    

                    data = {"name": file3D,
                        "H": H,
                        "h": h,
                        "g": g,
                        "nu": nu,
                        "max_disp": max_disp,
                        "solve_time": solve_time_PolyFEM,
                        "l2_2D": l2_2D,
                        "l2_3D": l2_3D,
                        "linf_2D": linf_2D,
                        "linf_3D": linf_3D,
                        "l2_3D_mid": l2_3D_mid,
                        "linf_3D_mid": linf_3D_mid,
                        "solvec": list(vec)}
                    dict_polyfem_tet.append(data)
                except IOError:
                    print("Cannot find " + file3D)

                try:
                    print("hex")
                    file3D =  "pointplate3D_h2-" + str(int(-np.log2(h))) + "_H2-" + str(int(-np.log2(H))) + "_g2+" + str(int(np.log2(g))) + "_nu" + strnu + "_hexahedral"
                    with open("resultsPolyFEM_hexahedral/" + file3D + "/stats.json", "r") as f:
                        data = json.load(f)
                        solve_time_PolyFEM = data["time_solving"]
                        max_disp = data["err_linf"]
                    vec = getpolyfem_hexahedral_Vectors(H, h, g, nu)
                    l2_2D =  np.linalg.norm(vec[3 * 2 * 49:] - refpesopt[thickness.index(h)][poissonRatios.index(nu)])
                    l2_3D =  np.linalg.norm(vec - refpolyfem) / 3.

                    linf_2D =  np.linalg.norm(vec[3 * 2 * 49:] - refpesopt[thickness.index(h)][poissonRatios.index(nu)], ord = np.inf)
                    linf_3D =  np.linalg.norm(vec - refpolyfem, ord = np.inf)

                    l2_3D_mid =  np.linalg.norm(vec[3 * 2 * 49:] - refpolyfem[3 * 2 * 49:]) / 3.
                    linf_3D_mid =  np.linalg.norm(vec[3 * 2 * 49:] - refpolyfem[3 * 2 * 49:], ord = np.inf)

                    

                    data = {"name": file3D,
                        "H": H,
                        "h": h,
                        "g": g,
                        "nu": nu,
                        "max_disp": max_disp,
                        "solve_time": solve_time_PolyFEM,
                        "l2_2D": l2_2D,
                        "l2_3D": l2_3D,
                        "linf_2D": linf_2D,
                        "linf_3D": linf_3D,
                        "l2_3D_mid": l2_3D_mid,
                        "linf_3D_mid": linf_3D_mid,
                        "solvec": list(vec)}
                    dict_polyfem_hex.append(data)
                except IOError:
                    print("Cannot find " + file3D)
                
                try:
                    print("prism")
                    file3D =  "pointplate3D_h2-" + str(int(-np.log2(h))) + "_H2-" + str(int(-np.log2(H))) + "_g2+" + str(int(np.log2(g))) + "_nu" + strnu + "_prism"
                    with open("resultsPolyFEM_prism/" + file3D + "/stats.json", "r") as f:
                        data = json.load(f)
                        solve_time_PolyFEM = data["time_solving"]
                        max_disp = data["err_linf"]
                    vec = getpolyfem_prism_Vectors(H, h, g, nu)
                    l2_2D =  np.linalg.norm(vec[3 * 2 * 49:] - refpesopt[thickness.index(h)][poissonRatios.index(nu)])
                    l2_3D =  np.linalg.norm(vec - refpolyfem) / 3.

                    linf_2D =  np.linalg.norm(vec[3 * 2 * 49:] - refpesopt[thickness.index(h)][poissonRatios.index(nu)], ord = np.inf)
                    linf_3D =  np.linalg.norm(vec - refpolyfem, ord = np.inf)

                    l2_3D_mid =  np.linalg.norm(vec[3 * 2 * 49:] - refpolyfem[3 * 2 * 49:]) / 3.
                    linf_3D_mid =  np.linalg.norm(vec[3 * 2 * 49:] - refpolyfem[3 * 2 * 49:], ord = np.inf)

                    

                    data = {"name": file3D,
                        "H": H,
                        "h": h,
                        "g": g,
                        "nu": nu,
                        "max_disp": max_disp,
                        "solve_time": solve_time_PolyFEM,
                        "l2_2D": l2_2D,
                        "l2_3D": l2_3D,
                        "linf_2D": linf_2D,
                        "linf_3D": linf_3D,
                        "l2_3D_mid": l2_3D_mid,
                        "linf_3D_mid": linf_3D_mid,
                        "solvec": list(vec)}
                    dict_polyfem_prism.append(data)
                except IOError:
                    print("Cannot find " + file3D)
                    

polyfem_tet_json = json.dumps(dict_polyfem_tet)
polyfem_hex_json = json.dumps(dict_polyfem_hex)
polyfem_prism_json = json.dumps(dict_polyfem_prism)
pesoptjson = json.dumps(dict_pesopt)

with open("polyfem_tet_data.json", "w") as outfile:
    outfile.write(polyfem_tet_json)
with open("polyfem_hex_data.json", "w") as outfile:
    outfile.write(polyfem_hex_json)
with open("polyfem_prism_data.json", "w") as outfile:
    outfile.write(polyfem_prism_json)
with open("pesopt_data.json", "w") as outfile:
    outfile.write(pesoptjson)
 