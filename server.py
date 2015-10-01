from socket import * # Import socket module from python
serverPort = 12000 # set the port to 12000
serverSocket = socket(AF_INET, SOCK_DGRAM) # Creates the server socket
serverSocket.bind(('',serverPort)) # binds the port number to the server socket
print "The server is ready to receive"
while 1:			# wait for packet arrival
		message,clientAddress = serverSocket.recvfrom(2048) #receives the message from the client
		modifiedMessage = message.upper() # converts message to upper case
		serverSocket.sendto(modifiedMessage,clientAddress) #sends the modified message to client