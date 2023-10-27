import numpy as np
import h5py

def readFromHdf(filepath, h):
    # file3D =  "pointplate3D_h2-" + str(int(-np.log2(h))) + "_H2-" + str(int(-np.log2(H))) + "_g2+" + str(int(np.log2(g))) + "_nu" + strnu + "_tetrahedral"
    # with h5py.File("resultsPolyFEM_tetrahedral/" + file3D + "_quartic/result.hdf", "r+") as f:
    with h5py.File(filepath, "r+") as f:

        a_group_key = list(f.keys())[0]

        points = f[a_group_key]['Points']
        pointzz = np.array(points[:])
        displacement = f[a_group_key]['PointData']["solution"]
        dispzz = np.array(displacement[:])
        # print(points[:])


        testpoints = [[1./8. + 1./8. * j, 1./8. + 1./8. * i] for i in range(7) for j in range(7)]
        disp_at_testpoints = np.zeros((3 * 49,3))
        has_mid_layer = False

        for pidx, pts in enumerate(testpoints):

            p0 = np.array([pts[0],pts[1], 0.])
            ph = np.array([pts[0],pts[1], h])
            ph2 = np.array([pts[0],pts[1], 0.5 * h])

            id0 = np.where(np.all(pointzz==p0,axis=1))
            idh = np.where(np.all(pointzz==ph,axis=1))
            idh2 = np.where(np.all(pointzz==ph2,axis=1))

            
            disp_at_testpoints[pidx][:] = dispzz[id0[0][0]]
            
            disp_at_testpoints[pidx + 49][:] = dispzz[:][idh[0][0]]
            try:
                disp_at_testpoints[pidx + 98][:] = dispzz[:][idh2[0][0]]
                has_mid_layer = True
            except IndexError:
                continue

        if not has_mid_layer:
            for pidx, pts in enumerate(testpoints):
                disp_at_testpoints[pidx + 98][:] = (disp_at_testpoints[pidx][:] + disp_at_testpoints[pidx + 49][:])/2
        disp_at_testpoints = disp_at_testpoints.reshape(-1)
        return disp_at_testpoints
    
# file3D =  "pointplate3D_h2-6_H2-5_g2+0_nu00_tetrahedral"
# filepath = "resultsPolyFEM_tetrahedral/" + file3D + "/result.hdf"
# print(readFromHdf(filepath, 2.**(-6.))) 

 