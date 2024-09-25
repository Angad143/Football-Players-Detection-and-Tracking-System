import cv2 
import sys  # Import the sys module to manipulate the Python runtime environment
sys.path.append('../')  # Add the parent directory to the system path to access utility functions
from utils import measure_distance, get_foot_position  

class SpeedAndDistance_Estimator():
    def __init__(self):
        # Initialize class parameters for the speed and distance estimator
        self.frame_window = 5  # Set the number of frames between which the distance is measured
        self.frame_rate = 24  # Set the frame rate (frames per second) of the video

    def add_speed_and_distance_to_tracks(self, tracks):
        # Add speed and distance information to the tracks of objects in the video

        total_distance = {}  # Dictionary to store the total distance covered by each tracked object

        # Iterate through each tracked object (like players) in the video
        for object, object_tracks in tracks.items():
            # Skip ball and referees as we are only interested in players' movements
            if object == "ball" or object == "referees":
                continue

            number_of_frames = len(object_tracks)  # Get the total number of frames for the current object

            # Iterate over frames in batches defined by the frame window
            for frame_num in range(0, number_of_frames, self.frame_window):
                last_frame = min(frame_num + self.frame_window, number_of_frames - 1)  # Define the last frame in the current window

                # Iterate over all track IDs in the current frame
                for track_id, _ in object_tracks[frame_num].items():
                    if track_id not in object_tracks[last_frame]:  # Check if the track ID exists in the last frame of the window
                        continue

                    # Get the transformed start and end positions of the object between frame_num and last_frame
                    start_position = object_tracks[frame_num][track_id]['position_transformed']
                    end_position = object_tracks[last_frame][track_id]['position_transformed']

                    # If either position is None (out of bounds), skip to the next track
                    if start_position is None or end_position is None:
                        continue

                    # Measure the distance covered between the start and end positions
                    distance_covered = measure_distance(start_position, end_position)
                    time_elapsed = (last_frame - frame_num) / self.frame_rate  # Calculate the time elapsed between frames
                    speed_meteres_per_second = distance_covered / time_elapsed  # Calculate speed in meters per second
                    speed_km_per_hour = speed_meteres_per_second * 3.6  # Convert speed to kilometers per hour

                    # Initialize or update the total distance for the current object and track ID
                    if object not in total_distance:
                        total_distance[object] = {}
                    
                    if track_id not in total_distance[object]:
                        total_distance[object][track_id] = 0

                    # Add the distance covered to the total distance for the track ID
                    total_distance[object][track_id] += distance_covered

                    # Update the speed and distance for each frame in the batch
                    for frame_num_batch in range(frame_num, last_frame):
                        if track_id not in tracks[object][frame_num_batch]:  # Skip if the track ID is not present in the current frame batch
                            continue
                        tracks[object][frame_num_batch][track_id]['speed'] = speed_km_per_hour  # Assign calculated speed
                        tracks[object][frame_num_batch][track_id]['distance'] = total_distance[object][track_id]  # Assign total distance covered

    def draw_speed_and_distance(self, frames, tracks):
        # Draw speed and distance information on each frame of the video

        output_frames = []  # Initialize an empty list to store the frames with drawn information

        # Iterate through each frame and add speed and distance data
        for frame_num, frame in enumerate(frames):
            # Iterate through each tracked object in the current frame
            for object, object_tracks in tracks.items():
                # Skip ball and referees as we are only interested in players' movements
                if object == "ball" or object == "referees":
                    continue

                # Iterate through each track ID and its associated information
                for _, track_info in object_tracks[frame_num].items():
                    if "speed" in track_info:  # Check if speed data is available
                        speed = track_info.get('speed', None)  # Get the speed value
                        distance = track_info.get('distance', None)  # Get the distance value
                        if speed is None or distance is None:  # Skip if either value is missing
                            continue

                        # Get the bounding box of the object and calculate the foot position
                        bbox = track_info['bbox']
                        position = get_foot_position(bbox)  # Get the position of the object (near foot)
                        position = list(position)  # Convert the position to a list
                        position[1] += 40  # Adjust the vertical position to draw text below the bounding box

                        position = tuple(map(int, position))  # Convert position back to a tuple of integers
                        # Draw the speed information on the frame at the calculated position
                        cv2.putText(frame, f"{speed:.2f} km/h", position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                        # Draw the distance information below the speed
                        cv2.putText(frame, f"{distance:.2f} m", (position[0], position[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

            output_frames.append(frame)  # Add the annotated frame to the output list

        return output_frames  # Return the list of frames with drawn speed and distance information
