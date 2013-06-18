drone-light-painting
====================

Light painting with AR Drone quadrocopter

## Description

Quick and dirty implementation of image contour light painting with AR.Drone quadrocopter.

To communicate with the device uses a python-ardrone library, can be found here: https://github.com/venthur/python-ardrone

## Requirements
- numpy
- skimage
- matplotlib
- pygame (only for dronedemo.py)
- python-ardrone (only for dronedemo.py and droneman.py)

### dronelp.py

Takes a jpeg image as input, calculates its contours with given approximation, and based on that creates a “score” for a quadrocopter to fly a trajectory that approximates the contour.

The trajectory is being printed to stdout, just copy-paste for use.

Type for help:

`$ python dronelp.py -h`

### droneman.py

Actually flies the drone. The sample is in the list returned by score() function.

To start type:

`$ python droneman.py`

WARNING! At its current state droneman.py doesn't have any tool for controlling drone while it's flying. Depending on the instructions it can be harmful for your Drone! For test flights use dronedemo.py (see below).

### dronedemo.py

Adapted for drone light painting from demo.py that can be found in the library python-ardrone https://github.com/venthur/python-ardrone. In case something goes wrong while the Drone is flying, keyboard reset stops it, interrupting the score and sending the “hover” command. You can then safely land the drone.

To start type:

`$ python droneman.py`

For additional information on the drone commands, refer to the README of the python-ardrone library.

IT IS STRONGLY RECOMMENDED TO USE THIS SCRIPT FOR TEST FLIGHTS!

## Additional information

Realized as a part of ICAP program at the University of New Mexico, Albuquerque NM.

Author: Denis Kolokol.
