import numpy as np  
import cv2 

class ViewTransformer():
    def __init__(self):
        court_width = 68  # Define the width of the court in the real world (meters)
        court_length = 23.32  # Define the length of the court in the real world (meters)

        # Define the pixel coordinates of the four vertices on the video frame (the court corners)
        self.pixel_vertices = np.array([[110, 1035], 
                                        [265, 275], 
                                        [910, 260], 
                                        [1640, 915]])
        
        # Define the corresponding real-world coordinates (target vertices) for the four corners of the court
        self.target_vertices = np.array([
            [0, court_width],  # Bottom-left corner in the real world
            [0, 0],  # Top-left corner in the real world
            [court_length, 0],  # Top-right corner in the real world
            [court_length, court_width]  # Bottom-right corner in the real world
        ])

        # Convert the pixel vertices and target vertices to float32 format for OpenCV functions
        self.pixel_vertices = self.pixel_vertices.astype(np.float32)
        self.target_vertices = self.target_vertices.astype(np.float32)

        # Calculate the perspective transformation matrix from pixel coordinates to real-world coordinates
        self.persepctive_trasnformer = cv2.getPerspectiveTransform(self.pixel_vertices, self.target_vertices)


    # Transform the adjusted positions of tracked objects to real-world coordinates
    def add_transformed_position_to_tracks(self, tracks):

        # Loop through each tracked object
        for object, object_tracks in tracks.items():
            for frame_num, track in enumerate(object_tracks):
                # Loop through each track ID and its associated position
                for track_id, track_info in track.items():
                    position = track_info['position_adjusted']  # Get the adjusted position of the object
                    position = np.array(position)  # Convert the position to a NumPy array
                    # Transform the position to real-world coordinates
                    position_transformed = self.transform_point(position)
                    if position_transformed is not None:  # If transformation is successful
                        position_transformed = position_transformed.squeeze().tolist()  # Flatten and convert to list
                    # Add the transformed position to the track
                    tracks[object][frame_num][track_id]['position_transformed'] = position_transformed