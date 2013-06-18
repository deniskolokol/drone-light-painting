#!/usr/bin/env python

"""
Ctrl app for the AR.Drone.
"""

import time
import sched
from datetime import datetime

# Import drone library from current_location/python-ardrone.
from sys import path
path.append('%s/%s' % (path[0], 'python-ardrone'))
import libardrone

s = sched.scheduler(time.time, time.sleep) # Main scheduler.
drone = libardrone.ARDrone() # Global drone object.

def drone_action(*argument):
    """
    Parse argument and command the drone.
    """
    print "%s:\tDrone %s: %-30s actual time: %s" % (
        argument + (datetime.now().isoformat(),))

    if argument[1] == 'action':
        try:
            getattr(drone, argument[2].strip())()
        except Exception as e:
            # If a dynamic method call fails, simply hover.
            drone.hover()
            print '[%s] %s' % (datetime.now().isoformat(), e)
    elif argument[1] == 'speed':
        try:
            drone.speed = float(argument[2])
        except:
            pass
    else:
        drone.hover()

def score():
    return [
  (0.10000, 'action', 'hover'),
	(1.00000, 'action', 'turn_left'),
	(1.52000, 'action', 'move_forward'),
	(2.49098, 'action', 'turn_right'),
	(3.09098, 'action', 'move_forward'),
	(6.24851, 'action', 'turn_left'),
	(6.72851, 'action', 'move_forward'),
	(8.86318, 'action', 'turn_right'),
	(9.32318, 'action', 'move_forward'),
	(10.01744, 'action', 'turn_right'),
	(10.41744, 'action', 'move_forward'),
	(11.07349, 'action', 'turn_right'),
	(11.39349, 'action', 'move_forward'),
	(12.00406, 'action', 'turn_right'),
	(12.30406, 'action', 'move_forward'),
	(12.90439, 'action', 'turn_right'),
	(13.22439, 'action', 'move_forward'),
	(13.83497, 'action', 'turn_right'),
	(14.29497, 'action', 'move_forward'),
	(14.98923, 'action', 'turn_right'),
	(15.32923, 'action', 'move_forward'),
	(15.95052, 'action', 'turn_right'),
	(16.21052, 'action', 'move_forward'),
	(17.28253, 'action', 'turn_right'),
	(17.58253, 'action', 'move_forward'),
	(18.66493, 'action', 'turn_right'),
	(18.90493, 'action', 'move_forward'),
	(19.97226, 'action', 'turn_left'),
	(20.25226, 'action', 'move_forward'),
	(20.91438, 'action', 'turn_left'),
	(21.17438, 'action', 'move_forward'),
	(21.75576, 'action', 'turn_left'),
	(22.07576, 'action', 'move_forward'),
	(23.05368, 'action', 'hover'),
	(23.85368, 'action', 'move_up'),
	(24.85368, 'action', 'hover'),
	(25.65368, 'action', 'turn_right'),
	(28.43368, 'action', 'move_forward'),
	(31.97016, 'action', 'turn_right'),
	(32.29016, 'action', 'move_forward'),
	(32.90074, 'action', 'turn_right'),
	(33.30074, 'action', 'move_forward'),
	(33.95678, 'action', 'turn_right'),
	(34.49678, 'action', 'move_forward'),
	(35.27473, 'action', 'turn_left'),
	(35.71473, 'action', 'move_forward'),
	(37.39591, 'action', 'hover'),
        (40.00000, 'action', 'land'),
        ]

def main():
    running = True
    while running:
        for event in score():
            s.enter(event[0], 1, drone_action, event)

        s.run()
        running = False        

    print "Shutting down...",
    drone.halt()
    print "Ok."

if __name__ == '__main__':
    main()
