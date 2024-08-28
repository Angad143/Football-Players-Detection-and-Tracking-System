from utils import read_video, save_video

def main():
    video_frame = read_video("inputs_videos/football_video_01.mp4")

    save_video(video_frame, "output_videos/output_video.avi")

if __name__ == "__main__":
    main()