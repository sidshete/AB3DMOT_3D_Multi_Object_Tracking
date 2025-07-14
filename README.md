
# AB3DMOT

A Python implementation of a 3D multi-object tracking pipeline based on Kalman Filter and Hungarian assignment, applied to the KITTI tracking dataset. This repository contains code for 3D tracking, association, evaluation, and visualization in Bird’s Eye View (BEV).

![Uploading output.gif…]()

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
