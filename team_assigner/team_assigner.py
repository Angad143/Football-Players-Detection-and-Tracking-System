from sklearn.cluster import KMeans

# Define the TeamAssigner class
class TeamAssigner:
    def __init__(self):
        # Initialize dictionaries to store team colors and player-to-team assignments
        self.team_colors = {}
        self.player_team_dict = {}
    
    # Method to get a KMeans clustering model based on the provided image
    def get_clustering_model(self, image):
        # Reshape the image into a 2D array where each row is a pixel and columns are RGB values
        image_2d = image.reshape(-1, 3)

        # Perform K-means clustering with 2 clusters
        kmeans = KMeans(n_clusters=2, init="k-means++", n_init=1)
        kmeans.fit(image_2d)

        # Return the trained KMeans model
        return kmeans

    # Method to get the dominant color of the player's uniform within the bounding box (bbox)
    def get_player_color(self, frame, bbox):
        # Crop the player's bounding box from the frame
        image = frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]

        # Extract the top half of the cropped image (where the uniform is more likely to be visible)
        top_half_image = image[0:int(image.shape[0]/2), :]

        # Get a clustering model for the top half image
        kmeans = self.get_clustering_model(top_half_image)

        # Get the cluster labels for each pixel in the top half image
        labels = kmeans.labels_

        # Reshape the labels back to the shape of the top half image
        clustered_image = labels.reshape(top_half_image.shape[0], top_half_image.shape[1])

        # Determine the cluster representing the player's uniform color by analyzing the corner clusters
        corner_clusters = [clustered_image[0, 0], clustered_image[0, -1], clustered_image[-1, 0], clustered_image[-1, -1]]
        non_player_cluster = max(set(corner_clusters), key=corner_clusters.count)
        player_cluster = 1 - non_player_cluster

        # Get the RGB color of the player's uniform cluster
        player_color = kmeans.cluster_centers_[player_cluster]

        # Return the player's uniform color
        return player_color

    # Method to assign team colors based on player detections in the first frame
    def assign_team_color(self, frame, player_detections):
        
        player_colors = []
        # Loop through each player's detection and extract their uniform color
        for _, player_detection in player_detections.items():
            bbox = player_detection["bbox"]
            player_color = self.get_player_color(frame, bbox)
            player_colors.append(player_color)
        
        # Perform K-means clustering on the extracted player colors to identify team clusters
        kmeans = KMeans(n_clusters=2, init="k-means++", n_init=10)
        kmeans.fit(player_colors)

        # Store the trained KMeans model
        self.kmeans = kmeans

        # Assign the cluster centers as the representative colors for two teams
        self.team_colors[1] = kmeans.cluster_centers_[0]
        self.team_colors[2] = kmeans.cluster_centers_[1]

    # Method to get the team ID for a player based on their uniform color
    def get_player_team(self, frame, player_bbox, player_id):
        # If the player ID is already assigned to a team, return the team ID
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id]

        # Get the player's uniform color
        player_color = self.get_player_color(frame, player_bbox)

        # Predict the team ID using the KMeans model
        team_id = self.kmeans.predict(player_color.reshape(1, -1))[0]
        team_id += 1

        # Special condition to manually set the team ID for a specific player ID (91)
        if player_id == 91:
            team_id = 1

        # Store the player's team assignment
        self.player_team_dict[player_id] = team_id

        # Return the team ID
        return team_id
