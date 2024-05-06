import time
import threading
import keyboard
from robomaster import robot

x_val = 0
y_val = 0
z_val = 0
speed = 0.5
z_speed = 50
running = True

def keyboard_control():
	global x_val, y_val, z_val, running

	while running:
		if keyboard.is_pressed('w'):
			x_val = speed
		elif keyboard.is_pressed('s'):
			x_val = -speed
		else:
			x_val = 0.0

		if keyboard.is_pressed('a'):
			z_val = -z_speed
		elif keyboard.is_pressed('d'):
			z_val = z_speed
		else:
			z_val = 0
		if keyboard.is_pressed(' '):
			x_val = 0.0
			y_val = 0.0
			z_val = 0.0
		
		time.sleep(0.1)

def handler(info):
	yaw, pitch, roll = info
def pos_handler(info):
	x, y, z = info

if __name__ == '__main__':
	ep_robot = robot.Robot()
	ep_robot.initialize(conn_type='rndis')
	ep_chassis = ep_robot.chassis
	ep_chassis.sub_position(freq=10, callback=pos_handler)

	keyboard_thread = threading.Thread(target=keyboard_control)
	keyboard_thread.start()

	try:
		while True:
			ep_chassis.drive_speed(x=x_val, y=y_val, z=z_val, timeout=0.1)
			time.sleep(0.1)
			if keyboard.is_pressed(" "):
				running = False
				break
		ep_robot.close()
	except KeyboardInterrupt:
		ep_robot.close()
		running = False
		keyboard_thread.join()
 
