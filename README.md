# **Tools and Libraries Used in Our Project**

<div style="display: flex; flex-wrap: wrap; gap: 10px;">
  <img src="https://img.shields.io/badge/Google%20Colab-blue" alt="Google Colab" style="flex: 1 1 30%;">
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white" alt="OpenCV" style="flex: 1 1 30%;">
  <img src="https://img.shields.io/badge/YOLOv8-FF6F00?style=flat&logo=YOLOv8&logoColor=white" alt="YOLOv8" style="flex: 1 1 30%;">
  <img src="https://img.shields.io/badge/Ultralytics-41b883?style=flat&logo=ultralytics&logoColor=white" alt="Ultralytics" style="flex: 1 1 30%;">
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white" alt="PyTorch" style="flex: 1 1 30%;">
  <img src="https://img.shields.io/badge/K--Means-FF0000?style=flat" alt="K-Means" style="flex: 1 1 30%;">
  <img src="https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white" alt="NumPy" style="flex: 1 1 30%;">
  <img src="https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white" alt="Pandas" style="flex: 1 1 30%;">
  <img src="https://img.shields.io/badge/Matplotlib-003366?style=flat&logo=matplotlib&logoColor=white" alt="Matplotlib" style="flex: 1 1 30%;">
  <img src="https://img.shields.io/badge/Supervision-F7931E?style=flat" alt="Supervision" style="flex: 1 1 30%;">
  <img src="https://img.shields.io/badge/Scikit%20Learn-F7931E?style=flat&logo=scikit-learn&logoColor=white" alt="Scikit Learn" style="flex: 1 1 30%;">
</div>


# Football Players Detection and Tracking

## Introduction
This project detects and tracks football players, referees, and the ball from video footage using advanced AI techniques. It utilizes YOLO (You Only Look Once) for object detection and Kmeans for player classification. The project also calculates each player’s speed and distance covered during a match and measures team possession based on ball control.
<img src="output_videos/tracked_players.png" alt="tracked_players" width="1200" height="400">

## Features
- **Player and Referee Detection**: Uses [YOLOv5](https://github.com/ultralytics/yolov5) to detect players, referees, and footballs in video footage.
- **Team Classification**: Automatically assigns players to teams based on their jersey color using Kmeans clustering.
- **Ball Possession Analysis**: Calculates which team has control of the ball and their percentage of possession.
- **Player Tracking**: Tracks player movements in real-time, measuring distance covered in meters using perspective transformation.
- **Speed and Distance Measurement**: Computes the speed and total distance traveled by each player during the match.

## Datasets
- **Roboflow Football Dataset**: [Football Players Detection](https://universe.roboflow.com/roboflow-jvuqo/football-players-detection-3zvbc/dataset/1)
- **Kaggle Dataset**: [DFL Bundesliga Data Shootout](https://www.kaggle.com/competitions/dfl-bundesliga-data-shootout/data?select=clips)
- **Video Clips**: Videos used from a different source since Kaggle removed them from the dataset: [Input Videos](https://github.com/Angad143/Football-Analysis-Projects/tree/main/Inputs_Videos)

## Technologies Used
- **YOLOv5**: Detects players, referees, and footballs in the video. ([Ultralytics YOLOv5](https://github.com/ultralytics/yolov5))
- **Kmeans Clustering**: Classifies players based on their team colors.
- **Optical Flow**: Tracks camera movement to ensure accurate player tracking.
- **Perspective Transformation**: Converts pixel measurements into real-world meters.
- **OpenCV, NumPy**: Handles video processing, tracking, and numerical computations.

## Installation
To run this project, install the following dependencies:
```bash
pip install ultralytics supervision opencv-python numpy matplotlib pandas
```

## Results
- **YOLO Detection**: Successfully detects and tracks players, referees, and the ball in the video.
- **Speed and Distance Calculation**: Measures the speed and distance covered by each player during the game.


This version now includes the [Ultralytics YOLOv5](https://github.com/ultralytics/yolov5) link for clarity.
