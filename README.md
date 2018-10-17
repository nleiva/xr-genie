# xr-genie

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/nleiva/xr-genie)

Getting started with [Genie](https://pubhub.devnetcloud.com/media/pyats-packages/docs/genie/index.html)/[pyATS](https://developer.cisco.com/site/pyats/) and IOS XR

## Running Genie/pyATS in a container

A ([Dockerfile](Dockerfile)) has been added to build a Docker image. Alternatively, you can pull the image from Docker hub: `docker pull nleiva/xr-genie`.

```bash
git clone https://github.com/nleiva/xr-genie.git && cd xr-genie
```

```bash
docker build -t nleiva/xr-genie .
```

To run this image:

```bash
docker run -it --rm --name my-genie nleiva/xr-genie
```

**NOTE**: They keep an official Cisco pyATS Docker image at https://hub.docker.com/r/ciscotestautomation/pyats/.

## IOS XR examples

### Running Python and importing requiered libraries

Once you are in the container, run the Python interpreter (interactive mode) to get immediate feedback for each statement.

```bash
$ docker run -it --rm --name my-genie nleiva/xr-genie
root@9423f2d426d0:/# python
```
```python
Python 3.6.6 (default, Sep  5 2018, 03:51:50)
[GCC 4.9.2] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Import libraries requiered.

```python
from ats.topology import loader
from genie.conf import Genie
from genie.libs.conf.interface.iosxr import Interface
import pprint

from genie.libs.parser.iosxr.show_interface import ShowIpInterfaceBrief
```

### Loading the device(s) details

Load the testbed details. Use the [example](example/interfaces/testbed.yaml) in the repo to create your own, you probably just need to change the target [IP address](example/interfaces/testbed.yaml#L20).

```python
pyats_testbed = loader.load('example/interfaces/testbed.yaml')
testbed = Genie.init(pyats_testbed)
```

### Connecting to the device(s)

Connect to each device. It is very important the device name in the [YAML definition file](example/interfaces/testbed.yaml) matches the hostname on the device’s prompt.

```python
device = testbed.devices['xrv9k']
device.connect()
```

### Getting structured Operational data

Parse the output of `show interfaces brief` using the [Genie Parser](https://github.com/CiscoTestAutomation/genieparser). Take a look at some of the option available for [IOS XR](https://github.com/CiscoTestAutomation/genieparser/tree/master/src/genie/libs/parser/iosxr).

```python
output = ShowIpInterfaceBrief(device=device)
parsed_output = output.parse()
pprint.pprint(parsed_output)
```

If you wanted to grab the IP address of given interface for example:

```python
>>> parsed_output["interface"]["HundredGigE0/0/1/0"]["ip_address"]
'192.0.2.11'
```

### Configuring IOS XR devices

Let's use [Genie Conf](https://github.com/CiscoTestAutomation/genielibs/tree/master/pkgs/conf-pkg/src/genie/libs/conf), a library that provides objects that model the configuration of devices to configure an interface (library already imported in the statements from before)

```python
intf1 = Interface(name='HundredGigE0/0/1/0', device=device)
intf1.description = 'test'
intf1.ipv4 = '203.0.113.11/24'
intf1.ipv6 = '2001:db8:ff::11/64'
cfgs = intf1.build_config()
```

### Validate the changes

You can either run a cli command or repeat the previous process to parse individual fields.

```python
>>> device.execute('show run int hu0/0/1/0')

2018-09-19T20:07:33: %UNICON-INFO: +++ execute command 'show run int hu0/0/1/0' +++
show run int hu0/0/1/0
Wed Sep 19 20:07:33.688 UTC
interface HundredGigE0/0/1/0
 description test
 ipv4 address 203.0.113.11 255.255.255.0
 ipv6 address 2001:db8:ff::11/64
!
```

```python
>>> output = ShowIpInterfaceBrief(device=device)
>>> parsed_output = output.parse()
>>> parsed_output["interface"]["HundredGigE0/0/1/0"]["ip_address"]
'203.0.113.11'
```

### Disconnect

Disconnect.

```python
device.disconnect()
```

## Cleaning up

The container is removed when it exits (--rm). To remove the image:

```bash
docker rmi nleiva/xr-genie
```
