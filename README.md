
# AB3DMOT

A Python implementation of a 3D multi-object tracking pipeline based on Kalman Filter and Hungarian assignment, applied to the KITTI tracking dataset. This repository contains code for 3D tracking, association, evaluation, and visualization in Bird’s Eye View (BEV).

![Demo](docs/output.gif)

---

## 🚀 Project Structure

```
ab3dmot/
│
├── data/                      # 📂 KITTI dataset and detections
├── main_bev.py                # 🚦 Entry point script to run tracking on KITTI sequences
├── configs.py                 # ⚙️ Configuration parameters (e.g. IOU thresholds, max age)
├── tracker.py                 # 🎯 Track class managing Kalman Filter states
├── kalman_filter.py           # 🔄 3D Kalman Filter implementation
├── association.py             # 🔗 Track-to-detection association using Hungarian algorithm
├── utils.py                   # 🧩 Utility functions (3D IoU, box operations)
├── visualizer_bev.py          # 🖼️ BEV visualization of point clouds and tracked objects
├── output/                    # 📸 Output tracking results and visualizations
├── evaluation.py              # 📊 MOT evaluation using motmetrics
└── Kitti2trackers_converter.py # 📥 Convert KITTI labels to tracking format
```

---

## Features

- **3D Object Tracking** using a Kalman Filter state representation with position, velocity, size, and orientation.
- **Data Association** with IoU-based cost matrix and Hungarian algorithm for assignment.
- **Bird’s Eye View (BEV) Visualization** of tracking results over LiDAR point clouds.
- **KITTI Dataset Compatibility**: load detections and ground truth labels from KITTI tracking dataset format.
- **Tracking Performance Evaluation** using MOTChallenge metrics via the `motmetrics` library.
- **Label Conversion Tool** to convert KITTI label files to tracking ground truth format.

---

## Requirements

- Python 3.x  
- numpy  
- scipy  
- matplotlib  
- motmetrics  

Install dependencies with:

```bash
pip install numpy scipy matplotlib motmetrics
```

---

