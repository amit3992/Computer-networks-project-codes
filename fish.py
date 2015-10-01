from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import *


# Switch numbers is based on order of switch installation.

# Temp rules for AS4 
as4rules = ((match(switch=2, inport=1) >> fwd(2)) + 
            (match(switch=2, inport=3) >> fwd(2)) +
			(match(switch=2, dstip='10.0.0.1') >> fwd(1)) +
			(match(switch=2, dstip='10.0.0.2') >> fwd(3)))

dummynorthrules = ((match(switch=3, inport=1) >> fwd(2)) +
					(match(switch=3, inport=2) >> fwd(1)))
					
dummysouthrules = ((match(switch=4, inport=1) >> fwd(2)) +
					(match(switch=4, inport=2) >> fwd(1)))
        
# Initial rules for as3switch. We forward based on the destination IP
# addresses. The fwd() rule tells us which port to go to. 
as3rules = ((match(switch=1, inport=2) >> fwd(1)) + 
            (match(switch=1, dstip='10.0.0.1') >> fwd(2)) +
            (match(switch=1, dstip='10.0.0.2') >> fwd(3)) +
			(match(switch=1, inport=3) >> fwd(4)) +
			(match(switch=1, inport=4) >> fwd(3)) +
			(match(switch=1, inport=1) >> fwd(2)))
			
fishpolicy = as4rules + as3rules + dummynorthrules + dummysouthrules

def main():
    print "Returning policy:"
    print fishpolicy
    print ""
    return fishpolicy
    
