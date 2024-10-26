import streamlit as st
import os
import subprocess

# Path to your Input and Output folders
INPUT_FOLDER = "inputs_videos"
OUTPUT_FOLDER = "output_videos"
MAIN_FILE = "main.py"

# Set max upload size to 200 MB
st.set_option('deprecation.showfileUploaderEncoding', False)

# CSS for rainbow text and upload text
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
    body {
        background-image: url('https://images.unsplash.com/photo-1561154464-b96710408aa1');
        background-size: cover;
        color: #333;
    }
    .rainbow-text {
        font-size: 48px;
        font-weight: bold;
        background: linear-gradient(90deg, red, orange, yellow, green, blue, indigo, violet);
        -webkit-background-clip: text;
        color: transparent;
        margin-bottom: 25px;
    }
    .upload-text {
        font-size: 25px;
        background: linear-gradient(90deg, red, orange, yellow, green, blue, indigo, violet);
        -webkit-background-clip: text;
        color: transparent;
    }
    .emoji {
        font-size: 60px;
        vertical-align: middle;
        margin-right: 5px;
    }
    .container {
        display: flex;
        margin-bottom: 10px;
    }
    </style>
    <div class="container">
        <span class="emoji">⚽</span>
        <h1 class="rainbow-text"><i class="fas fa-futbol"></i> Welcome to Football Analysis System <i class="fas fa-futbol"></i></h1>
        <span class="emoji">⚽</span>
    </div>
    """, unsafe_allow_html=True)

# Initialize session state to track if analysis is complete
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

# Upload video file with increased text size and rainbow gradient
st.markdown(
    "<span class='upload-text'>Please upload your football video (maximum size: 200 MB) for analysis.</span>",
    unsafe_allow_html=True
)
uploaded_file = st.file_uploader("", type=["mp4"], accept_multiple_files=False)

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

        # Set analysis as complete in session state
        st.session_state.analysis_complete = True

    except subprocess.CalledProcessError as e:
        st.error(f"Error during analysis: {e}")

# Show the 'Show Analysis Video' button only if analysis is complete
if st.session_state.analysis_complete:
    if st.button("Show Analysis Video"):
        output_video_path = os.path.join(OUTPUT_FOLDER, "output_video.mp4")
        if os.path.exists(output_video_path):
            # Display the MP4 video in Streamlit
            st.video(output_video_path)
            # Provide a download button
            with open(output_video_path, "rb") as video_file:
                video_bytes = video_file.read()
            st.download_button(
                label="Download Analysis Video",
                data=video_bytes,
                file_name="output_video.mp4",
                mime="video/mp4"
            )
        else:
            st.warning("Output video not found!")
