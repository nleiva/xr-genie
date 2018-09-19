# xr-genie

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

## IOS XR examples

Once you are in the container, run the Python interpreter to run a script in  interactive mode.

```bash
$ docker run -it --rm --name my-genie nleiva/xr-genie:1.0
root@9423f2d426d0:/# python
Python 3.6.6 (default, Sep  5 2018, 03:51:50)
[GCC 4.9.2] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Import libraries requiered.

```python
from ats.topology import loader
from genie.conf import Genie
import pprint

from genie.libs.parser.iosxr.show_interface import ShowIpInterfaceBrief
```

Load the testbed details.

```python
pyats_testbed = loader.load('example/interfaces/testbed.yaml')
testbed = Genie.init(pyats_testbed)
```

Connect to our device.

```python
device = testbed.devices['xrv9k']
device.connect()
```

Parse the output of `show interfaces brief`.

```python
output = ShowIpInterfaceBrief(device=device)
parsed_output = output.parse()
pprint.pprint(parsed_output)
```

If you wanted to grab the IP address of given interface:

```python
>>> parsed_output["interface"]["HundredGigE0/0/1/0"]["ip_address"]
'192.0.2.11'
```

Disconnect.

```python
device.disconnect()
```

### Cleaning up

The container is removed when it exits (--rm). To remove the image:

```bash
docker rmi nleiva/xr-genie
```