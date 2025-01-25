import sys
import numpy as np
import open3d as o3d

def main():

    argv = sys.argv
    argc = len(argv)

    print('%s decimates vertices' % argv[0])
    print('%s <ply file> [<decimation factor>]' % argv[0])
    
    if argc < 2:
        quit()

    pcd = o3d.io.read_point_cloud(argv[1])

    sample_factor = 500
    
    if argc > 2:
        sample_factor = int(argv[2])

    points = np.asarray(pcd.points)
    sizeX = np.max(points[:,0]) - np.min(points[:,0])
    sizeY = np.max(points[:,1]) - np.min(points[:,1])
    sizeZ = np.max(points[:,2]) - np.min(points[:,2])

    voxel_size = np.max((sizeX, sizeY, sizeZ)) / sample_factor 

    downsampled = pcd.voxel_down_sample(voxel_size = voxel_size)

    downsampled.estimate_normals(
            search_param = o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

    downsampled.orient_normals_consistent_tangent_plane(10)

    distances = downsampled.compute_nearest_neighbor_distance()

    avg_dist = np.mean(distances)

    radius = 2 * avg_dist

    radii = [radius, radius * 2]

    recMeshBPA = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
            downsampled, o3d.utility.DoubleVector(radii))

    dst_path = 'decimated_%d.ply' % sample_factor
    o3d.io.write_triangle_mesh(dst_path, recMeshBPA)
    print('save %s' % dst_path)

    o3d.visualization.draw_geometries([recMeshBPA])

if __name__ == '__main__':
    main()
