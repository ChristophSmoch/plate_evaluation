import meshio
import os
import numpy as np
thickness = [ 2.**( - i ) for i in range( 6, 20 ) ]
inplaneRes = [ 2.**( -i ) for i in range(5,6) ]


npts_sqrt = 7
coord = 1. / (npts_sqrt + 1.)

for H in inplaneRes:
    for h in thickness:
        file3D =  "pointplate3D_h2-" + str(int(-np.log2(h))) + "_H2-" + str(int(-np.log2(H))) + "_hexahedral_single" 
        with open(file3D + ".geo", "w" ) as f:
            f.write("H = " + str(H) + ";\n")
            f.write("h = " + str(h) + ";\n")
            
            f.write("Point(1) = {0.,0.,0., H};\n")
            f.write("Point(2) = {1.,0.,0., H};\n")
            f.write("Point(3) = {1.,1.,0., H};\n")
            f.write("Point(4) = {0.,1.,0., H};\n")

            f.write("Line(1) = {1,2};\n")
            f.write("Line(2) = {2,3};\n")
            f.write("Line(3) = {3,4};\n")
            f.write("Line(4) = {4,1};\n")
            
            for i in range(npts_sqrt):
                for j in range(npts_sqrt):
                    k = 5 + j + npts_sqrt * i
                    coord1 = coord + j * coord
                    coord2 = coord + i * coord
                    f.write("Point(" + str(k) + ") = {" + str(coord1) + "," + str(coord2) + ",0., H};\n" )

            for i in range(npts_sqrt):
                for j in range(npts_sqrt - 1):
                    point1 = 5 + j + npts_sqrt * i  
                    point2 = 5 + j + npts_sqrt * i + 1
                    k = 9 + j + (2 * npts_sqrt - 1) * i
                    f.write("Line(" + str(k) + ") = {" + str(point1) + "," + str(point2) + "};\n")

            for i in range(npts_sqrt - 1):
                for j in range(npts_sqrt):
                    point1 = 5 + j + npts_sqrt * i
                    point2 = point1 + npts_sqrt
                    k = 9 + npts_sqrt - 1 + j + (2 * npts_sqrt - 1) * i
                    f.write("Line(" + str(k) + ") = {" + str(point1) + "," + str(point2) + "};\n")
            
            f.write("Line(5) = {1,5};\n")
            f.write("Line(6) = {2," + str(4 + npts_sqrt) + "};\n")
            f.write("Line(7) = {3," + str(4 + npts_sqrt**2 ) + "};\n")
            f.write("Line(8) = {4," + str(4 + npts_sqrt**2 - npts_sqrt + 1) + "};\n")


            loop1 = "Curve Loop(1) = {1,6"
            for i in range(npts_sqrt - 1):
                loop1 += ",-" + str(8 + npts_sqrt - 1 - i)
            loop1 += ",-5};\n"
            f.write(loop1)
            f.write("Plane Surface(1) = {1};\n")

            loop2 = "Curve Loop(2) = {2,7"
            for i in range(npts_sqrt - 1):
                loop2 += ",-" + str(8 + 2 * npts_sqrt - 1 + (npts_sqrt - 2 ) * (2 * npts_sqrt - 1) - i * (2 * npts_sqrt - 1) )
            loop2 += ",-6};\n"
            f.write(loop2)
            f.write("Plane Surface(2) = {2};\n")

            loop3 = "Curve Loop(3) = {3,8"
            for i in range(npts_sqrt - 1):
                loop3 += "," + str(9 + (npts_sqrt - 1) * (2 * npts_sqrt - 1) + i)
            loop3 += ",-7};\n"
            f.write(loop3)
            f.write("Plane Surface(3) = {3};\n")

            loop4 = "Curve Loop(4) = {4,5"
            for i in range(npts_sqrt - 1):
                loop4 += "," + str(8 + npts_sqrt + i * (2 * npts_sqrt - 1))
            loop4 += ",-8};\n"
            f.write(loop4)
            f.write("Plane Surface(4) = {4};\n")

            for i in range(npts_sqrt - 1):
                for j in range(npts_sqrt - 1):
                    k = 5 + j + i * (npts_sqrt - 1)
                    line1 = 9 + j + i * (2 * npts_sqrt - 1)
                    line2 = line1 + npts_sqrt
                    line3 = line2 + npts_sqrt - 1
                    line4 = line2 - 1
                    f.write("Curve Loop(" + str(k) + ") = {" + str(line1) + "," + str(line2) + ",-" +str(line3) + ",-" + str(line4) + "};\n" )
                    f.write("Plane Surface(" + str(k) + ") = {" + str(k) + "};\n")
            f.write("Recombine Surface {:};\n")
            # surfloop = "1"
            for i in range(  (npts_sqrt - 1)**2 + 4):
                # surfloop += "," + str(i+1)
                f.write("Extrude {0,0,h} {Surface{" + str(i + 1) + "}; Layers{1}; Recombine;}\n")

        os.system("../../gmsh-4.11.1-Linux64/bin/gmsh -3 " + file3D + ".geo")