## ⚙️ Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/ab3dmot_tutorial.git
cd ab3dmot_tutorial
```

2. Install required dependencies:

```bash
pip install numpy scipy matplotlib motmetrics
```

3. Download the KITTI Tracking dataset and place detection and label files under the `data/` folder following the expected structure.

---

## 📝 Usage

### Run Tracking on KITTI Sequences

```bash
python main_bev.py
```

- Processes each KITTI sequence in `data/data_tracking_label_2/training/label_02/`
- Saves tracking results to `output/`
- Visualizes tracking in BEV using `matplotlib`

---

### Convert KITTI Labels to Tracking Format

```bash
python Kitti2trackers_converter.py
```

- Converts KITTI label files to the tracking ground truth format.
- Outputs are saved in `converted_gt_tracks/`

---

### Evaluate Tracking Performance

```bash
python evaluation.py
```

- Computes MOT metrics on ground truth and predicted tracks.
- Outputs detailed MOTChallenge metrics summary.

---
### Results

| Seq   | IDF1  | IDP  | IDR  | Rcll | Prcn | GT  | MT  | PT | ML | FP  | FN   | IDs | FM | MOTA | MOTP  | IDt | IDa | IDm |
|-------|-------|------|------|------|------|-----|-----|----|----|-----|------|-----|----|------|-------|-----|-----|-----|
| 0000  | 97.0% | 94.0% | 79.6% | 62.9% | 98.1% | 16 | 13 | 2 | 1 | 13  | 404  | 1   | 0  | 61.6% | 0.008 | 3   | 0   | 2   |
| 0001  | 69.9% | 64.9% | 60.9% | 68.9% | 92.8% | 99 | 95 | 3 | 1 | 230 | 1328 | 29  | 0  | 62.8% | 0.294 | 81  | 5   | 57  |
| 0002  | 98.8% | 94.2% | 84.9% | 69.5% | 96.6% | 21 | 18 | 2 | 1 | 52  | 639  | 4   | 0  | 66.9% | 0.013 | 5   | 0   | 1   |
| 0003  |91.2% | 95.3% | 80.7% | 43.0% | 92.5% | 10 |  9 | 0 | 1 | 30  | 491  | 2   | 0  | 39.3% | 0.015 | 2   | 0   | 0   |
| 0004  | 93.9% | 84.0% | 73.9% | 52.3% | 91.0% | 42 | 37 | 3 | 2 | 104 | 960  | 11  | 1  | 46.6% | 0.141 | 21  | 3   | 13  |
| 0005  | 86.0% | 81.9% | 73.4% | 66.1% | 93.4% | 37 | 36 | 0 | 1 | 101 | 728  | 9   | 0  | 61.0% | 0.062 | 17  | 0   | 8   |
| 0006  | 96.2% | 89.4% | 74.0% | 50.8% | 94.4% | 16 | 14 | 1 | 1 | 44  | 711  | 3   | 0  | 47.6% | 0.212 | 4   | 1   | 2   |
| 0007  | 79.9% | 79.8% | 70.2% | 70.9% | 93.8% | 64 | 63 | 0 | 1 | 175 | 1083 | 18  | 1  | 65.7% | 0.172 | 33  | 1   | 16  |
| 0008  | 92.0% | 92.8% | 76.6% | 63.4% | 95.0% | 29 | 22 | 5 | 2 | 69  | 765  | 4   | 0  | 59.9% | 0.008 | 8   | 1   | 5   |
| 0009  | 73.4% | 70.4% | 63.7% | 69.4% | 94.3% | 90 | 89 | 0 | 1 | 221 | 1623 | 36  | 1  | 64.5% | 0.212 | 73  | 6   | 43  |
| 0010  | 80.9% | 82.0% | 69.8% | 66.7% | 92.2% | 29 | 27 | 0 | 2 | 75  | 440  | 22  | 1  | 59.4% | 0.077 | 27  | 1   | 6   |
| 0011  | 84.2% | 84.4% | 79.4% | 85.1% | 96.0% | 61 | 57 | 2 | 2 | 153 | 650  | 19  | 0  | 81.1% | 0.141 | 34  | 3   | 18  |
| 0012  | 89.0% | 97.5% | 75.7% | 68.1% | 97.2% |  5 |  4 | 0 | 1 | 7   | 113  | 0   | 0  | 66.1% | 0.000 | 0   | 0   | 0   |
| 0013  | 84.3% | 78.0% | 68.9% | 57.7% | 91.0% | 69 | 56 |11 | 2 | 137 | 1020 | 12  | 0  | 51.5% | 0.218 | 37  | 1   | 26  |
| 0014  | 77.6% | 81.0% | 70.2% | 77.6% | 96.0% | 18 | 15 | 2 | 1 | 26  | 179  | 3   | 0  | 73.9% | 0.085 | 6   | 0   | 3   |
| 0015  |92.4% | 93.3% | 83.9% | 62.1% | 97.1% | 27 | 25 | 1 | 1 | 64  | 1323 | 4   | 0  | 60.2% | 0.022 | 9   | 1   | 6   |
| 0016  |95.8% | 97.9% | 92.9% | 74.3% | 98.3% | 29 | 27 | 1 | 1 | 53  | 1064 | 6   | 0  | 72.9% | 0.006 | 7   | 0   | 1   |
| 0017  |90.6% | 97.1% | 88.1% | 57.4% | 97.0% | 12 | 11 | 0 | 1 | 27  | 638  | 1   | 0  | 55.6% | 0.007 | 1   | 0   | 0   |
| 0018  | 84.0% | 92.3% | 75.3% | 76.6% | 96.6% | 22 | 21 | 0 | 1 | 48  | 420  | 3   | 0  | 73.7% | 0.010 | 5   | 0   | 2   |
| 0019  | 88.4% | 86.2% | 79.6% | 77.5% | 97.0% |107 |105 | 1 | 1 | 270 | 2517 | 28  | 0  | 74.8% | 0.054 | 57  | 2   | 31  |
| 0020  | 81.4% | 78.3% | 72.9% | 75.4% | 95.3% |135 |124 | 7 | 4 | 331 | 2187 | 32  | 0  | 71.3% | 0.097 | 94  | 3   | 65  |
| OVERALL | 87.0% | 83.6% | 75.6% | 70.5% | 95.4% | 938 | 868 | 41 | 29 | 2230 | 19283 | 247 | 4 | 66.7% | 0.102 | 524 | 28 | 305 |

| Column   | Meaning                                                                                                       |
| -------- | ------------------------------------------------------------------------------------------------------------- |
| **IDF1** | ID F1 score: The F1 score of correctly identified detections (combines precision & recall for identity).      |
| **IDP**  | ID Precision: Fraction of computed detections that are correctly identified.                                  |
| **IDR**  | ID Recall: Fraction of ground truth detections that are correctly identified.                                 |
| **Rcll** | Recall: Fraction of total ground truth objects that were correctly detected (detection recall).               |
| **Prcn** | Precision: Fraction of detected objects that were correct (detection precision).                              |
| **GT**   | Ground Truth: Number of ground truth tracks/objects.                                                          |
| **MT**   | Mostly Tracked: Tracks covered by the tracker ≥ 80% of their lifespan.                                        |
| **PT**   | Partially Tracked: Tracks covered by the tracker between 20%–80%.                                             |
| **ML**   | Mostly Lost: Tracks covered ≤ 20% of their lifespan.                                                          |
| **FP**   | False Positives: Number of false detections.                                                                  |
| **FN**   | False Negatives: Number of missed detections.                                                                 |
| **IDs**  | Identity Switches: How many times a tracked ID jumps to a different ground truth ID.                          |
| **FM**   | Fragmentations: Number of times a ground truth trajectory is interrupted (the tracker loses then reacquires). |
| **MOTA** | Multi-Object Tracking Accuracy: Combines FP, FN, and IDs into one metric. Higher is better (max 100%).        |
| **MOTP** | Multi-Object Tracking Precision: Average alignment of predicted boxes to ground truth (lower is better).      |
| **IDt**  | ID switches total (sometimes matches **IDs**).                                                                |
| **IDa**  | ID assignments: How many times an ID is reassigned.                                                           |
| **IDm**  | ID merges: How many times two tracks are merged incorrectly.                                                  |


