import numpy as np

def convert_to_points(l_block, c_block, dl=0.01, marker_distance = 0.07):
    # initialize block origin
    pt0 = np.array([0.0, 0.0])
    ang0 = 0.0
    sum_l = 0.0


    idx_block = 0
    l = 0.0
    points = []
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

            continue
        
        # add new point on the line
        pt = pt0.copy()

        dif_ang = c_block[idx_block] * l_local
        dif_t = l_local * np.sinc(dif_ang / np.pi)
        dif_n = l_local * np.sinc(0.5 * dif_ang / np.pi) *  np.sin(0.5 * dif_ang)
        pt += dif_t * np.array([ np.cos(ang0), np.sin(ang0)])
        pt += dif_n * np.array([-np.sin(ang0), np.cos(ang0)])
        
        points.append(pt)
        l += dl
    return np.array(points)

if __name__ == '__main__':
    import os
    for raster_path in ['synthetic/'+p for p in os.listdir('synthetic') if p[-4:]=='.csv']:
        l_block, c_block = np.loadtxt(raster_path, delimiter=',').T
        points = convert_to_points(l_block, c_block, dl=0.01)
        np.savetxt(raster_path[:-4]+'_points.txt', points)
        print(raster_path[:-4]+'_points.txt saved')

