import numpy as np

def compute_marker_center(point_l, ang_l, marker_distance):
    return point_l + marker_distance * np.array([-np.sin(ang_l), np.cos(ang_l)])


def convert_vector_to_raster(l_block, c_block, dl=0.01, marker_distance = 0.07):
    # initialize block origin
    pt0 = np.array([0.0, 0.0])
    ang0 = 0.0
    sum_l = 0.0


    idx_block = 0
    l = 0.0
    line = []
    marker = [ compute_marker_center(pt0, ang0, -marker_distance) ]
    while idx_block < len(l_block):
        l_local = l - sum_l
        if l_local > l_block[idx_block]:
            # update block origin
            dif_ang = c_block[idx_block]*l_block[idx_block]
            dif_t = l_block[idx_block] * np.sinc(dif_ang / np.pi)
            dif_n = l_block[idx_block] * np.sinc(0.5 * dif_ang / np.pi) * np.sin(0.5 * dif_ang)
            pt0 += dif_t * np.array([ np.cos(ang0), np.sin(ang0)])
            pt0 += dif_n * np.array([-np.sin(ang0), np.cos(ang0)])
            ang0 += c_block[idx_block] * l_block[idx_block]

            sum_l += l_block[idx_block]

            idx_block += 1

            # add new marker
            marker.append(compute_marker_center(pt0, ang0, np.sign(len(l_block) - 0.5 - idx_block) * marker_distance))
            continue
        
        # add new point on the line
        pt = pt0.copy()

        dif_ang = c_block[idx_block] * l_local
        dif_t = l_local * np.sinc(dif_ang / np.pi)
        dif_n = l_local * np.sinc(0.5 * dif_ang / np.pi) *  np.sin(0.5 * dif_ang)
        pt += dif_t * np.array([ np.cos(ang0), np.sin(ang0)])
        pt += dif_n * np.array([-np.sin(ang0), np.cos(ang0)])
        
        line.append(pt)
        l += dl
    return np.array(line), np.array(marker)


if True:
    import os
    for raster_path in ['synthetic/'+p for p in os.listdir('synthetic') if p[-4:]=='.csv']:
        l_block, c_block = np.loadtxt(raster_path, delimiter=',').T
        line, marker = convert_vector_to_raster(l_block, c_block, dl=0.01)
        np.savetxt(raster_path[:-4]+'_line.txt', line)
        print(raster_path[:-4]+'_line.txt saved')

        #import matplotlib.pyplot as plt
        #plt.plot(line[:,0], line[:,1])
        #plt.scatter(marker[:,0], marker[:,1])
        #plt.show()

