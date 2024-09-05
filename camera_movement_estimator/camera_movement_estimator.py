import pickle
import cv2
import numpy as np
import os
import sys
sys.path.append('../') 
from utils import measure_distance, measure_xy_distance  

class CameraMovementEstimator():

    def __init__(self, frame):
        # Initialize the class with the first video frame and setup necessary parameters
        self.minimum_distance = 5  # Minimum movement threshold for considering camera movement

        # Parameters for the Lucas-Kanade optical flow algorithm
        self.lk_params = dict(
            winSize=(15, 15),  # Window size
            maxLevel=2,  # Maximum pyramid levels
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)  # Criteria for termination
        )

        # Convert the first frame to grayscale
        first_frame_grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Create a mask to limit the area where feature points are detected
        mask_features = np.zeros_like(first_frame_grayscale)
        mask_features[:, 0:20] = 1  # Mark the left side of the frame for tracking
        mask_features[:, 900:1050] = 1  # Mark the right side of the frame for tracking

        # Parameters for detecting good features to track (corners)
        self.features = dict(
            maxCorners=100,  # Maximum number of corners to detect
            qualityLevel=0.3,  # Quality level for the corners
            minDistance=3,  # Minimum distance between detected corners
            blockSize=7,  # Size of the neighborhood for corner detection
            mask=mask_features  # Use the custom mask for corner detection
        )

    def add_adjust_positions_to_tracks(self, tracks, camera_movement_per_frame):
        # Adjust the object positions in the tracks according to the camera movement
        for object, object_tracks in tracks.items():
            for frame_num, track in enumerate(object_tracks):
                for track_id, track_info in track.items():
                    position = track_info['position']
                    camera_movement = camera_movement_per_frame[frame_num]
                    # Adjust the position of the object based on the camera movement
                    position_adjusted = (position[0] - camera_movement[0], position[1] - camera_movement[1])
                    tracks[object][frame_num][track_id]['position_adjusted'] = position_adjusted
                    
    def get_camera_movement(self, frames, read_from_stub=False, stub_path=None):
        # If a saved result (stub) is available, load it to avoid recomputing
        if read_from_stub and stub_path is not None and os.path.exists(stub_path):
            with open(stub_path, 'rb') as f:
                return pickle.load(f)

        # Initialize camera movement for each frame
        camera_movement = [[0, 0]] * len(frames)

        # Convert the first frame to grayscale and detect good features to track
        old_gray = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        old_features = cv2.goodFeaturesToTrack(old_gray, **self.features)

        # Loop through the remaining frames
        for frame_num in range(1, len(frames)):
            frame_gray = cv2.cvtColor(frames[frame_num], cv2.COLOR_BGR2GRAY)  # Convert current frame to grayscale
            # Calculate optical flow to get the new positions of the tracked features
            new_features, _, _ = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, old_features, None, **self.lk_params)

            max_distance = 0  # Initialize maximum distance
            camera_movement_x, camera_movement_y = 0, 0  # Initialize camera movement

            # Compare the old and new feature positions to estimate camera movement
            for i, (new, old) in enumerate(zip(new_features, old_features)):
                new_features_point = new.ravel()
                old_features_point = old.ravel()

                # Measure the distance between old and new feature points
                distance = measure_distance(new_features_point, old_features_point)
                if distance > max_distance:
                    max_distance = distance  # Update maximum distance
                    # Measure the X and Y distances between feature points
                    camera_movement_x, camera_movement_y = measure_xy_distance(old_features_point, new_features_point)

            # If the movement exceeds the minimum distance threshold, update the camera movement for this frame
            if max_distance > self.minimum_distance:
                camera_movement[frame_num] = [camera_movement_x, camera_movement_y]
                old_features = cv2.goodFeaturesToTrack(frame_gray, **self.features)  # Detect new features

            old_gray = frame_gray.copy()  # Update the previous frame for the next iteration

        # Save the camera movement to a stub if a path is provided
        if stub_path is not None:
            with open(stub_path, 'wb') as f:
                pickle.dump(camera_movement, f)

        return camera_movement

    def draw_camera_movement(self, frames, camera_movement_per_frame):
        # Overlay camera movement annotations on each frame
        output_frames = []

        for frame_num, frame in enumerate(frames):
            frame = frame.copy()  # Make a copy of the current frame

            # Create an overlay rectangle for the text
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (500, 100), (255, 255, 255), -1)
            alpha = 0.6  # Transparency for the overlay
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)  # Apply the overlay

            # Get the camera movement for the current frame
            x_movement, y_movement = camera_movement_per_frame[frame_num]
            # Annotate the X movement
            frame = cv2.putText(frame, f"Camera Movement X: {x_movement:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
            # Annotate the Y movement
            frame = cv2.putText(frame, f"Camera Movement Y: {y_movement:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)

            output_frames.append(frame)  # Add the annotated frame to the output list

        return output_frames  # Return the list of annotated frames
