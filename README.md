## To setup on Seeed NPI I.MX6ULL board:

#### Install required packages:

```
sudo apt-get update
sudo apt install -y python3 python3-pip python3-venv openssh-server git
```

#### Setup python:

```
git clone https://github.com/cstrutton/prodmon
cd prodmon
python3 -m venv venv
source venv/bin/activate
pip install -r requirents.txt
# create directory for sql files
```

#### Add Service Files:

```
# create hard links to service files
sudo ln ./service_files/prodmon-collect.service /ect/systemd/system/prodmon-collect.service
sudo ln ./service_files/prodmon-post.service /ect/systemd/system/prodmon-post.service
sudo ln ./service_files/prodmon-config.service /ect/systemd/system/prodmon-config.service

# enable services
sudo systemctl enable prodmon-collect
sudo systemctl enable prodmon-post
sudo systemctl enable prodmon-config

# reload systemd configuration
sudo systemctl daemon-reload
```

#### Network Configuration:

The image for these boards is Linux 4.19.71-imx-r1 armv7l and is based on Debian buster.
The images are built with Seeed's customized version of the BeagleBoard image builder.
https://github.com/Seeed-Studio/image-builder

`connman` is used to configure networking. (https://wiki.archlinux.org/index.php/ConnMan)

These boards generate a random mac address on each boot. This makes it really hard to use `connman` as services are configured by name and that includes the MAC address.  
To fix the MAC address, add the following to the end of `/boot/uEnv.txt`

```
ethaddr=xx:xx:xx:xx:xx:xx
eth1addr=xx:xx:xx:xx:xx:xx
```

Note that any given service will only be visable if it is connected. Each network port will auto connect with DHCP if it is available.
To set up, I used a DHCP server on my laptop to give an known IP to one port then configured it as below. Then connected to the other port and configured it. Note: ip address changes take effect immediatly and you will need to reconnect.

Use connman interactive mode to configure the PLANT network:

```
root@npi:~# connmanctl
# Plug in the PLANT network and run
connmanctl> services # prints out the name of the plant network
connmanctl> config ethernet_<mac-address>_cable --ipv4 manual 10.2.42.155 255.255.192.0 10.4.1.9
connmanctl> config ethernet_<mac-address>_cable --nameservers 10.4.1.200 10.5.1.200
connmanctl> exit
```

Use connman interactive mode to configure the PLC network:

```
root@npi:~# connmanctl
# Plug in the PLC network and run
connmanctl> services # prints out the name of the networks
connmanctl> config ethernet_<mac-address>_cable --ipv4 manual 192.168.1.254 255.255.255.0
connmanctl> exit
```

## Sources:

- service files:

  - https://www.devdungeon.com/content/creating-systemd-service-files
  - https://www.freedesktop.org/software/systemd/man/systemd.service.html#

- rock pi boot from emmc:

  - https://forum.radxa.com/t/rock-pi-4b-v1-4-no-boot-on-emmc/3812

- Network configuration with connman

  - https://developer.toradex.com/knowledge-base/ethernet-network-(linux)
  - http://variwiki.com/index.php?title=Static_IP_Address

- DHCP server for setup:
  - https://www.dhcpserver.de/cms/download/

## Static IP adresses provided by IT:

| IP          | Machine | MAC               |
| ----------- | ------- | ----------------- |
| 10.4.42.153 | 1533    | d6:89:7c:ec:e0:9e |
| 10.4.42.154 | 1816    | d6:89:7c:ec:e0:a1 |
| 10.4.42.155 |         |                   |
| 10.4.42.156 |         |                   |
| 10.4.42.157 |         |                   |
| 10.4.42.158 |         |                   |
| 10.4.42.160 |         |                   |
| 10.4.42.161 |         |                   |
| 10.4.42.162 |         |                   |
| 10.4.42.163 |         |                   |
| 10.4.42.164 |         |                   |
| 10.4.42.165 |         |                   |
| 10.4.42.166 |         |                   |
| 10.4.42.167 |         |                   |
| 10.4.42.168 |         |                   |
| 10.4.42.169 | 920     | 00:D0:C9:FE:83:5D |

## TODO:

- read config from a file
- read config file from command line
- modify loop to work with different communications systems
  - factor out pylogix
  - add in pymodbus
