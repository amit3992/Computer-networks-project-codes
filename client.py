from socket import * # imports socket module in python 
serverName = "10.0.0.2" # sets the variable serverName to the IP address of the server
serverPort = 12000 # sets the 'serverPort' to a randomly chosen port
clientSocket = socket(AF_INET, SOCK_DGRAM) #creates a socket for the UDP client
message = raw_input('Input lower case: ') # user inputs a sentence in lowercase.
clientSocket.sendto(message,(serverName,serverPort)) #sends the message to the server
modifiedMessage,serverAddress = clientSocket.recvfrom(2048) # receive the modified message
print "Server message: ", modifiedMessage # prints the modified message
clientSocket.close() # closes the client socket