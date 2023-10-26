import numpy as np
import json
import h5py

def readFromHdf(filepath, h):
    # file3D =  "pointplate3D_h2-" + str(int(-np.log2(h))) + "_H2-" + str(int(-np.log2(H))) + "_g2+" + str(int(np.log2(g))) + "_nu" + strnu + "_tetrahedral"
    # with h5py.File("resultsPolyFEM_tetrahedral/" + file3D + "_quartic/result.hdf", "r+") as f:
    with h5py.File(filepath, "r+") as f:

        a_group_key = list(f.keys())[0]

        points = f[a_group_key]['Points']
        displacement = f[a_group_key]['PointData']["solution"]
        # print(points[:])


        testpoints = [[1./8. + 1./8. * j, 1./8. + 1./8. * i] for i in range(7) for j in range(7)]
        disp_at_testpoints = np.zeros((3 * 49,3))

        for pidx, pts in enumerate(testpoints):
            for idx, x in enumerate(points[:]):
                if x[0] == pts[0] and x[1] == pts[1] and x[2] == 0.:
                    disp_at_testpoints[pidx][:] = displacement[:][idx]
                    break
            for idx, x in enumerate(points[:]):
                if x[0] == pts[0] and x[1] == pts[1] and x[2] == h:
                    disp_at_testpoints[pidx + 49][:] = displacement[:][idx]
                    break
        for pidx, pts in enumerate(testpoints):
            disp_at_testpoints[pidx + 98][:] = (disp_at_testpoints[pidx][:] + disp_at_testpoints[pidx + 49][:])/2
        return disp_at_testpoints
    
file3D =  "pointplate3D_h2-6_H2-5_g2+0_nu00_tetrahedral"
filepath = "resultsPolyFEM_tetrahedral/" + file3D + "_quartic/result.hdf"
print(readFromHdf(filepath, 2.**(-6.))) 

 