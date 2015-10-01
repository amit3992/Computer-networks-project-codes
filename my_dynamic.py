#!/usr/bin/python

from mininet.cli import CLI
from mininet.log import lg
from mininet.node import Node
from mininet.topolib import TreeNet
from mininet.topo import LinearTopo
from mininet.link import Intf
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import Controller	

if __name__ == '__main__':
    lg.setLogLevel( 'info')
    net = Mininet(controller=Controller)
    info( '*** Adding controller\n' )
    net.addController( 'c0' )
    
    ## Script Parameters ##
    prefixLen = 24 
    hostPernetwork = 2
    Num_Networks=15
    
    #################################### SETUP NETWORKS ####################################
    allNetwork= []      
    
    for nwNumber in range(1,Num_Networks+1):	
	#Create a dictionary for network i
	allNetwork.append({})
	network=allNetwork[nwNumber-1]
	network['id'] = nwNumber	
	
	## Setup the network with id  as nwNumber##
	
	# Add switches
	switchName = 'n%sswitch' % network['id']
	network['switch']  = net.addSwitch(switchName) 
	network['hosts'] = []
	network['allLinks']=[]
	
	# Add hosts and connect them to the switch
	for hNumber in range(1,hostPernetwork + 1): 
		hostIP = '10.0.%s.%s' % (network['id'],hNumber)
		hostName = 'n%sh%s' % (network['id'],hNumber)
		host = net.addHost(hostName, ip= '%s/%s' % (hostIP,prefixLen) )
		net.addLink(host, network['switch'])
		# Add to the host list of the network
		network['hosts'].append(host)
	
	# Add border router
	routerIP =  '10.0.%s.254' % network['id']
	routerName = 'n%sborder' % network['id']
	network['router'] = net.addHost(routerName, ip= '%s/%s' % (routerIP,prefixLen) )
	net.addLink(network['router'], network['switch'])
	
	# Transform host into a router
	network['router'].cmd( 'sysctl net.ipv4.ip_forward=1' )
	print "-->Routing on %s enabled" % network['router'].name
    
    # Point to point link: network i <--> network i+1    
    link_id=1
    print "\n-->Creating Links between:"
    for nwNumber in range(1,Num_Networks):
	print "----> %s and %s"  % (nwNumber,nwNumber+1)
	link = net.addLink(allNetwork[nwNumber-1]['router'], allNetwork[nwNumber]['router'] ) 
	link.intf1.setIP('10.62.0.%s/30' % link_id)
	link.intf2.setIP('10.62.0.%s/30' % (link_id+1))
	link_id=link_id+4
	
    ########################### END SETUP NETWORKS ####################################

    # Starts Mininet
    net.start()	 
    
    ## Configure the default gateways for each host and create Bird sockets for each router##
    for nwNumber in range(1,Num_Networks+1):
	
	# Default gateway to router for network i
	for hNumber in range(1,hostPernetwork + 1):
	    hostName = 'n%sh%s' % (allNetwork[nwNumber-1]['id'],hNumber)	
	    net.get(hostName).cmd( 'route add default gw', '10.0.%s.254' % nwNumber)		    
	routerName='n%sborder' % nwNumber
    
	# Create Bird socket for router i
	net.get(routerName).cmd('bird -c rip_bird.conf -s mySocketForn%sborder.ctl' % nwNumber)
    
    info('*** Running CLI\n')
    CLI( net )
    info('*** Stopping network') 
    net.stop()
