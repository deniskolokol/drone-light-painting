#!/usr/bin/env python

"""
Ctrl app for the AR.Drone.

Adapted from demo.py that comes along with python-ardrone library.
"""

import time
import sched
import pygame
from datetime import datetime

# Import drone library from current_location/python-ardrone
from sys import path
path.append('%s/%s' % (path[0], 'python-ardrone'))
import libardrone

s = sched.scheduler(time.time, time.sleep) # Main scheduler.
drone = libardrone.ARDrone() # Global drone object.

def score():
    return [
        (0.10000, 'speed', 0.2),
  (0.10000, 'action', 'hover'),
	(1.00000, 'action', 'move_forward'),
	(1.52000, 'action', 'turn_right'),
	(1.82000, 'action', 'move_forward'),
	(2.42033, 'action', 'turn_right'),
	(2.48033, 'action', 'move_forward'),
	(3.00378, 'action', 'turn_right'),
	(3.06378, 'action', 'move_forward'),
	(3.58723, 'action', 'turn_right'),
	(3.76723, 'action', 'move_forward'),
	(4.31751, 'action', 'turn_right'),
	(4.39751, 'action', 'move_forward'),
	(4.92362, 'action', 'turn_right'),
	(5.10362, 'action', 'move_forward'),
	(5.65390, 'action', 'turn_left'),
	(6.15390, 'action', 'move_forward'),
	(6.87528, 'action', 'turn_left'),
	(6.95528, 'action', 'move_forward'),
	(7.48140, 'action', 'turn_left'),
	(7.50140, 'action', 'move_forward'),
	(8.02179, 'action', 'turn_left'),
	(8.20179, 'action', 'move_forward'),
	(8.75206, 'action', 'turn_left'),
	(9.15206, 'action', 'move_forward'),
	(9.80811, 'action', 'turn_right'),
	(10.26811, 'action', 'move_forward'),
	(10.96237, 'action', 'turn_right'),
	(11.36237, 'action', 'move_forward'),
	(12.01842, 'action', 'turn_right'),
	(12.33842, 'action', 'move_forward'),
	(12.94899, 'action', 'turn_right'),
	(13.24899, 'action', 'move_forward'),
	(13.84933, 'action', 'turn_right'),
	(14.16933, 'action', 'move_forward'),
	(14.77990, 'action', 'turn_right'),
	(15.23990, 'action', 'move_forward'),
	(15.93416, 'action', 'turn_right'),
	(16.27416, 'action', 'move_forward'),
	(16.89545, 'action', 'turn_right'),
	(17.05545, 'action', 'move_forward'),
	(17.59951, 'action', 'turn_right'),
	(17.69951, 'action', 'move_forward'),
	(18.22904, 'action', 'turn_right'),
	(18.36904, 'action', 'move_forward'),
	(18.90755, 'action', 'turn_right'),
	(19.06755, 'action', 'move_forward'),
	(19.61161, 'action', 'turn_right'),
	(19.69161, 'action', 'move_forward'),
	(20.21773, 'action', 'turn_right'),
	(20.37773, 'action', 'move_forward'),
	(20.92179, 'action', 'turn_right'),
	(21.00179, 'action', 'move_forward'),
	(21.52791, 'action', 'turn_left'),
	(21.76791, 'action', 'move_forward'),
	(22.34062, 'action', 'turn_left'),
	(22.60062, 'action', 'move_forward'),
	(23.18200, 'action', 'turn_left'),
	(23.50200, 'action', 'move_forward'),
	(24.11257, 'action', 'turn_left'),
	(24.21257, 'action', 'move_forward'),
	(24.74210, 'action', 'turn_right'),
	(24.88210, 'action', 'move_forward'),
	(25.17869, 'action', 'hover'),
	(25.97869, 'action', 'move_up'),
	(26.97869, 'action', 'hover'),
	(27.77869, 'action', 'turn_right'),
	(30.55869, 'action', 'move_forward'),
	(37.60306, 'action', 'turn_right'),
	(37.92306, 'action', 'move_forward'),
	(38.53363, 'action', 'turn_right'),
	(38.93363, 'action', 'move_forward'),
	(39.58968, 'action', 'turn_left'),
	(39.62968, 'action', 'move_forward'),
	(40.15122, 'action', 'turn_right'),
	(40.17122, 'action', 'move_forward'),
	(40.69160, 'action', 'turn_left'),
	(41.13160, 'action', 'move_forward'),
	(42.81278, 'action', 'hover')
        ]

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

def start_score():
    for event in score():
        s.enter(event[0], 1, drone_action, event)
    try:
        s.run()
    except (KeyboardInterrupt, SystemExit):
        print('Exiting')
        drone.hover()

def main():
    pygame.init()
    W, H = 320, 240
    screen = pygame.display.set_mode((W, H))
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                drone.hover()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    drone.reset()
                    running = False
                # takeoff / land
                elif event.key == pygame.K_RETURN:
                    drone.takeoff()
                elif event.key == pygame.K_SPACE:
                    drone.land()
                # emergency
                elif event.key == pygame.K_BACKSPACE:
                    drone.reset()
                # forward / backward
                elif event.key == pygame.K_w:
                    drone.move_forward()
                elif event.key == pygame.K_s:
                    drone.move_backward()
                # left / right
                elif event.key == pygame.K_a:
                    drone.move_left()
                elif event.key == pygame.K_d:
                    drone.move_right()
                # up / down
                elif event.key == pygame.K_UP:
                    drone.move_up()
                elif event.key == pygame.K_DOWN:
                    drone.move_down()
                # turn left / turn right
                elif event.key == pygame.K_LEFT:
                    drone.turn_left()
                elif event.key == pygame.K_RIGHT:
                    drone.turn_right()
                elif event.key == pygame.K_j:
                    start_score()
                # speed
                elif event.key == pygame.K_1:
                    drone.speed = 0.1
                elif event.key == pygame.K_2:
                    drone.speed = 0.2
                elif event.key == pygame.K_3:
                    drone.speed = 0.3
                elif event.key == pygame.K_4:
                    drone.speed = 0.4
                elif event.key == pygame.K_5:
                    drone.speed = 0.5
                elif event.key == pygame.K_6:
                    drone.speed = 0.6
                elif event.key == pygame.K_7:
                    drone.speed = 0.7
                elif event.key == pygame.K_8:
                    drone.speed = 0.8
                elif event.key == pygame.K_9:
                    drone.speed = 0.9
                elif event.key == pygame.K_0:
                    drone.speed = 1.0

        try:
            surface = pygame.image.fromstring(drone.image, (W, H), 'RGB')
            # battery status
            hud_color = (255, 0, 0) if drone.navdata.get('drone_state', dict()).get('emergency_mask', 1) else (10, 10, 255)
            bat = drone.navdata.get(0, dict()).get('battery', 0)
            f = pygame.font.Font(None, 20)
            hud = f.render('Battery: %i%%' % bat, True, hud_color)
            screen.blit(surface, (0, 0))
            screen.blit(hud, (10, 10))
        except:
            pass

        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("FPS: %.2f" % clock.get_fps())

    print "Shutting down...",
    drone.halt()
    print "Ok."

if __name__ == '__main__':
    main()

