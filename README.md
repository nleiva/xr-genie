# xr-genie

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/nleiva/xr-genie)

Getting started with [Genie](https://pubhub.devnetcloud.com/media/pyats-packages/docs/genie/index.html)/[pyATS](https://developer.cisco.com/site/pyats/) and IOS XR

## Running Genie/pyATS in a container

To run the example on a container image, execute:

```bash
git clone https://github.com/nleiva/xr-genie.git && cd xr-genie
docker run -it --rm --name my-genie quay.io/nleiva/xr-genie
```

**NOTE**: They keep an official Cisco pyATS Docker image at https://hub.docker.com/r/ciscotestautomation/pyats/.

## IOS XR examples

### Running Python and importing required libraries

Once you are in the container, run the Python interpreter (interactive mode) with the command `python3` to get immediate feedback for each statement.

```bash
$ docker run -it --rm --name my-genie quay.io/nleiva/xr-genie
root@9423f2d426d0:/# python3
Python 3.9.9 (main, Nov 22 2021, 00:00:00) 
[GCC 11.2.1 20211019 (Red Hat 11.2.1-6)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

Next, import the libraries required to run this example. Copy & paste this lines to the Python interpreter.

```python
from ats.topology import loader
from genie.conf import Genie
from genie.libs.conf.interface.iosxr import Interface
import pprint

from genie.libs.parser.iosxr.show_interface import ShowIpInterfaceBrief
```

### Loading the device(s) details

Load the testbed details. Use the [example](example/interfaces/testbed.yaml) file in the repo or create your own. If you use the example file, just copy and paste the lines below in the Python interpreter.

```python
pyats_testbed = loader.load('example/interfaces/testbed.yaml')
testbed = Genie.init(pyats_testbed)
```

### Connecting to the device(s)

Connect to the device(s). It is very important the device name(s) in the [YAML definition file](example/interfaces/testbed.yaml) matches the hostname on the device’s prompt. If the DevNet alway-on IOS XR device hostname is different than "iosxr1", this example might not work.

```python
device = testbed.devices['iosxr1']
device.connect()
```

### Getting structured Operational data

Parse the output of `show interfaces brief` using the [Genie Parser](https://github.com/CiscoTestAutomation/genieparser). Take a look at some of the option available for [IOS XR](https://github.com/CiscoTestAutomation/genieparser/tree/master/src/genie/libs/parser/iosxr).

```python
output = ShowIpInterfaceBrief(device=device)
parsed_output = output.parse()
pprint.pprint(parsed_output)
```

If you want to grab the IP address of given interface for example, you can go down the `parsed_output` data tree:

```python
>>> >>> parsed_output["interface"]["GigabitEthernet0/0/0/4"]["ip_address"]
'192.0.2.11'
```

### Configuring IOS XR devices

Let's use [Genie Conf](https://github.com/CiscoTestAutomation/genielibs/tree/master/pkgs/conf-pkg/src/genie/libs/conf), a library that provides objects that model the configuration of devices to configure an interface (library already imported in the statements initially).

```python
intf1 = Interface(name='GigabitEthernet0/0/0/4', device=device)
intf1.description = 'test'
intf1.ipv4 = '203.0.113.11/24'
intf1.ipv6 = '2001:db8:ff::11/64'
cfgs = intf1.build_config()
```

### Validate the changes

You can either run a CLI command or repeat the previous process to parse individual fields.

#### CLI Command:

```python
>>> device.execute('show run int gi0/0/0/4')

2021-12-22 19:17:46,808: %UNICON-INFO: +++ iosxr1 with via 'vty': executing command 'show run int gi0/0/0/4' +++
show run int gi0/0/0/4
Wed Dec 22 19:16:16.970 UTC
interface GigabitEthernet0/0/0/4
description test
ipv4 address 203.0.113.11 255.255.255.0
ipv6 address 2001:db8:ff::11/64
shutdown
!
```

#### Parse a specific field of a command (IP address):

Parse the output of `show interfaces brief` again.

```python
output = ShowIpInterfaceBrief(device=device)
parsed_output = output.parse()
```
    
Then you get the IP from it.

```python
>>> parsed_output["interface"]["GigabitEthernet0/0/0/4"]["ip_address"]
'203.0.113.11'
```

### Disconnect

Finally, disconnect from the device to terminate the SSH connection.

```python
device.disconnect()
```

## Cleaning up

The container instance is removed when it exits (option `--rm`). To remove the container image completely from your system, you can run:

```bash
docker rmi quay.io/nleiva/xr-genie
```

## Building the container image

A ([Dockerfile](Dockerfile)) has been added to build the Conatiner image manually if you prefer to do so instead of pulling it from Quay. You can pre-download the image with `docker pull quay.io/nleiva/xr-genie`.

To build the image you can either use `buildah`:

```bash
buildah bud -t quay.io/nleiva/xr-genie .
```

Or `docker`:

```bash
docker build -t quay.io/nleiva/xr-genie .
```
