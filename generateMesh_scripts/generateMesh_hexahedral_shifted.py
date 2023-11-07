import subprocess
import numpy as np
import json
import random

with open("specs.json", "r") as f:
    specs = json.load(f)
    path_to_gmsh_bin = specs["path_to_gmsh_bin"]
    thickness_bounds = specs["thickness_bounds"]
    inplaneRes_bounds = specs["inplaneRes_bounds"]
    outofplaneRes_bounds = specs["outofplaneRes_bounds"]
    shift_angles = specs["shift"]["shift_angles"]
    randomshift = specs["shift"]["randomshift"]

thickness = [ 2.**( - i ) for i in range( thickness_bounds[0], thickness_bounds[1] ) ]
inplaneRes = [ 2.**( -i ) for i in range(inplaneRes_bounds[0], inplaneRes_bounds[1] ) ]
outofplaneRes = [ 2**( i ) for i in range(outofplaneRes_bounds[0], outofplaneRes_bounds[1]) ]

npts_sqrt = 7
coord = 1. / (npts_sqrt + 1.)

for H in inplaneRes:
    for h in thickness:
        for g in outofplaneRes:
            for alpha in shift_angles:
                file3D =  "pointplate3D_h2-" + str(int(-np.log2(h))) + "_H2-" + str(int(-np.log2(H))) + "_g2+" + str(int(np.log2(g))) + "_hexahedral"
                shiftfile3D = file3D + "_shift" + str(alpha)
                if randomshift:
                    shiftfile3D += "_random"
                with open( "meshes/" + file3D + ".msh", "r" ) as f:
                    with open( "meshes/" + shiftfile3D + ".msh", "w" ) as g:
                        nodes = False
                        entities = False
                        for line in f:
                            if line.startswith("$Entities"):
                                entities = True
                            
                            if line.startswith("$Nodes"):
                                nodes = True
                            if line.startswith("$EndNodes"):
                                nodes = False
                            
                            if not entities:
                                if not nodes:
                                    g.write(line)
                                    
                                else:
                                    line = line.strip()
                                    point = line.split(" ")
                                    if len(point) == 3:
                                        x = float(point[0])
                                        y = float(point[1])
                                        z = float(point[2])
                                        if z == h and x!= 0. and x != 1. and y != 0. and y != 1.:
                                            if randomshift:
                                                x += 2 * (random.random() - 0.5) * h * np.tan(alpha * 2. * np.pi/360.)/np.sqrt(2.)
                                                y += 2 * (random.random() - 0.5) * h * np.tan(alpha * 2. * np.pi/360.)/np.sqrt(2.)

                                            else:
                                                x +=  h * np.tan(alpha * 2. * np.pi/360.)/np.sqrt(2.)
                                                y +=  h * np.tan(alpha * 2. * np.pi/360.)/np.sqrt(2.)
                                            line = str(x) + " " + str(y) + " " + str(z)
                                    g.write(line + "\n")

                            if line.startswith("$EndEntities"):
                                entities = False

                                
                        
                        
