from ats.topology import loader
from genie.conf import Genie
import pprint

from genie.libs.parser.iosxr.show_interface import ShowIpInterfaceBrief

pyats_testbed = loader.load('testbed.yaml')
testbed = Genie.init(pyats_testbed)

device = testbed.devices['xrv9k']
device.connect()

output = ShowIpInterfaceBrief(device=device)
parsed_output = output.parse()
pprint.pprint(parsed_output)
