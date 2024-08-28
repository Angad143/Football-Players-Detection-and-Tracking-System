from ultralytics import YOLO  
import supervision as sv  
import pickle 
import os 

class Tracker:
    def __init__(self, model_path):
        # Initialize the Tracker class with a YOLO model and a ByteTrack object
        self.model = YOLO(model_path)  
        self.tracker = sv.ByteTrack() 

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
