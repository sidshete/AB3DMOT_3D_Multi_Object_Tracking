import os
import numpy as np
import motmetrics as mm

# === CONFIG ===
GT_DIR = 'converted_gt_tracks'
PRED_DIR = 'output'

# === UTILS ===
def load_sequence(file_path):
    """
    Load a sequence file into a dict: {frame_id: [ (id, [x, y, z]) ]}
    """
    frame_dict = {}
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            frame_id = int(parts[0])
            track_id = int(parts[1])
            # Use center x, y for 2D distance OR x,y,z for 3D
            x, y = float(parts[2]), float(parts[3])
            if frame_id not in frame_dict:
                frame_dict[frame_id] = []
            frame_dict[frame_id].append( (track_id, (x, y)) )
    return frame_dict

def compute_distance_matrix(gt_objs, pred_objs):
    """
    Compute distance matrix for one frame.
    Simple Euclidean distance.
    """
    dists = np.zeros((len(gt_objs), len(pred_objs)), dtype=float)
    for i, (_, gt_pos) in enumerate(gt_objs):
        for j, (_, pred_pos) in enumerate(pred_objs):
            dist = np.linalg.norm(np.array(gt_pos) - np.array(pred_pos))
            dists[i, j] = dist
    return dists

# === MAIN ===
def evaluate_sequence(gt_file, pred_file, dist_threshold=2.0):
    acc = mm.MOTAccumulator(auto_id=True)

    gt_frames = load_sequence(gt_file)
    pred_frames = load_sequence(pred_file)

    all_frames = sorted(set(gt_frames.keys()) | set(pred_frames.keys()))

    for frame_id in all_frames:
        gt_objs = gt_frames.get(frame_id, [])
        pred_objs = pred_frames.get(frame_id, [])

        gt_ids = [obj[0] for obj in gt_objs]
        pred_ids = [obj[0] for obj in pred_objs]

        if len(gt_objs) == 0 or len(pred_objs) == 0:
            dist_matrix = np.zeros((len(gt_objs), len(pred_objs)))
            acc.update(gt_ids, pred_ids, dist_matrix)
            continue

        dist_matrix = compute_distance_matrix(gt_objs, pred_objs)
        dist_matrix[dist_matrix > dist_threshold] = np.nan

        acc.update(gt_ids, pred_ids, dist_matrix)


    return acc

# === LOOP OVER ALL SEQUENCES ===
if __name__ == '__main__':
    seq_files = sorted([f for f in os.listdir(GT_DIR) if f.endswith('.txt')])

    mh = mm.metrics.create()
    accs = []

    for seq_file in seq_files:
        seq_name = seq_file.split('_')[0]
        gt_file = os.path.join(GT_DIR, seq_file)
        pred_file = os.path.join(PRED_DIR, f"{seq_name}_tracks.txt")

        print(f"Evaluating {seq_name}...")
        acc = evaluate_sequence(gt_file, pred_file)
        accs.append(acc)

    summary = mh.compute_many(
        accs,
        names=[f.split('_')[0] for f in seq_files],
        metrics=mm.metrics.motchallenge_metrics,
        generate_overall=True
    )

    print(mm.io.render_summary(
        summary,
        formatters=mh.formatters,
        namemap=mm.io.motchallenge_metric_names
    ))
