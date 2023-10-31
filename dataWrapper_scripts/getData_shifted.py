import numpy as np
import json
import h5py


def readFromHdf_shifted(filepath, h):
    with h5py.File(filepath, "r+") as f:
        a_group_key = list(f.keys())[0]

        points = f[a_group_key]['Points']
        pointzz = np.array(points[:])
        displacement = f[a_group_key]['PointData']["solution"]
        dispzz = np.array(displacement[:])

        testpoints = [[1./8. + 1./8. * j, 1./8. + 1./8. * i] for i in range(7) for j in range(7)]
        disp_at_testpoints = np.zeros((49,3))


        for pidx, pts in enumerate(testpoints):

            p0 = np.array([pts[0],pts[1], 0.])

            id0 = np.where(np.all(pointzz==p0,axis=1))
        
            disp_at_testpoints[pidx][:] = dispzz[id0[0][0]]
            
        disp_at_testpoints = disp_at_testpoints.reshape(-1)
        return disp_at_testpoints


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

dict_reg = []
dict_reg_shift = []
for H in inplaneRes:
    for h in thickness:
        for nu in poissonRatios:
            strnu = str(nu)
            strnu = strnu.replace(".", "")

            for g in outofplaneRes:
                for alpha in shift_angles:
                    try:
                        file3D =  "regularplate3D_h2-" + str(int(-np.log2(h))) + "_H2-" + str(int(-np.log2(H))) + "_g2+" + str(int(np.log2(g))) + "_nu" + strnu + "_hexahedral_shift" + str(alpha)
                        if randomshift:
                            file3D += "_random"

                        vec = readFromHdf_shifted("resultsPolyFEM_hexahedral/" + file3D + "/result.hdf", h)

                        refvec = []
                        with open("polyfem_ref_data.json", "r") as f:
                            refdata = json.load(f)
                            for d in refdata:
                                if d["h"] == h and d["nu"] == nu:
                                    refvec = d["solvec"]
                                    break
                        refpolyfem = np.array(refvec)

                        l2_3D =  np.linalg.norm(vec - refpolyfem[:3 * 49])
                        
                        with open("resultsPolyFEM_hexahedral/" + file3D + "/stats.json", "r") as f:
                            data = json.load(f)
                            solve_time_PolyFEM = data["time_solving"]
                            max_disp = data["err_linf"]

                        data = {"name": file3D,
                            "H": H,
                            "h": h,
                            "g": g,
                            "nu": nu,
                            "l2_3D": l2_3D,
                            "max_disp": max_disp,
                            "solve_time": solve_time_PolyFEM,
                            "shift": h * np.tan(alpha),
                            "shift_angle": alpha
                        }
                        dict_reg_shift.append(data)
                    except IOError:
                        print("Cannot find " + file3D)
                    try:
                        file3D =  "regularplate3D_h2-" + str(int(-np.log2(h))) + "_H2-" + str(int(-np.log2(H))) + "_g2+" + str(int(np.log2(g))) + "_nu" + strnu + "_hexahedral"

                        vec = readFromHdf_shifted("resultsPolyFEM_hexahedral/" + file3D + "/result.hdf", h)

                        refvec = []
                        with open("polyfem_ref_data.json", "r") as f:
                            refdata = json.load(f)
                            for d in refdata:
                                if d["h"] == h and d["nu"] == nu:
                                    refvec = d["solvec"]
                                    break
                        refpolyfem = np.array(refvec)

                        l2_3D =  np.linalg.norm(vec - refpolyfem[:3 * 49])
                        
                        with open("resultsPolyFEM_hexahedral/" + file3D + "/stats.json", "r") as f:
                            data = json.load(f)
                            solve_time_PolyFEM = data["time_solving"]
                            max_disp = data["err_linf"]

                        data = {"name": file3D,
                            "H": H,
                            "h": h,
                            "g": g,
                            "nu": nu,
                            "l2_3D": l2_3D,
                            "max_disp": max_disp,
                            "solve_time": solve_time_PolyFEM,
                            "shift": h * np.tan(alpha),
                            "shift_angle": alpha
                        }
                        dict_reg.append(data)
                    except IOError:
                        print("Cannot find " + file3D)
                    

regshiftjson = json.dumps(dict_reg_shift)
regjson = json.dumps(dict_reg)

with open("polyfem_hexahedral_regular_shifted_data.json", "w") as outfile:
    outfile.write(regshiftjson)
with open("polyfem_hexahedral_regular_data.json", "w") as outfile:
    outfile.write(regjson)

 