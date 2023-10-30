import json
import numpy as np

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
            g_real = h * g
            for nu in poissonRatios:
                for alpha in shift_angles:
                    strnu = str(nu)
                    strnu = strnu.replace(".", "")
                    basefile3D =  "regularplate3D_h2-" + str(int(-np.log2(h))) + "_H2-" + str(int(-np.log2(H))) + "_g2+" + str(int(np.log2(g)))
                    meshfile3D = basefile3D + "_hexahedral_shift" + str(alpha)
                    file3D = basefile3D + "_nu" + strnu + "_hexahedral_shift" + str(alpha)

                    if randomshift:
                        meshfile3D += "_random"
                        file3D += "_random"
                    dictionary = {
                        "geometry": {
                            "advanced": {
                                "normalize_mesh": False
                            },
                            "mesh": "meshes/" + meshfile3D + ".msh",
                            "surface_selection": {
                                "threshold": 1e-07
                            }
                        },
                        "materials": {
                                "type": "LinearElasticity",
                                "E": 100,
                                "nu": nu,
                                "rho": 1
                            },

                        "boundary_conditions": {
                            "rhs": [0,0,10. * h**2 ],
                            "dirichlet_boundary": [{
                                "id": 1,
                                "value": [0.0, 0.0, 0.0]
                            },{
                                "id": 2,
                                "value": [0.0, 0.0, 0.0]
                            },{
                                "id": 3,
                                "value": [0.0, 0.0, 0.0]
                            },{
                                "id": 4,
                                "value": [0.0, 0.0, 0.0]
                            }]
                            },
                        "output": {
                            "json": "resultsPolyFEM_hexahedral/" + file3D + "/stats.json",
                            "data": {
                                "nodes": "resultsPolyFEM_hexahedral/" + file3D + "/nodes.txt",
                                "solution": "resultsPolyFEM_hexahedral/" + file3D + "/sol.txt",
                                "advanced": {
                                    "reorder_nodes": True
                                }
                            },
                            "paraview": {"file_name": "resultsPolyFEM_hexahedral/" + file3D + "/result.vtu",
                                    "high_order_mesh": False,
                                     "options": {
                                         "use_hdf5" : True
                                     }}
                        },
                        "space": {
                            "discr_order": 2
                        },
                        "solver": {
                            "linear": {
                                "solver": "Eigen::PardisoLLT"
                            }
                        }
                    }
                    # Serializing json
                    json_object = json.dumps(dictionary)
    
                    # Writing to sample.json
                    with open("json/run_" + file3D + ".json", "w") as outfile:
                        outfile.write(json_object)
