from utils import read_video, save_video
from trackers import Tracker
import cv2
def main():
    video_frames = read_video("inputs_videos/football_video_01.mp4")

    tracker = Tracker("models/best.pt")

    tracks = tracker.get_object_tracks(video_frames, read_from_stub = True, stub_path = "stubs/track_stubs.pkl")
    
    # # save croppeed image of a players
    # for tracks_id, player in tracks["players"][0].items():
    #     bbox = player["bbox"]
    #     frame = video_frames[0]

    #     # croppeed bbox from images
    #     cropped_image = frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]

    #     # save croppeed image of a players
    #     cv2.imwrite(f"output_videos/cropped_image.jpg", cropped_image)
    
    # Annotate video frames with object tracks
    output_video_frames = tracker.draw_annotations(video_frames, tracks)

    save_video(output_video_frames, "output_videos/output_video.avi")

if __name__ == "__main__":
    main()