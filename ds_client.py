# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Aadi Shanker
# aadidevs@uci.edu
# 75948470
import socket
import json
import time
from ds_protocol import extract_json


def create_connection(server, port):
  '''
  Handles connection to the server
  '''
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect((server, port))
  return client_socket


def prepare_data(username, password):
  '''
  Prepare JSON data for sending
  '''
  data_dict = {"join": {"username": username, "password": password, "token": ""}}
  
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
  client_socket = None
  try:
    # Establish Connection
    client_socket = create_connection(server, port)
    send_stream = client_socket.makefile('w')
    recv_stream = client_socket.makefile('r')

    # Prepare the data
    data_to_send = prepare_data(username, password)
    
    

    # Send the data
    send_stream.write(data_to_send + '\r\n')
    send_stream.flush()

    # Receive the response
    response = recv_stream.readline()
    # print(response)
    response_tuple = extract_json(response)
    

    


    # Process the response
    try:
      
      # Convert the response from JSON format to a Python dictionary
      response_dict = json.loads(response)

      # Check the type of response recieved
      if "response" in response_dict:
        
        if response_dict["response"]["type"] == "ok":
          token = response_tuple.token
          message_msg = json.dumps({"token": token, "post": {"entry": message, "timestamp": str(time.time())}})
          send_stream.write(message_msg + '\r\n')
          send_stream.flush()

          if bio:
            bio_msg = json.dumps({"token": token, "bio": {"entry": bio, "timestamp": str(time.time())}})
            send_stream.write(bio_msg + '\r\n')
            send_stream.flush()

          print("Operation was succsessful")
          return True
        
        elif response_dict["response"]["type"] == "error":
            print(f"Error from server: {response_dict['response']['message']}")
            return False
      
      else:
        print("Unexpected response format.")
        return False
    
    except json.JSONDecodeError:
      print("Failed to decode JSON response.")
      return False

  except Exception as e:
    print(f"An error occurred: {e}")
    return False
  
  finally:
    if client_socket is not None:
      client_socket.close()


# server = "168.235.86.101" # replace with actual server ip address
# port = 3021 # replace with actual port
# send(server, port, "askdnkajsnd", "helloilikethispassword", "Hello World!")
