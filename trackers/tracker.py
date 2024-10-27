from ultralytics import YOLO  
import supervision as sv  
import pickle 
import os 
import cv2
import pandas as pd
import numpy as np
import sys
sys.path.append("../")
from utils import get_center_of_bbox, get_bbox_width, get_foot_position

class Tracker:
    def __init__(self, model_path):
        # Initialize the Tracker class with a YOLO model and a ByteTrack object
        self.model = YOLO(model_path)  
        self.tracker = sv.ByteTrack() 

    def add_position_to_tracks(self, tracks):
        """
        Adds the position of detected objects to the tracking information.
        Positions are determined based on the object type (ball or player/referee).
        """
        # Iterate through each type of object (e.g., players, referees, ball)
        for obj_type, object_tracks in tracks.items():
            # Iterate through each frame's tracks
            for frame_num, track in enumerate(object_tracks):
                # Iterate through each track ID in the current frame
                for track_id, track_info in track.items():
                    bbox = track_info['bbox']  # Get bounding box for the track
                    # Determine position based on object type
                    if obj_type == 'ball':
                        position = get_center_of_bbox(bbox)  # Use the center of the bbox for the ball
                    else:
                        position = get_foot_position(bbox)  # Use the foot position for players/referees
                    tracks[obj_type][frame_num][track_id]['position'] = position  # Update position in tracks
                    

    def interpolate_ball_positions(self, ball_positions):
        """
        Interpolates missing ball positions to ensure continuity in the tracking data.
        
        Parameters:
        - ball_positions (list): List of dictionaries containing ball bounding boxes for each frame.
        
        Returns:
        - ball_positions (list): List of dictionaries with interpolated ball positions.
        """
        ball_positions = [x.get(1, {}).get('bbox', []) for x in ball_positions]  # Extract bounding boxes
        df_ball_positions = pd.DataFrame(ball_positions, columns=['x1', 'y1', 'x2', 'y2'])  # Create DataFrame

        # Interpolate missing values
        df_ball_positions = df_ball_positions.interpolate()  # Interpolate missing values
        df_ball_positions = df_ball_positions.bfill()  # Backfill any remaining missing values

        # Convert back to original format
        ball_positions = [{1: {"bbox": x}} for x in df_ball_positions.to_numpy().tolist()]  

        return ball_positions

    def detect_frames(self, frames):
        # Detect objects in the given frames using the YOLO model
        batch_size = 20  
        detections = []  
        for i in range(0, len(frames), batch_size):
            # Predict detections for a batch of frames
            detections_batch = self.model.predict(frames[i: i+batch_size], conf=0.1)

            # Append the batch detections to the overall list
            detections = detections + detections_batch  
        return detections  
    
    def get_object_tracks(self, frames, read_from_stub=False, stub_path=None):
        # Track objects across frames and optionally read/write tracks from/to a stub file
        
        # Check if we should read tracks from a stub file
        if read_from_stub and stub_path is not None and os.path.exists(stub_path):
            with open(stub_path, 'rb') as f:
                tracks = pickle.load(f) 
            return tracks 

        # Get detections from frames
        detections = self.detect_frames(frames)  

        # Initialize a dictionary to store tracks for players, referees, and the ball
        tracks = {
            "players": [],
            "referees": [],
            "ball": []
        }

        for frame_num, detection in enumerate(detections):
            # Invert the class names dictionary for easier lookup
            cls_names = detection.names
            cls_names_inv = {v: k for k, v in cls_names.items()}

            # Convert YOLO detections to supervision format
            detection_supervision = sv.Detections.from_ultralytics(detection)

            # Convert 'goalkeeper' class to 'player' class for tracking purposes
            for object_ind, class_id in enumerate(detection_supervision.class_id):
                if cls_names[class_id] == "goalkeeper":
                    detection_supervision.class_id[object_ind] = cls_names_inv["player"]

            # Update the tracker with the current frame's detections
            detection_with_tracks = self.tracker.update_with_detections(detection_supervision)

            # Initialize empty dictionaries for the current frame's tracked objects
            tracks["players"].append({})
            tracks["referees"].append({})
            tracks["ball"].append({})

            # Process tracked objects
            for frame_detection in detection_with_tracks:
                bbox = frame_detection[0].tolist()  # Get the bounding box coordinates
                cls_id = frame_detection[3]  # Get the class ID of the object
                track_id = frame_detection[4]  # Get the tracking ID

                # Store player tracks
                if cls_id == cls_names_inv['player']:
                    tracks["players"][frame_num][track_id] = {"bbox": bbox}
                
                # Store referee tracks
                if cls_id == cls_names_inv['referee']:
                    tracks["referees"][frame_num][track_id] = {"bbox": bbox}
            
            # Process the ball's bounding box separately
            for frame_detection in detection_supervision:
                bbox = frame_detection[0].tolist()  # Get the bounding box coordinates
                cls_id = frame_detection[3]  # Get the class ID of the object

                # Store ball tracks
                if cls_id == cls_names_inv['ball']:
                    tracks["ball"][frame_num][1] = {"bbox": bbox}

        # Optionally save the tracks to a stub file
        if stub_path is not None:
            with open(stub_path, 'wb') as f:
                pickle.dump(tracks, f)  # Save the tracks dictionary to a file

        return tracks  # Return the dictionary of tracks
    
    
    def draw_ellipse(self, frame, bbox, color, track_id=None):
        """
        Draws an ellipse around an object in the frame.
        
        Parameters:
        - frame (ndarray): The video frame to draw on.
        - bbox (list): Bounding box coordinates [x1, y1, x2, y2].
        - color (tuple): Color for the ellipse (BGR format).
        - track_id (int): Optional track ID to display.
        
        Returns:
        - frame (ndarray): The annotated frame.
        """
        y2 = int(bbox[3])  # Bottom y-coordinate of the bounding box
        x_center, _ = get_center_of_bbox(bbox)  # Center x-coordinate of the bounding box
        width = get_bbox_width(bbox)  # Width of the bounding box

        # Draw an ellipse around the object
        cv2.ellipse(
            frame,
            center=(x_center, y2),
            axes=(int(width), int(0.35 * width)),
            angle=0.0,
            startAngle=-45,
            endAngle=235,
            color=color,
            thickness=2,
            lineType=cv2.LINE_4
        )

        # Draw a rectangle with the track ID if provided
        rectangle_width = 40
        rectangle_height = 20
        x1_rect = x_center - rectangle_width // 2
        x2_rect = x_center + rectangle_width // 2
        y1_rect = (y2 - rectangle_height // 2) + 15
        y2_rect = (y2 + rectangle_height // 2) + 15

        if track_id is not None:
            cv2.rectangle(frame,
                          (int(x1_rect), int(y1_rect)),
                          (int(x2_rect), int(y2_rect)),
                          color,
                          cv2.FILLED)
            
            x1_text = x1_rect + 12
            if track_id > 99:
                x1_text -= 10
            
            cv2.putText(
                frame,
                f"{track_id}",
                (int(x1_text), int(y1_rect + 15)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 0),
                2
            )

        return frame
    

    def draw_triangle(self, frame, bbox, color):
        """
        Draws a triangle around an object in the frame.
        
        Parameters:
        - frame (ndarray): The video frame to draw on.
        - bbox (list): Bounding box coordinates [x1, y1, x2, y2].
        - color (tuple): Color for the triangle (BGR format).
        
        Returns:
        - frame (ndarray): The annotated frame.
        """
        y = int(bbox[1])  # Top y-coordinate of the bounding box
        x, _ = get_center_of_bbox(bbox)  # Center x-coordinate of the bounding box

        # Define the triangle points
        triangle_points = np.array([
            [x, y],
            [x - 10, y - 20],
            [x + 10, y - 20],
        ])
        
        # Draw the filled triangle
        cv2.drawContours(frame, [triangle_points], 0, color, cv2.FILLED)
        cv2.drawContours(frame, [triangle_points], 0, (0, 0, 0), 2)  # Draw the border of the triangle

        return frame
    
    def draw_team_ball_control(self, frame, frame_num, team_ball_control):
        """
        Draws the ball control statistics for both teams on the frame.
        
        Parameters:
        - frame (ndarray): The video frame to draw on.
        - frame_num (int): The current frame number.
        - team_ball_control (pd.Series): Series indicating which team had ball control in each frame.
        
        Returns:
        - frame (ndarray): The annotated frame.
        """
        # Draw a semi-transparent rectangle for displaying statistics
        overlay = frame.copy()
        cv2.rectangle(overlay, (1350, 850), (1900, 970), (255, 255, 255), -1)
        alpha = 0.4
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        # Slice control data up to current frame
        team_ball_control_till_frame = team_ball_control[:frame_num + 1]  

        # Calculate the number of frames each team had ball control
        team_1_num_frames = team_ball_control_till_frame[team_ball_control_till_frame == 1].shape[0]
        team_2_num_frames = team_ball_control_till_frame[team_ball_control_till_frame == 2].shape[0]
        team_1 = team_1_num_frames / (team_1_num_frames + team_2_num_frames)
        team_2 = team_2_num_frames / (team_1_num_frames + team_2_num_frames)

        # Display the ball control percentages on the frame
        # Using red color for Team 1 Ball Control
        cv2.putText(frame, f"Team 1 Ball Control: {team_1 * 100:.2f}%", (1400, 900), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        # Using green color for Team 2 Ball Control
        cv2.putText(frame, f"Team 2 Ball Control: {team_2 * 100:.2f}%", (1400, 950), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

        return frame
    
    
    def draw_annotations(self, video_frames, tracks, team_ball_control):
        """
        Draws annotations on video frames including object tracking and ball control statistics.
        
        Parameters:
        - video_frames (list): List of video frames (images) to annotate.
        - tracks (dict): Dictionary containing tracking information for players, referees, and ball.
        - team_ball_control (pd.Series): Series indicating which team had ball control in each frame.
        
        Returns:
        - output_video_frames (list): List of annotated video frames.
        """
        output_video_frames = []  # List to store annotated frames

        # Process each frame
        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()  # Make a copy of the frame to draw on

            player_dict = tracks["players"][frame_num]  # Get player tracks for the current frame
            ball_dict = tracks["ball"][frame_num]  # Get ball tracks for the current frame
            referee_dict = tracks["referees"][frame_num]  # Get referee tracks for the current frame

            # Draw Players
            for track_id, player in player_dict.items():
                color = player.get("team_color", (0, 255, 0))  # Get color for the player, default is red
                frame = self.draw_ellipse(frame, player["bbox"], color, track_id)  # Draw ellipse around player

                if player.get('has_ball', False):
                    frame = self.draw_triangle(frame, player["bbox"], (0, 0, 255))  # Draw triangle if player has the ball

            # Draw Referee
            for _, referee in referee_dict.items():
                frame = self.draw_ellipse(frame, referee["bbox"], (255, 0, 0))  # Draw ellipse around referee

            # Draw Ball
            for track_id, ball in ball_dict.items():
                frame = self.draw_triangle(frame, ball["bbox"], (0, 255, 0))  # Draw triangle around ball

            # Draw team ball control
            frame = self.draw_team_ball_control(frame, frame_num, team_ball_control)

            output_video_frames.append(frame)  # Add the annotated frame to the output list

        return output_video_frames