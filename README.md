

# Football Players Detection and Tracking

## Introduction
This project detects and tracks football players, referees, and the ball from video footage using advanced AI techniques. It utilizes YOLO (You Only Look Once) for object detection and Kmeans for player classification. The project also calculates each player’s speed and distance covered during a match and measures team possession based on ball control.

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
