# converter.py

from moviepy.editor import VideoFileClip

def convert_avi_to_mp4(input_path, output_path):
    try:
        # Load the AVI file
        clip = VideoFileClip(input_path)
        # Write the file as MP4
        clip.write_videofile(output_path, codec='libx264')
        print(f"Converted {input_path} to {output_path}")
    except Exception as e:
        print(f"Error during conversion: {e}")
