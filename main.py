import datetime
import random
import re
import string
import networkx as nx
from collections import defaultdict


# Function to generate a random username
def generate_username():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


# Function to generate a random post
def generate_post():
    return ' '.join('@' + generate_username() if random.random() < 0.1 else generate_username()
                    for _ in range(random.randint(5, 15)))


# Function to generate a list of random posts
def generate_posts():
    return [generate_post() for _ in range(random.randint(1, 5))]


# Function to generate a list of random followees
def generate_followees():
    return [generate_username() for _ in range(random.randint(1, 5))]


class UserNetwork:
    """Class to represent a social network of users."""

    def __init__(self):
        """Initialize an empty dictionary to hold the network graphs."""
        self.networks = {}

    def add_user(self, username, date, following, posts):
        """
        Add a user to the network graph for a specific month.

        Parameters:
            username (str): the username of the user
            date (datetime): the date when the user data was collected
            following (list): the list of users that the user is following
            posts (list): the list of posts made by the user
        """

        # Get the month from the date
        month = date.strftime('%Y-%m')

        # Create a new graph for the month if it doesn't exist
        if month not in self.networks:
            self.networks[month] = nx.DiGraph()

        # Add the user to the graph
        self.networks[month].add_node(username, following=following, posts=posts)

        # Add edges for 'following' connections
        for followee in following:
            self.networks[month].add_edge(username, followee, connection='following')

        # Add edges for 'mention' connections
        for post in posts:
            mentions = re.findall(r'@(\w+)', post)
            for mention in mentions:
                self.networks[month].add_edge(username, mention, connection='mention')

    def get_network(self, date):
        """
        Get the network graph for a specific month.

        Parameters:
            date (datetime): the date of the graph to retrieve

        Returns:
            DiGraph: the network graph for the specified month, or None if no such graph exists
        """

        # Get the month from the date
        month = date.strftime('%Y-%m')

        # Return the network graph for the month
        return self.networks.get(month)

    def get_connections(self, username, date):
        """
        Get the 'following' and 'mention' connections for a user in a specific month.

        Parameters:
            username (str): the username of the user
            date (datetime): the date of the graph to use

        Returns:
            tuple: two dictionaries mapping target usernames to the number of 'following' and 'mention' connections
        """

        # Get the month from the date
        month = date.strftime('%Y-%m')

        # Get the graph for the month
        graph = self.networks.get(month)

        if graph is None:
            return None

        # Get the edges for the user
        edges = graph.edges(username, data=True)

        # Split the edges by connection type
        following = defaultdict(int)
        mention = defaultdict(int)
        for _, target, data in edges:
            if data['connection'] == 'following':
                following[target] += 1
            elif data['connection'] == 'mention':
                mention[target] += 1

        return following, mention

    def get_all_connections(self, username, date):
        """
        Get all connections for a user in a specific month.

        Parameters:
            username (str): the username of the user
            date (datetime): the date of the graph to use

        Returns:
            list: a list of usernames that the user is connected to
        """

        # Get the dictionaries of 'following' and 'mention' connections
        following, mention = self.get_connections(username, date)

        # Return a list of all connections
        return list(following.keys()) + list(mention.keys())

    def get_centrality(self, username, date):
        """
        Compute centrality measures for a user in a specific month.

        Parameters:
            username (str): the username of the user
            date (datetime): the date of the graph to use

        Returns:
            dict: a dictionary mapping centrality measure names to values
        """

        # Get the month from the date
        month = date.strftime('%Y-%m')

        # Get the graph for the month
        graph = self.networks.get(month)

        if graph is None:
            return None

        # Compute centrality measures
        degree_centrality = nx.degree_centrality(graph)
        closeness_centrality = nx.closeness_centrality(graph)
        betweenness_centrality = nx.betweenness_centrality(graph)

        # Compute eigenvector centrality and handle potential convergence error
        try:
            eigenvector_centrality = nx.eigenvector_centrality(graph)
        except nx.PowerIterationFailedConvergence:
            eigenvector_centrality = None

        # Return the centrality measures
        return {
            'degree': degree_centrality.get(username),
            'closeness': closeness_centrality.get(username),
            'betweenness': betweenness_centrality.get(username),
            'eigenvector': eigenvector_centrality and eigenvector_centrality.get(username),
        }


# Create a UserNetwork instance
un = UserNetwork()

# Add users to the network and store their usernames
usernames = []
for month_delta in range(3):
    date = datetime.datetime.now() - datetime.timedelta(days=30 * month_delta)
    for _ in range(20):
        username = generate_username()
        un.add_user(username, date, generate_followees(), generate_posts())
        usernames.append(username)

# Pick a username from the list
username = usernames[0]

# Get centrality measures for a user
centrality = un.get_centrality(username, datetime.datetime.now())

# Get connections for a user
connections = un.get_all_connections(username, datetime.datetime.now())

print(f"Centrality measures for {username}: {centrality}")
print(f"Connections for {username}: {connections}")
