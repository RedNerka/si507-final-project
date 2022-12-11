# si507-final-project

The project includes the use of Twitter API v2 OAuth. As a result, a set of keys are needed. TwitterSecrets.py has been uploaded to canvas. In order to run the codes 
correctly, please keep TwitterSecrets.py in the same folder with all other Python codes.  
Be aware, the twitter keys and tokens are generated for personal use. Please discard TwitterSecrets.py after examining the codes immediately.  

## Interaction with the program  
The program interacts with the user from the command line. The main interaction program is in kdTree.py. Please run kdTree.py to start interacting with the program.  
Users have several available interactions to choose from. All inputs are not case-sensitive.  
- The data includes 1106 records of Twitter user information. 24 of them are contributors in five TV works: Band of Brothers, Saving Private Ryan, Braveheart, Mad Max: 
Fury Road, and Good Will Hunting. 1082 of them are the Twitter users that the 24 contributors are following. Users need to enter the index(s) (0-4) to indicate 
Which TV work(s) they want to look up.  
- Quit
  - Kill the process.
- Search By ID
  - Users enter a Twitter user ID into the command line to look up the user information. 
  - If output="ID doesn't exist in database!", the ID is not in the 1106 records.
  - If output="Twitter user not found!", the user with input ID is not found in the chosen TV work(s).
  - If found, the user information will be printed in the command line output.
- Search By Username
  - Users enter a Twitter username into the command line to look up the user information.
  - If output="Username doesn't exist in database!", the username is not in the 1106 records.
  - If output="Twitter user not found!", the user with input username is not found in the chosen TV work(s).
  - If found, the user information will be printed in the command line output.
- Insert
  - If users are querying multiple TV works, insert function is not supported.
  - Users input Twitter user ID.
  - Users input Twitter username.
  - Users input as many key-value pairs for extra information as they like.
  - Users input "no" to stop adding information.
- Range Search
  - Users input the first digit of the ID they want to search as the starting point of the range.
  - Users input the first digit of the ID they want to search as the ending point of the range.
  - Users input the first character of the username they want to search as the starting point of the range.
  - Users input the first character of the username they want to search as the ending point of the range.
  - Users input a number for the number of results they want to see. 
- Get Following
  - Users enter a Twitter username into the command line to look up the users he/she is following.
  - If output="Username doesn't exist in database!", the username is not in the 1106 records.
  - If output="Twitter user not found!", the user with input username is not found in the chosen TV work(s).
  - If found, a list of usernames will be shown in the command line output.
- Find Common Following
  - Users enter two Twitter usernames into the command line to look up the common users they are following.
  - If output="Username doesn't exist in database!", the username is not in the 1106 records.
  - If output="Twitter user not found!", the user with input username is not found in the chosen TV work(s).
  - If found, a list of usernames will be shown in the command line output.\
  - If no common followings, output="No common following users! "
- Return
  - Users enter "return" to return to the previous menu (choosing TV works)
