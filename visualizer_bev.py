# visualizer_bev.py
import matplotlib.pyplot as plt
import numpy as np

def draw_bev(ax, point_cloud, tracks):
    ax.cla()  # clear previous frame

    ax.set_xlim(-50, 50)
    ax.set_ylim(0, 100)
    ax.set_title("Bird's Eye View Tracking")
    ax.set_xlabel('X (left/right, meters)')
    ax.set_ylabel('Y (forward, meters)')

    # Plot point cloud (only XY for BEV)
    if point_cloud is not None:
        ax.scatter(point_cloud[:, 0], point_cloud[:, 1], s=0.2, c='grey')

    # Plot tracked boxes
    for track in tracks:
        x, y, z, l, w, h, ry = track.bbox
        draw_bbox(ax, x, y, l, w, ry, track.id)

    # plt.draw()
    # plt.pause(0.001)  # small pause to update GUI

def draw_bbox(ax, x, y, l, w, ry, track_id):
    # If your ry is in degrees, convert:
    ry = np.radians(ry)

    # Box corners (local frame)
    corners = np.array([
        [ l/2,  w/2],
        [ l/2, -w/2],
        [-l/2, -w/2],
        [-l/2,  w/2]
    ])

    # Rotate
    R = np.array([
        [np.cos(ry), -np.sin(ry)],
        [np.sin(ry),  np.cos(ry)]
    ])
    corners = corners @ R.T

    # Translate
    corners += np.array([x, y])

    # Close the loop
    corners = np.vstack((corners, corners[0]))
    ax.plot(corners[:, 0], corners[:, 1], c='r')

    # Heading arrow
    heading = np.array([l/2, 0.0])
    heading_rot = R @ heading
    ax.arrow(x, y, heading_rot[0], heading_rot[1],
             head_width=0.5, head_length=1.0, fc='g', ec='g')

    # Track ID
    ax.text(x, y, str(track_id), color='blue', fontsize=8)

    # Debug: plot corners
    ax.scatter(corners[:,0], corners[:,1], c='orange', s=10)

