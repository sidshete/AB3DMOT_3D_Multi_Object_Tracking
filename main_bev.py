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
