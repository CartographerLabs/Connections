# Connections

"Connections" is a Python tool for analyzing a social network of users. It provides the ability to add users to the network and analyze their connections and centrality measures.

## Description

Connections uses the `UserNetwork` class to maintain a network graph for each month. Users are represented as nodes in the graph, and their interactions are represented as directed edges. There are two types of interactions: 'following' and 'mentioning' (when a user mentions another user in a post using the '@' symbol).

The class provides methods to:

- Add a user to the network.
- Retrieve the network graph for a specific month.
- Retrieve the 'following' and 'mention' connections for a user in a specific month.
- Retrieve all connections for a user in a specific month.
- Compute centrality measures (degree, closeness, betweenness, and eigenvector centrality) for a user in a specific month.

## Requirements

Connections requires Python 3 and the following Python libraries installed:

- [NetworkX](https://networkx.github.io/)

## Usage
Here is an example of how to use the Connections tool:
```python
from datetime import datetime
from connections import UserNetwork

# Create a UserNetwork instance
un = UserNetwork()

# Add a user to the network
username = "Alice"
date = datetime.now()
following = ["Bob", "Charlie"]
posts = ["Hello world!", "@Bob Hi!"]
un.add_user(username, date, following, posts)

# Get centrality measures for the user
print(un.get_centrality(username, date))

# Get connections for the user
print(un.get_connections(username, date))
```
