import os

def parse_kitti_tracking_label_file(label_file):
    """
    Parse KITTI tracking label file: [frame_id, track_id, type, ...].
    Keeps ALL classes.
    """
    tracking_lines = []

    with open(label_file, 'r') as f:
        for line in f:
            parts = line.strip().split(' ')
            if len(parts) < 15:
                continue

            frame_id = int(parts[0])
            track_id = int(parts[1])
            # No filtering!
            obj_type = parts[2]  # we can keep it for logging if you want

            h, w, l = map(float, parts[8:11])
            x, y, z = map(float, parts[11:14])
            ry = float(parts[14])

            tracking_lines.append([frame_id, track_id, x, y, z, l, w, h, ry])

    return tracking_lines


def batch_convert_kitti_labels(label_dir, output_dir):
    """
    Convert all KITTI label files in label_dir to your tracking format and save in output_dir.
    """
    os.makedirs(output_dir, exist_ok=True)

    files = sorted([f for f in os.listdir(label_dir) if f.endswith('.txt')])

    for filename in files:
        label_path = os.path.join(label_dir, filename)
        output_path = os.path.join(output_dir, filename.replace('.txt', '_gt_tracks.txt'))

        print(f"Converting {filename}...")

        tracking_lines = parse_kitti_tracking_label_file(label_path)

        with open(output_path, 'w') as out_file:
            for line in tracking_lines:
                out_file.write(' '.join(map(str, line)) + '\n')

    print("Conversion done!")

if __name__ == "__main__":
    label_dir = '/home/dfki.uni-bremen.de/sshete/test_codes/AB3DMOT/data/data_tracking_label_2/training/label_02'
    output_dir = './converted_gt_tracks/'

    batch_convert_kitti_labels(label_dir, output_dir)
