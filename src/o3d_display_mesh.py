import cv2, os, sys
import numpy as np
import open3d as o3d

def main():

    argv = sys.argv
    argc = len(argv)

    print('%s displays mesh file (.ply)' % argv[0])
    print('[usage] python %s <.ply file>' % argv[0])

    if argc < 2:
        quit()

    mesh =  o3d.io.read_triangle_mesh(argv[1])
    mesh.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh])

if __name__ == '__main__':
    main()
