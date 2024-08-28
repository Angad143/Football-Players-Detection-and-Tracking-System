import cv2

def read_video(video_path):
    # Open the video file using the specified path
    video_capture = cv2.VideoCapture(video_path)
    frames = []  # Initialize an empty list to store video frames
    while True:
        # Capture frame-by-frame from the video
        ret, frame = video_capture.read()
        if not ret:  # If no more frames are left to read, break the loop
            break
        frames.append(frame)  # Append each captured frame to the frames list
    return frames  # Return the list of frames

def save_video(output_video_frames, output_video_path):
    # Define the codec and create a VideoWriter object to save the video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, 24, 
                          (output_video_frames[0].shape[1], output_video_frames[0].shape[0]))
    for frame in output_video_frames:
        out.write(frame)  # Write each frame to the output video file
    out.release()  # Release the VideoWriter object to close the video file
