# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Aadi Shanker
# aadidevs@uci.edu
# 75948470
import socket
import json


def create_connection(server, port):
  '''
  Handles connection to the server
  '''
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect((server, port))
  return client_socket


def close_connection(client_socket):
  '''
  Closes the given socket connection
  '''
  client_socket.close()


def prepare_data(username, password, message=None, bio=None):
  '''
  Prepare JSON data for sending
  '''
  data_dict = {"username": username, "password": password}
  
  # checks if there is a message
  if message:
    #adds the message
    data_dict["message"] = message
  
  # checks if there is a bio
  if bio:
    # adds the bio
    data_dict["bio"] = bio
  
  # returns json dump
  return json.dumps(data_dict)




def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''
  
  # Establish Connection
  client_socket = create_connection(server, port)

  # Prepare the data
  data_to_send = prepare_data(username, password, message, bio)

  

  # #TODO: return either True or False depending on results of required operation
  # return 
