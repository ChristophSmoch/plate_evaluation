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
    shift_bounds = specs["shift_bounds"]

thickness = [ 2.**( - i ) for i in range( thickness_bounds[0], thickness_bounds[1] ) ]
inplaneRes = [ 2.**( -i ) for i in range(inplaneRes_bounds[0], inplaneRes_bounds[1] ) ]
outofplaneRes = [ 2**( i ) for i in range(outofplaneRes_bounds[0] , outofplaneRes_bounds[1]  ) ]
shift_factor = [5 + 5 * i for i in range(shift_bounds)]


for H in inplaneRes:
    for h in thickness:
        for g in outofplaneRes:
            for alpha in shift_factor:
                file3D = "regularplate3D_h2-" + str(int(-np.log2(h))) + "_H2-" + str(int(-np.log2(H))) + "_g2+" + str(int(np.log2(g))) + "_hexahedral_shift" + str(alpha) 
                n_nodes = int( (1 / H + 1)**2) * (g + 1)
                print(n_nodes)
                n_elems = int(1/H**2 * g)
                with open("meshes/" + file3D + ".msh", "w" ) as f:
                    f.write("$MeshFormat\n")
                    f.write("2.2 0 8\n")
                    f.write("$EndMeshFormat\n")
                    f.write("$Nodes\n")
                    f.write(str(n_nodes) + "\n")
                    for k in range( g + 1 ):
                        for i in range(int(1 / H ) + 1):
                            for j in range(int(1 / H ) + 1 ):
                                node_nr = j + int( 1 / H + 1 ) * i +  int( 1 / H + 1 )**2 * k + 1
                                if k == 1 and H * j != 0 and H * j != 1 and H * i != 0 and H * i != 1:
                                    f.write(str(node_nr) + " " + str(H * j + h * np.tan(alpha * 2. * np.pi/360.)/np.sqrt(2.)) + " " + str( H * i + h * np.tan(alpha * 2. * np.pi/360.)/np.sqrt(2.)) + " " + str ( k * h / g) + "\n")
                                else:
                                    f.write(str(node_nr) + " " + str(H * j) + " " + str( H * i ) + " " + str ( k * h / g) + "\n")

                    f.write("$EndNodes\n")
                    f.write("$Elements\n")
                    f.write(str(n_elems) + "\n")
                    for k in range(g):
                        for i in range(int(1/H)):
                            for j in range(int(1/H)):
                                elem_nr = j + int( 1 / H  ) * i +  int( 1 / H  )**2 * k + 1
                                node_nr = elem_nr + i + k * int(2 / H) + k
                                f.write(str(node_nr) + " 5 0 " + str(node_nr) + " " + str(node_nr + 1) + " " + str(node_nr + 1 + int(1 / H + 1)) + " " + str(node_nr  + int(1 / H + 1)))
                                f.write(" " + str(node_nr + int( 1 / H + 1 )**2) + " " + str(node_nr + 1 + int( 1 / H + 1 )**2) + " " + str(node_nr + 1 + int(1 / H + 1) + int( 1 / H + 1 )**2) + " " + str(node_nr + int(1 / H + 1) + int( 1 / H + 1 )**2) + "\n")


                    f.write("$EndElements")




