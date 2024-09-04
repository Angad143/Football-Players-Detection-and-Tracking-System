import sys 
sys.path.append('../')
from utils import get_center_of_bbox, measure_distance

# Define the PlayerBallAssigner class
class PlayerBallAssigner():
    def __init__(self):
        # Initialize a maximum distance threshold for assigning the ball to a player
        self.max_player_ball_distance = 70
    
    # Method to assign the ball to the nearest player within the max distance
    def assign_ball_to_player(self, players, ball_bbox):
        # Calculate the center position of the ball's bounding box
        ball_position = get_center_of_bbox(ball_bbox)

        # Initialize variables to track the minimum distance and the assigned player ID
        minimum_distance = 99999
        assigned_player = -1

        # Loop through each player to calculate the distance to the ball
        for player_id, player in players.items():
            player_bbox = player['bbox']

            # Measure the distance from the ball to the left and right sides of the player's bounding box
            distance_left = measure_distance((player_bbox[0], player_bbox[-1]), ball_position)
            distance_right = measure_distance((player_bbox[2], player_bbox[-1]), ball_position)
            
            # Take the minimum of the two distances as the player's distance to the ball
            distance = min(distance_left, distance_right)

            # Check if the player's distance is within the maximum threshold and is the smallest distance so far
            if distance < self.max_player_ball_distance:
                if distance < minimum_distance:
                    # Update the minimum distance and assign the ball to this player
                    minimum_distance = distance
                    assigned_player = player_id

        # Return the ID of the assigned player, or -1 if no player is close enough
        return assigned_player
