from utils import read_video, save_video
from trackers import Tracker
import cv2
import numpy as np
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
from camera_movement_estimator import CameraMovementEstimator
from view_transformer import ViewTransformer

def main():
    # Read the video frames
    video_frames = read_video("inputs_videos/football_video_01.mp4")

    # Initialize the Tracker with the path to the YOLO model
    tracker = Tracker('models/best.pt')

    # Get object tracks from the video frames, optionally loading from a stub file
    tracks = tracker.get_object_tracks(video_frames,
                                       read_from_stub=True,
                                       stub_path='stubs/track_stubs.pkl')
    
    # Add object positions to the tracks
    tracker.add_position_to_tracks(tracks)

    # Initialize the CameraMovementEstimator with the first frame of the video
    camera_movement_estimator = CameraMovementEstimator(video_frames[0])

    # Estimate camera movement per frame, optionally loading from a stub file
    camera_movement_per_frame = camera_movement_estimator.get_camera_movement(video_frames,
                                                                                read_from_stub=True,
                                                                                stub_path='stubs/camera_movement_stub.pkl')

    
    # Adjust positions in tracks based on estimated camera movement
    camera_movement_estimator.add_adjust_positions_to_tracks(tracks, camera_movement_per_frame)
    
    # # save croppeed image of a players
    # for tracks_id, player in tracks["players"][0].items():
    #     bbox = player["bbox"]
    #     frame = video_frames[0]

    #     # croppeed bbox from images
    #     cropped_image = frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]

    #     # save croppeed image of a players
    #     cv2.imwrite(f"output_videos/cropped_image.jpg", cropped_image)
    

    # Interpolate missing ball positions in the tracks
    tracks["ball"] = tracker.interpolate_ball_positions(tracks["ball"])

    # Initialize the TeamAssigner
    team_assigner = TeamAssigner()

    # Assign team colors to players based on their appearance in the first frame
    team_assigner.assign_team_color(video_frames[0], tracks['players'][0])
    
    # Assign teams to players for each frame
    for frame_num, player_track in enumerate(tracks['players']):
        for player_id, track in player_track.items():
            # Determine the team for each player
            team = team_assigner.get_player_team(video_frames[frame_num], 
                                                 track['bbox'],
                                                 player_id)
            # Update the player's team and team color in the track
            tracks['players'][frame_num][player_id]['team'] = team 
            tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_colors[team]

    # Initialize the PlayerBallAssigner
    player_assigner = PlayerBallAssigner()

    # Initialize a list to keep track of ball control by teams
    team_ball_control = []

    # Assign the ball to a player and track team ball control for each frame
    for frame_num, player_track in enumerate(tracks['players']):
        # Get the bounding box of the ball
        ball_bbox = tracks['ball'][frame_num][1]['bbox']
        # Assign the ball to a player based on the ball's bounding box
        assigned_player = player_assigner.assign_ball_to_player(player_track, ball_bbox)

        # Update ball ownership status and team ball control list
        if assigned_player != -1:
            tracks['players'][frame_num][assigned_player]['has_ball'] = True
            team_ball_control.append(tracks['players'][frame_num][assigned_player]['team'])
        else:
            # Maintain the previous team's ball control if no player is assigned
            team_ball_control.append(team_ball_control[-1])
    
    # Convert the list of team ball control to a numpy array
    team_ball_control = np.array(team_ball_control)

    # Annotate video frames with object tracks
    output_video_frames = tracker.draw_annotations(video_frames, tracks, team_ball_control)

    # Annotate video frames with camera movement information
    output_video_frames = camera_movement_estimator.draw_camera_movement(output_video_frames, camera_movement_per_frame)

    save_video(output_video_frames, "output_videos/output_video.avi")

if __name__ == "__main__":
    main()