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

def startNAT( root, inetIntf='eth1', subnet='10.0/8' ):
    """Start NAT/forwarding between Mininet and external network
    root: node to access iptables from
    inetIntf: interface for internet access
    subnet: Mininet subnet (default 10.0/8)="""

    # Identify the interface connecting to the mininet network
    localIntf = root.defaultIntf()

    # Flush any currently active rules
    root.cmd( 'iptables -F' )
    root.cmd( 'iptables -t nat -F' )

    # Create default entries for unmatched traffic
    root.cmd( 'iptables -P INPUT ACCEPT' )
    root.cmd( 'iptables -P OUTPUT ACCEPT' )
    root.cmd( 'iptables -P FORWARD DROP' )

    # Configure NAT
    root.cmd( 'iptables -I FORWARD -i', localIntf, '-d', subnet, '-j DROP' )
    root.cmd( 'iptables -A FORWARD -i', localIntf, '-s', subnet, '-j ACCEPT' )
    root.cmd( 'iptables -A FORWARD -i', inetIntf, '-d', subnet, '-j ACCEPT' )
    root.cmd( 'iptables -t nat -A POSTROUTING -o ', inetIntf, '-j MASQUERADE' )

    # Instruct the kernel to perform forwarding
    root.cmd( 'sysctl net.ipv4.ip_forward=1' )
	
def stopNAT( root ):
    """Stop NAT/forwarding between Mininet and external network"""
    # Flush any currently active rules
    root.cmd( 'iptables -F' )
    root.cmd( 'iptables -t nat -F' )

    # Instruct the kernel to stop forwarding
    root.cmd( 'sysctl net.ipv4.ip_forward=0' )
	
	
if __name__ == '__main__':
	lg.setLogLevel( 'info')

	net = Mininet(controller=Controller)

	info( '*** Adding controller\n' )
	net.addController( 'c0' )
	
	## Script Parameters ##
	prefixLen = 24 # See CIDR (http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing)
	hostPerNetwork = 2 # excluding the router
	#######################
	
	## SETUP NETWORK 1 ##
	network = {}
	network['id'] = 1	
	switchName = 'n%sswitch' % network['id']
	network['switch']  = net.addSwitch(switchName) 
	network['hosts'] = []
	
	# Add hosts and connect them to the switch
	for hNumber in range(1,hostPerNetwork + 1):
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
	
	# Setup NAT for network 1 -- ONLY FOR NETWORK 1
	nat = Node( 'nat', inNamespace=False )	
	link = net.addLink(nat, network['switch'] )	
	natip = '10.0.%s.222' % network['id']
	link.intf1.setIP(natip, prefixLen)

	## END SETUP NETWORK 1 ##
	
	
	## NETWORK 2 ##
	## To complete

	## END SETUP NETWORK 2 ##	
	
	
	
	# Point to point link: network 1 <--> network 2 
	# To complete
	
	# Starts Mininet
	# You cannot add/remove routes on hosts before Mininet has started	
	net.start()	
	startNAT(nat)
		
	# Default gateway to NAT for network 1
	# Only network 1 has access to internet
	net.get('n1h1').cmd( 'route add default gw', natip)
	net.get('n1h2').cmd( 'route add default gw', natip)
	
	# Set static routes
	# Example: net.get('hostName').cmd( 'route add -net x.x.x.x/Y gw IP')
	## To complete
		
	info('*** Running CLI\n')
	CLI( net )
	info('*** Stopping network')
	stopNAT(nat)
	net.stop()
