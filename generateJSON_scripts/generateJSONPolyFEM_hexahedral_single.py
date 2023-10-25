import json
import os
import numpy as np

with open("specs.json", "r") as f:
    specs = json.load(f)
    path_to_polyfem_bin = specs["path_to_polyfem_bin"]
    thickness_bounds = specs["thickness_bounds"]
    inplaneRes_bounds = specs["inplaneRes_bounds"]
    outofplaneRes_bounds = specs["outofplaneRes_bounds"]

thickness = [ 2.**( - i ) for i in range( thickness_bounds[0], thickness_bounds[1] ) ]
inplaneRes = [ 2.**( -i ) for i in range(inplaneRes_bounds[0], inplaneRes_bounds[1] ) ]
outofplaneRes = [ 2.**( i ) for i in range(outofplaneRes_bounds[0], outofplaneRes_bounds[1] ) ]
poissonRatios = [0.0] 


for H in inplaneRes:
    for h in thickness:
        for nu in poissonRatios:
            strnu = str(nu)
            strnu = strnu.replace(".", "")
            file3D =  "pointplate3D_h2-" + str(int(-np.log2(h))) + "_H2-" + str(int(-np.log2(H))) 
            dictionary = {
                "geometry": {
                    "advanced": {
                        "normalize_mesh": True
                    },
                    "mesh": "meshes/" + file3D + "_hexahedral_single.msh",
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
                    "json": "resultsPolyFEM_hexahedral/" + file3D + "_nu" + strnu + "_hexahedral_single/stats.json",
                    "data": {
                        "nodes": "resultsPolyFEM_hexahedral/" + file3D + "_nu" + strnu + "_hexahedral_single/nodes.txt",
                        "solution": "resultsPolyFEM_hexahedral/" + file3D + "_nu" + strnu + "_hexahedral_single/sol.txt",
                        "advanced": {
                            "reorder_nodes": True
                        }
                    },
                    "paraview": {"file_name": "resultsPolyFEM_hexahedral/" + file3D + "_nu" + strnu + "_hexahedral_single/result.vtu",
                            "high_order_mesh": False}
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
            with open("json/run_" + file3D + "_nu" + strnu + "_hexahedral_single.json", "w") as outfile:
                outfile.write(json_object)
