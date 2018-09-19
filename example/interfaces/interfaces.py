from ats.topology import loader
from genie.conf import Genie
from genie.libs.conf.interface.iosxr import Interface
import pprint

from genie.libs.parser.iosxr.show_interface import ShowIpInterfaceBrief

# Load setup details
pyats_testbed = loader.load('testbed.yaml')
testbed = Genie.init(pyats_testbed)

# Connect to a device
device = testbed.devices['xrv9k']
device.connect()

# Parse operational output
output = ShowIpInterfaceBrief(device=device)
parsed_output = output.parse()

# Print the output (optional)
pprint.pprint(parsed_output)

# Configure an interface
intf1 = Interface(name='HundredGigE0/0/1/0', device=device)
intf1.description = 'test'
intf1.ipv4 = '203.0.113.11/24'
intf1.ipv6 = '2001:db8:ff::11/64'
cfgs = intf1.build_config()

# See the changes
device.execute('show run int hu0/0/1/0')

device.disconnect()
