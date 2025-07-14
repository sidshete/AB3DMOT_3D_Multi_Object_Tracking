import os
import numpy as np
import matplotlib.pyplot as plt

from tracker import Track
from association import associate_tracks
from configs import MAX_AGE, IOU_THRESHOLD, MIN_HITS  # Make sure MIN_HITS is defined somewhere
from visualizer_bev import draw_bev

ROOT_DIR = os.getcwd()
DET_DIR = os.path.join(ROOT_DIR, 'data/data_tracking_label_2/training/label_02/')
VEL_DIR = os.path.join(ROOT_DIR, 'data/data_tracking_velodyne/training/velodyne/')

SEQUENCES = sorted([f for f in os.listdir(DET_DIR) if f.endswith('.txt')])

# Prepare output directory
OUTPUT_DIR = os.path.join(ROOT_DIR, 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.ion()
fig, ax = plt.subplots(figsize=(8, 8))

for seq_file in SEQUENCES:
    seq_id = seq_file.replace('.txt', '')
    print(f"\n=== Sequence: {seq_id} ===")

    # Open output file per sequence (overwrite if exists)
    output_file = os.path.join(OUTPUT_DIR, f'{seq_id}_tracks.txt')
    with open(output_file, 'w') as f:  # open once per sequence
        seq_dets = np.loadtxt(os.path.join(DET_DIR, seq_file), dtype=str)
        seq_dets = seq_dets[seq_dets[:, 0].astype(int).argsort()]
        unique_frames = np.unique(seq_dets[:, 0].astype(int))

        active_tracks = []

        for frame_id in unique_frames:
            frame_dets = seq_dets[seq_dets[:, 0].astype(int) == frame_id]

            # Parse detections: [x, y, z, l, w, h, ry]
            detections = []
            for det in frame_dets:
                h, w, l = float(det[8]), float(det[9]), float(det[10])
                x, y, z = float(det[11]), float(det[12]), float(det[13])
                ry = float(det[14])
                det_vec = [x, y, z, l, w, h, ry]
                detections.append(det_vec)
            detections = np.array(detections)

            # Load point cloud for visualization (optional)
            velodyne_file = os.path.join(VEL_DIR, seq_id, f"{frame_id:06d}.bin")
            point_cloud = None
            if os.path.exists(velodyne_file):
                point_cloud = np.fromfile(velodyne_file, dtype=np.float32).reshape(-1, 4)
                point_cloud = point_cloud[:, :3]

            # 1. Predict existing tracks forward
            for track in active_tracks:
                track.predict()

            # 2. Associate detections to tracks
            matches, unmatched_tracks, unmatched_dets = associate_tracks(
                active_tracks, detections, IOU_THRESHOLD)

            # 3. Update matched tracks with assigned detections
            for track_idx, det_idx in matches:
                active_tracks[track_idx].update(detections[det_idx])

            # 4. Create new tracks for unmatched detections
            for det_idx in unmatched_dets:
                active_tracks.append(Track(detections[det_idx]))

            # 5. Remove tracks that haven't been updated for too long
            active_tracks = [t for t in active_tracks if not t.is_dead(MAX_AGE)]

            # === Save tracks for this frame to file ===
            for track in active_tracks:
                if track.hits >= MIN_HITS:
                    bbox = track.bbox  # should be [x, y, z, l, w, h, ry]
                    f.write(f"{frame_id} {track.id} {bbox[0]:.4f} {bbox[1]:.4f} {bbox[2]:.4f} "
                            f"{bbox[3]:.4f} {bbox[4]:.4f} {bbox[5]:.4f} {bbox[6]:.4f}\n")

            # === Visualization ===
            ax.clear()
            draw_bev(ax, point_cloud, active_tracks)
            ax.set_xlim(-50, 50)
            ax.set_ylim(-50, 50)
            ax.set_xlabel('X (m)')
            ax.set_ylabel('Y (m)')
            ax.set_title(f'Sequence: {seq_id} Frame: {frame_id}')
            ax.grid(True)
            plt.pause(0.01)

            # === Debug print ===
            print(f"Frame {frame_id}: Active track IDs: {[t.id for t in active_tracks]}")
            print(f"Matches: {matches}")
            print(f"Unmatched tracks: {unmatched_tracks}")
            print(f"Unmatched detections: {unmatched_dets}")

plt.ioff()
plt.show()



# import os
# import numpy as np
# import cv2

# from tracker import Track
# from association import associate_tracks
# from configs import MAX_AGE, IOU_THRESHOLD

# from visualizer_bev import BEVVisualizer
# from AB3DMOT.visualizer_3d import LidarVisualizer3D
# from visualizer_image import ImageVisualizer

# ROOT_DIR = '/home/dfki.uni-bremen.de/sshete/test_codes/AB3DMOT/'
# DET_DIR = os.path.join(ROOT_DIR, 'results/')
# VEL_DIR = os.path.join(ROOT_DIR, 'data/data_tracking_velodyne/training/velodyne/')
# IMG_DIR = os.path.join(ROOT_DIR, 'data/data_tracking_image_2/training/image_02/')

# # ---------------------------
# # Initialize visualizers
# # ---------------------------
# bev_vis = BEVVisualizer()
# pcd_vis = LidarVisualizer3D()
# img_vis = ImageVisualizer()

# SEQUENCES = sorted([f for f in os.listdir(DET_DIR) if f.endswith('.txt')])

# for seq_file in SEQUENCES:
#     seq_id = seq_file.replace('.txt', '')
#     print(f"\n=== Sequence: {seq_id} ===")

#     # Load detections for this sequence
#     seq_dets = np.loadtxt(os.path.join(DET_DIR, seq_file), dtype=str)
#     seq_dets = seq_dets[seq_dets[:, 0].astype(int).argsort()]
#     unique_frames = np.unique(seq_dets[:, 0].astype(int))

#     active_tracks = []

#     for frame_id in unique_frames:
#         frame_dets = seq_dets[seq_dets[:, 0].astype(int) == frame_id]

#         detections = []
#         for det in frame_dets:
#             h, w, l = float(det[8]), float(det[9]), float(det[10])
#             x, y, z = float(det[11]), float(det[12]), float(det[13])
#             ry = float(det[14])
#             det_vec = [x, y, z, l, w, h, ry]
#             detections.append(det_vec)
#         detections = np.array(detections)

#         # Predict
#         for track in active_tracks:
#             track.predict()

#         # Associate
#         matches, unmatched_tracks, unmatched_dets = associate_tracks(
#             active_tracks, detections, IOU_THRESHOLD)

#         for track_idx, det_idx in matches:
#             active_tracks[track_idx].update(detections[det_idx])
#         for det_idx in unmatched_dets:
#             active_tracks.append(Track(detections[det_idx]))
#         active_tracks = [t for t in active_tracks if not t.is_dead(MAX_AGE)]

#         # ----------------------------
#         # 1. BEV Visualization
#         # ----------------------------
#         velodyne_file = os.path.join(VEL_DIR, seq_id, f"{frame_id:06d}.bin")
#         point_cloud = None
#         if os.path.exists(velodyne_file):
#             point_cloud = np.fromfile(velodyne_file, dtype=np.float32).reshape(-1, 4)
#             bev_vis.update(active_tracks)

#         # ----------------------------
#         # 2. 3D Point Cloud
#         # ----------------------------
#         if point_cloud is not None:
#             pcd_vis.update(point_cloud[:, :3], active_tracks)

#         # ----------------------------
#         # 3. Image Visualization
#         # ----------------------------
#         image_file = os.path.join(IMG_DIR, seq_id, f"{frame_id:06d}.png")
#         if os.path.exists(image_file):
#             image = cv2.imread(image_file)
#             # ⚠️ Here you need a 3D-to-2D projection to get image boxes!
#             # For this example, we just fake it:
#             for track in active_tracks:
#                 # Replace with real 3D->2D projection
#                 track.image_bbox = [100, 100, 200, 200]  # dummy placeholder
#             img_vis.update(image, active_tracks)

#         print(f"Frame {frame_id} | Tracks: {[t.id for t in active_tracks]}")

# # Cleanup
# bev_vis.close()
# pcd_vis.close()
# img_vis.close()


# # main_bev.py
# import os
# import numpy as np
# from visualizer_bev import draw_bev

# # ROOT = '/home/.../AB3DMOT/'

# VEL_DIR =  'data/data_tracking_velodyne/training/velodyne/'
# LABEL_DIR = 'data/data_tracking_label_2/training/label_02/'

# SEQUENCES = sorted(os.listdir(VEL_DIR))

# def parse_detections(line):
#     parts = line.strip().split()
#     h, w, l = float(parts[8]), float(parts[9]), float(parts[10])
#     x, y, z = float(parts[11]), float(parts[12]), float(parts[13])
#     ry = float(parts[14])
#     return [x, y, z, l, w, h, ry]

# for seq in SEQUENCES:
#     label_file = os.path.join(LABEL_DIR, f"{seq}.txt")
#     with open(label_file) as f:
#         all_labels = f.readlines()

#     frames = sorted(os.listdir(os.path.join(VEL_DIR, seq)))
#     for f in frames:
#         frame_id = int(f.replace('.bin', ''))
#         bin_file = os.path.join(VEL_DIR, seq, f)

#         points = np.fromfile(bin_file, dtype=np.float32).reshape(-1, 4)

#         boxes = []
#         for line in all_labels:
#             if int(line.split()[0]) != frame_id:
#                 continue
#             det = parse_detections(line)
#             boxes.append(det)

#         print(f"SEQ {seq} FRAME {frame_id} | {len(boxes)} boxes")
#         draw_bev(points, boxes)

# main.py

# import os
# import numpy as np

# from tracker import Track
# from association import associate_tracks
# from configs import MAX_AGE, IOU_THRESHOLD
# from visualizer_bev import draw_bev

# # --- Load KITTI labels from file ---
# def load_kitti_labels(label_path):
#     """
#     Parse KITTI label_02 text file, return Nx7 array:
#     [x, y, z, length, width, height, rotation_y]
#     """
#     detections = []
#     if not os.path.exists(label_path):
#         return np.empty((0, 7))  # no detections

#     with open(label_path, 'r') as f:
#         lines = f.readlines()
#     for line in lines:
#         parts = line.strip().split(' ')
#         obj_type = parts[0]
#         if obj_type == 'DontCare':
#             continue
#         try:
#             x = float(parts[11])
#             y = float(parts[12])
#             z = float(parts[13])
#             length = float(parts[8])
#             width = float(parts[9])
#             height = float(parts[10])
#             rotation_y = float(parts[14])
#             detections.append([x, y, z, length, width, height, rotation_y])
#         except:
#             # corrupted line? skip
#             continue
#     if len(detections) == 0:
#         return np.empty((0, 7))
#     return np.array(detections)

# # --- Config ---
# LABEL_DIR = 'data/data_tracking_label_2/training/label_02/'
# OUTPUT_DIR = './output/'

# if not os.path.exists(OUTPUT_DIR):
#     os.makedirs(OUTPUT_DIR)

# frame_files = sorted([f for f in os.listdir(LABEL_DIR) if f.endswith('.txt')])

# active_tracks = []

# for frame_file in frame_files:
#     frame_idx = int(frame_file.split('.')[0])
#     label_path = os.path.join(LABEL_DIR, frame_file)
#     detections = load_kitti_labels(label_path)

#     # Predict existing tracks
#     for track in active_tracks:
#         track.predict()

#     # Associate detections with tracks
#     matches, unmatched_tracks, unmatched_dets = associate_tracks(
#         active_tracks, detections, IOU_THRESHOLD
#     )

#     # Update matched tracks
#     for track_idx, det_idx in matches:
#         active_tracks[track_idx].update(detections[det_idx])

#     # Create new tracks for unmatched detections
#     for det_idx in unmatched_dets:
#         new_track = Track(detections[det_idx])
#         active_tracks.append(new_track)

#     # Remove dead tracks
#     active_tracks = [t for t in active_tracks if not t.is_dead(MAX_AGE)]

#     # Print tracking info
#     print(f"Frame: {frame_file} | Active tracks IDs: {[t.id for t in active_tracks]}")

#     # Draw BEV visualization
#     draw_bev(
#         detections,
#         active_tracks,
#         frame_idx,
#         save_dir=OUTPUT_DIR
#     )

# print(f"\nTracking complete! Visualizations saved in: {OUTPUT_DIR}")
