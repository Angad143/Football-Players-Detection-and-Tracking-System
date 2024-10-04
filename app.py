import streamlit as st
import os
import subprocess

# Path to your Input and Output folders
INPUT_FOLDER = "inputs_videos"
OUTPUT_FOLDER = "outputs_videos"
MAIN_FILE = "main.py"

# Set max upload size to 10 MB
st.set_option('deprecation.showfileUploaderEncoding', False)
st.title("Football Analysis System")

# Upload video file
uploaded_file = st.file_uploader("Upload a football video (Max size 10 MB)", type=["mp4"], accept_multiple_files=False)

if uploaded_file:
    # Save the uploaded video to the Input folder
    with open(os.path.join(INPUT_FOLDER, "video.mp4"), "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("File uploaded successfully!")

# Create 'Analyze' button to trigger the analysis
if st.button("Analyze"):
    # Run the main.py file to perform the analysis
    try:
        st.info("Running analysis... This may take a few moments.")
        subprocess.run(["python", MAIN_FILE], check=True)
        st.success("Analysis complete! Check the Output folder for results.")

        # Display the saved output video after analysis
        output_video_path = os.path.join(OUTPUT_FOLDER, "output_video1.avi")
        if os.path.exists(output_video_path):
            st.video(output_video_path)
        else:
            st.warning("Output video not found!")
    except subprocess.CalledProcessError as e:
        st.error(f"Error during analysis: {e}")


# Optionally, show the saved output video
if os.path.exists(os.path.join(OUTPUT_FOLDER, "output_video1.avi")):
    st.video(os.path.join(OUTPUT_FOLDER, "output_video1.avi"))
