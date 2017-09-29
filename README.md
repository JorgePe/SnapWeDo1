# SnapWeDo1
This is a WeDo 1.0 extension for [Snap!](http://snap.berkeley.edu/)

It is based on Connor Hudson (AKA technoboy10) [snap-server](https://github.com/technoboy10/snap-server).

I just converted it to python3 and added the WeDo 1.0 methods from 
Ian Daniher (AKA itdaniher) [WeDoMore](https://github.com/itdaniher/WeDoMore) library.

It still needs some cleaning and improvements but it already works on my Ubuntu laptop and my Raspbery Pi Zero W.


# Requirements

- python 3.x
- WeDoMore

# Installation

WeDoMore:

    mkdir WeDo1  
    cd WeDo1  
    wget https://github.com/gbin/WeDoMore/archive/master.zip  
    unzip master.zip  
    cd WeDoMore-master/  
    sudo python3 ./setup.py install  

SnapWeDo1:

    just download the 'snap-wedo1.py' and 'SnapWeDo1.xml' files and give execution permissions to the first one
    

On Raspberry Pi (and probably also many other linuxes):

Check for the presence of LEGO WeDo 1.0 USB Hub:
```
lsusb
Bus 001 Device 003: ID 0694:0003 Lego Group
```

Create a udev rule to avoid running with root privileges:

```
sudo nano /lib/udev/rules.d/50-LEGOWeDo.rules
```

Just paste this line:
```
ACTION=="add", SUBSYSTEMS=="usb", ATTRS{idVendor}=="0694", ATTRS{idProduct}=="0003", MODE="666", GROUP="plugdev"
```

Then load the new rule:
```
sudo udevadm control --reload
sudo udevadm trigger
```

Now unplug & replug LEGO WeDo 1.0 USB Hub

This assumes you are using 'pi' account. Any other account must also belong to 'plugdev' group:

```
sudo adduser username plugdev
```

Please note that in some linuxes the group can be different, like 'input' instead of 'plugdev'. Just update the udev rule accordingly.


# Usage

Run the python script:
```
$ ./snap-wedo1.py 
Snap! WeDo 1.0 extension by JorgePe
Serving at port 8001
Go ahead and launch Snap!
<a>http://snap.berkeley.edu/snapsource/snap.html</a>
Then import SnapWeDo1.xml containing block definitions for motor and sensors.

```

Then from a browser launch Snap! by navigating to the runtime URL:
http://snap.berkeley.edu/snapsource/snap.html

Then use the menu option 'Import...' and specify the 'SnapWeDo1.xml' file, it contains 3 new custom blocks:
- In 'motion' a 'move motor' block
- In 'sensing' a 'read dist' and a 'read tilt' blocks

You now need to specify the IP Address of your Raspberry Pi to use it.

# Example

Connect a distance sensor on port A and a motor on port B then try this example to make the motor rotate when an object is detected at less than 15 cm of the distance sensor:

![](https://github.com/JorgePe/SnapWeDo1/blob/master/images/example01.png)

This is the expected result:
https://youtu.be/KnzAiFDyu7c

