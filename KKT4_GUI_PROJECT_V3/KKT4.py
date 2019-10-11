from __future__ import division
from threading import Thread, Lock

import time
import Adafruit_PCA9685  # Import the PCA9685 module.
import pygame

from picamera import PiCamera
from time import sleep

from keras.preprocessing.image import img_to_array
from keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import cv2

cur_angle_mutex = Lock()
i2c_mutex = Lock()
pwm = Adafruit_PCA9685.PCA9685()  # Asignation to variable pwm, Adafruit Library.
pwm.set_pwm_freq(60)  # Frecuency to singal PWM.
# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

# -------     DECLARATION and ASIGNATION VARIABLES     ------- #
move_delay = 0.00025  # Time 'seconds' to move delay.
step_delay = 0.0005  # Time 'seconds' to steps move delay.

# Value angle to offset position calibration of the servos motors.
leg_1_angle_offset = [0, 0, 100]
leg_2_angle_offset = [0, 25, 100]
leg_3_angle_offset = [0, 0, 80]
leg_4_angle_offset = [0, 0, 80]
# -------------------------------- #
front_lateral = 40
front_parallel = 89
front_lateral_add = -30
back_lateral = 140
back_parallel = 89
back_lateral_add = 30
footup = 0
footdown = 60
pincer_up = 130
pincer_down = 120
leg_1_footdown = footdown
leg_2_footdown = footdown
leg_3_footdown = footdown
leg_4_footdown = footdown

flag_leg_formation = 0

channel_cur = [90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90]

automatic = True

#------------------------------------------------------------------------------------
def init_camera():
    global model
    global vs

    model = load_model("outputmodel.model")
    print("[INFO] starting video stream...")
    vs = VideoStream(usePiCamera=True).start()


# MAIN function.
def main():
    global flag_leg_formation
    global automatic

    pygame.init()

    pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Proyecto KKT4")
    
    message_display('MODO 2: AUTOPILOTO ACTIVADO')

    #startSpider()

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if not automatic:
            if keys[pygame.K_s] and flag_leg_formation == 0:
                startSpider()

            if flag_leg_formation != 0 and flag_leg_formation != 3 and flag_leg_formation != 4:
                if keys[pygame.K_LEFT]:
                    turn_left()
                if keys[pygame.K_RIGHT]:
                    turn_right()
                if keys[pygame.K_UP]:
                    forward()
                if keys[pygame.K_DOWN]:
                    backward()
                if keys[pygame.K_f]:
                    salute_1()
                if keys[pygame.K_g]:
                    salute_2()
                if keys[pygame.K_a]:
                    automatic = True

            if keys[pygame.K_z] and flag_leg_formation != 0 and flag_leg_formation != 4:
                upSpyder()
            if keys[pygame.K_x] and flag_leg_formation != 0 and flag_leg_formation != 3:
                downSpyder()

            if keys[pygame.K_p]:
                camera.start_preview()
                camera.capture('/home/pi/Desktop/SpyderCamera/ImageTaker/%s.jpg' % i)
                i = i + 1
                camera.stop_preview()

        if automatic:
            decide()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                automatic = False

    pygame.quit()

    if flag_leg_formation != 0:
        stand_downSpider()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()
    

def decide():
    global model
    global vs

    frame = vs.read()
    image = cv2.resize(frame, (28, 28))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    (Izquierda, Derecha, NoLinea) = model.predict(image)[0]

    if Izquierda > Derecha and Izquierda > NoLinea:
        #forward()
        sleep(0.5)

        frame = vs.read()
        image = cv2.resize(frame, (28, 28))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        (Izquierda, Derecha, NoLinea) = model.predict(image)[0]

        if Izquierda > Derecha and Izquierda > NoLinea:
            turn_left()
            turn_left()
            turn_left()
        else:
            pass

    elif Derecha > Izquierda and Derecha > NoLinea:
        #forward()
        sleep(0.5)

        frame = vs.read()
        image = cv2.resize(frame, (28, 28))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        (Izquierda, Derecha, NoLinea) = model.predict(image)[0]

        if Derecha > Izquierda and Derecha > NoLinea:
            turn_right()
            turn_right()
            turn_right()
        else:
            pass
    elif NoLinea > Izquierda and NoLinea > Derecha:
        forward()
    


# Function to begin 'start' the spider. Get the init position to move.
def startSpider():
    # Formation of the legs status.
    global flag_leg_formation

    leg_1(front_parallel, 0, 160)
    leg_2(front_parallel, 0, 160)
    leg_3(front_parallel, 0, 160)
    leg_4(front_parallel, 0, 160)

    time.sleep(1)

    # Get the lateral position leg to stand up in the next threads.
    thread_1 = Thread(target=leg_1, args=(front_parallel, 0, 200))  # Move Left Side.
    thread_2 = Thread(target=leg_2, args=(back_parallel, 0, 200))
    thread_3 = Thread(target=leg_3, args=(back_lateral, 0, 200))  # Move Right Side.
    thread_4 = Thread(target=leg_4, args=(front_lateral, 0, 200))

    thread_1.start()  # Start the threads.
    thread_2.start()
    thread_3.start()
    thread_4.start()

    thread_1.join()  # Wait that threads was completed.
    thread_2.join()
    thread_3.join()
    thread_4.join()

    #time.sleep(1)

    # Stand up the body of the spider.
    thread_1 = Thread(target=leg_1, args=(front_parallel, footdown, pincer_down))
    thread_2 = Thread(target=leg_2, args=(back_parallel, footdown, pincer_down))
    thread_3 = Thread(target=leg_3, args=(back_lateral, footdown, pincer_down))
    thread_4 = Thread(target=leg_4, args=(front_lateral, footdown, pincer_down))

    thread_1.start()  # Start the threads.
    thread_2.start()
    thread_3.start()
    thread_4.start()

    thread_1.join()  # Wait that threads was completed.
    thread_2.join()
    thread_3.join()
    thread_4.join()

    flag_leg_formation = 1

# ----------------------------------------------------------------------- #

# Function to set, servo motors.
def setServo(channel, angle):
  # Arguments: channel -> number of the channel i2c interface.
  #            angle -> value to set position servo motor.
    if(angle < 0):
        angle = 0  # top min angle.
    elif(angle > 220):
        angle = 220  # top max angle.
    i2c_mutex.acquire()
    pwm.set_pwm(channel, 0, (int)((angle * 2.5) + 150))  # (number_channel, pulse width PWM)
    i2c_mutex.release()

# Function to set inverse, servo motors.
def setServo_invert(channel, angle):
  # Arguments: channel -> number of the channel i2c interface.
  #            angle -> value to set position servo motor.
    if(angle < 0):
        angle = 0
    elif(angle > 180):
        angle = 180
    i2c_mutex.acquire()
    pwm.set_pwm(channel, 0, (int)((angle * (-2.5)) + 600))  # (number_channel, pulse width PWM)
    i2c_mutex.release()

# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
# -----------    Definition function foreach legs of spider    ---------- #
# Note: These Function, Have Like Principal Objective, Get the Same Value of Angle Got on Arguments.

#   --- LEG_1 ---  #
def leg_1(angle_1, angle_2, angle_3):

    angle_1 = angle_1 + leg_1_angle_offset[0]
    angle_2 = angle_2 + leg_1_angle_offset[1]
    angle_3 = angle_3 + leg_1_angle_offset[2]

    # While angles difference value of requeriment value (angle_1_2_3).
    while(channel_cur[0] != angle_1 or channel_cur[1] != angle_2 or channel_cur[2] != angle_3):
        # ANGLE1
       if angle_1 > channel_cur[0]:
           channel_cur[0] = channel_cur[0] + 1  # Increment value angle.
           setServo_invert(0, channel_cur[0])
       elif angle_1 < channel_cur[0]:
           channel_cur[0] = channel_cur[0] - 1  # Decrement value angle.
           setServo_invert(0, channel_cur[0])
       # ANGLE2
       if angle_2 > channel_cur[1]:
           channel_cur[1] = channel_cur[1] + 1  # Increment value angle.
           setServo_invert(1, channel_cur[1])
       elif angle_2 < channel_cur[1]:
           channel_cur[1] = channel_cur[1] - 1  # Decrement value angle.
           setServo_invert(1, channel_cur[1])
       # ANGLE3
       if angle_3 > channel_cur[2]:
           channel_cur[2] = channel_cur[2] + 1  # Increment value angle.
           setServo(2, channel_cur[2])
       elif angle_3 < channel_cur[2]:
           channel_cur[2] = channel_cur[2] - 1  # Decrement value angle.
           setServo(2, channel_cur[2])

       time.sleep(move_delay)  # Delay to wait other movement of legs.

#   --- LEG_2 ---  #
def leg_2(angle_1, angle_2, angle_3):

    angle_1 = angle_1 + leg_2_angle_offset[0]
    angle_2 = angle_2 + leg_2_angle_offset[1]
    angle_3 = angle_3 + leg_2_angle_offset[2]

    # While angles difference value of requeriment value (angle_1_2_3).
    while(channel_cur[3] != angle_1 or channel_cur[4] != angle_2 or channel_cur[5] != angle_3):
        # ANGLE1
        if angle_1 > channel_cur[3]:
            channel_cur[3] = channel_cur[3] + 1  # Increment value angle.
            setServo_invert(3, channel_cur[3])
        elif angle_1 < channel_cur[3]:
            channel_cur[3] = channel_cur[3] - 1  # Decrement value angle.
            setServo_invert(3, channel_cur[3])

        # ANGLE2
        if angle_2 > channel_cur[4]:
            channel_cur[4] = channel_cur[4] + 1  # Increment value angle.
            setServo_invert(4, channel_cur[4])
        elif angle_2 < channel_cur[4]:
            channel_cur[4] = channel_cur[4] - 1  # Decrement value angle.
            setServo_invert(4, channel_cur[4])

        # ANGLE3
        if angle_3 > channel_cur[5]:
            channel_cur[5] = channel_cur[5] + 1  # Increment value angle.
            setServo(5, channel_cur[5])
        elif angle_3 < channel_cur[5]:
            channel_cur[5] = channel_cur[5] - 1  # Decrement value angle.
            setServo(5, channel_cur[5])

        time.sleep(move_delay)  # Delay to wait othe movement of legs.

#   --- LEG_3 ---  #
def leg_3(angle_1, angle_2, angle_3):

    angle_1 = angle_1 + leg_3_angle_offset[0]
    angle_2 = angle_2 + leg_3_angle_offset[1]
    angle_3 = angle_3 + leg_3_angle_offset[2]

    # While angles difference value of requeriment value (angle_1_2_3).
    while(channel_cur[6] != angle_1 or channel_cur[7] != angle_2 or channel_cur[8] != angle_3):
        # ANGLE1
        if angle_1 > channel_cur[6]:
            channel_cur[6] = channel_cur[6] + 1  # Increment value angle.
            setServo(6, channel_cur[6])
        elif angle_1 < channel_cur[6]:
            channel_cur[6] = channel_cur[6] - 1  # Decrement value angle.
            setServo(6, channel_cur[6])

        # ANGLE2
        if angle_2 > channel_cur[7]:
            channel_cur[7] = channel_cur[7] + 1  # Increment value angle.
            setServo_invert(7, channel_cur[7])
        elif angle_2 < channel_cur[7]:
            channel_cur[7] = channel_cur[7] - 1  # Decrement value angle.
            setServo_invert(7, channel_cur[7])

        # ANGLE3
        if angle_3 > channel_cur[8]:
            channel_cur[8] = channel_cur[8] + 1  # Increment value angle.
            setServo(8, channel_cur[8])
        elif angle_3 < channel_cur[8]:
            channel_cur[8] = channel_cur[8] - 1  # Decrement value angle.
            setServo(8, channel_cur[8])

        time.sleep(move_delay)  # Delay to wait othe movement of legs.

#   --- LEG_4 ---  #
def leg_4(angle_1, angle_2, angle_3):

    angle_1 = angle_1 + leg_4_angle_offset[0]
    angle_2 = angle_2 + leg_4_angle_offset[1]
    angle_3 = angle_3 + leg_4_angle_offset[2]

    # While angles difference value of requeriment value (angle_1_2_3).
    while(channel_cur[9] != angle_1 or channel_cur[10] != angle_2 or channel_cur[11] != angle_3):
        # ANGLE1
        if angle_1 > channel_cur[9]:
            channel_cur[9] = channel_cur[9] + 1  # Increment value angle.
            setServo(9, channel_cur[9])
        elif angle_1 < channel_cur[9]:
            channel_cur[9] = channel_cur[9] - 1  # Decrement value angle.
            setServo(9, channel_cur[9])

        # ANGLE2
        if angle_2 > channel_cur[10]:
            channel_cur[10] = channel_cur[10] + 1  # Increment value angle.
            setServo_invert(10, channel_cur[10])
        elif angle_2 < channel_cur[10]:
            channel_cur[10] = channel_cur[10] - 1  # Decrement value angle.
            setServo_invert(10, channel_cur[10])

        # ANGLE3
        if angle_3 > channel_cur[11]:
            channel_cur[11] = channel_cur[11] + 1  # Increment value angle.
            setServo(11, channel_cur[11])
        elif angle_3 < channel_cur[11]:
            channel_cur[11] = channel_cur[11] - 1  # Decrement value angle.
            setServo(11, channel_cur[11])

        time.sleep(move_delay)  # Delay to wait other movement of legs.


# --------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------- #
# -----------    Definitions of the Movements Functions of the Spider.   ---------- #

# Function go to foward spider.
def forward():
    global flag_leg_formation

    if(flag_leg_formation == 1):

        #flag_leg_formation = 2
        # Always lift the leg in a parallel side. Assuming that this function is called after startSpider(), which makes the left side legs parallel and right side legs lateral.

        # Lift leg_1
        leg_1(front_parallel, footup, pincer_up)
        time.sleep(step_delay)
        # Move leg_1 to lateral position
        leg_1(front_lateral, footup, pincer_up)
        time.sleep(step_delay)
        # Bring leg_1 down
        leg_1(front_lateral, footdown, pincer_down)
        time.sleep(step_delay)

        # Moving leg_2 to lateral, and leg4 to parallel, keep leg3 in lateral
        thread_2 = Thread(target=leg_2, args=(back_lateral, footdown, pincer_down))
        thread_3 = Thread(target=leg_3, args=(back_lateral + back_lateral_add, footdown, pincer_down))
        thread_4 = Thread(target=leg_4, args=(front_parallel, footdown, pincer_down))

        thread_2.start()  # Start the threads.
        thread_3.start()
        thread_4.start()

        thread_2.join()  # Wait that threads was completed.
        thread_3.join()
        thread_4.join()

        # Lift leg_3 and bring to parallel position
        # Lift
        leg_3(back_lateral + back_lateral_add, footup, pincer_up)
        time.sleep(step_delay)
        #Move leg_3 to parallel position
        leg_3(back_parallel, footup, pincer_up)
        time.sleep(step_delay)
        #Bring leg_3 down
        leg_3(back_parallel, footdown, pincer_down)
        time.sleep(step_delay)

        # Now right side legs are parallel and left side legs are lateral

    if (flag_leg_formation == 2):

        #flag_leg_formation = 1
        # Lift leg_4
        leg_4(front_parallel, footup, pincer_up)
        time.sleep(step_delay)
        # Move leg_4 to lateral position
        leg_4(front_lateral, footup, pincer_up)
        time.sleep(step_delay)
        # Bring leg_4 down
        leg_4(front_lateral, footdown, pincer_down)
        time.sleep(step_delay)

        # Moving leg_3 to lateral, and leg1 to parallel, keep leg_2 lateral.
        thread_3 = Thread(target=leg_3, args=(back_lateral, footdown, pincer_down))
        thread_2 = Thread(target=leg_2, args=(back_lateral + back_lateral_add, footdown, pincer_down))
        thread_1 = Thread(target=leg_1, args=(front_parallel, footdown, pincer_down))

        thread_3.start()  # Start the threads.
        thread_2.start()
        thread_1.start()

        thread_3.join()  # Wait that threads was completed.
        thread_2.join()
        thread_1.join()

        time.sleep(step_delay)

        # Lift leg_2 and Bring to parallel position
        leg_2(back_lateral + back_lateral_add, footup, pincer_up)
        time.sleep(step_delay)
        # Move leg_2 to lateral position
        leg_2(back_parallel, footup, pincer_up)
        time.sleep(step_delay)
        # Bring leg2 down
        leg_2(back_parallel, footdown, pincer_down)
        time.sleep(step_delay)

        # Now left side legs are parallel and right side legs are lateral.

    if(flag_leg_formation == 1):
        flag_leg_formation = 2
    elif(flag_leg_formation == 2):
        flag_leg_formation = 1

# Function go to backward the spider.
def backward():
    global flag_leg_formation

    if(flag_leg_formation == 1):

        #flag_leg_formation = 2
        # Always lift the leg in a parallel side. Assuming this function is called after startSpider, which makes the left side legs parallel and right side legs lateral.

        # Lift leg_2
        leg_2(back_parallel, footup, pincer_up)
        time.sleep(step_delay)
        # Move leg_2 to lateral position
        leg_2(back_lateral, footup, pincer_up)
        time.sleep(step_delay)
        #bring leg2 down
        leg_2(back_lateral, footdown, pincer_down)
        time.sleep(step_delay)

        # Moving leg_1 to lateral, and leg_3 to parallel, keep leg_4 lateral.
        thread_1 = Thread(target=leg_1, args=(front_lateral, footdown, pincer_down))
        thread_3 = Thread(target=leg_3, args=(back_parallel, footdown, pincer_down))
        thread_4 = Thread(target=leg_4, args=(front_lateral + front_lateral_add, footdown, pincer_down))

        thread_1.start()  # Start the threads.
        thread_3.start()
        thread_4.start()

        thread_1.join()  # Wait that threads was completed.
        thread_3.join()
        thread_4.join()

        # Lift leg_4 and bring to parallel position.
        # Lift.
        leg_4(front_lateral + front_lateral_add, footup, pincer_up)
        time.sleep(step_delay)
        # Move leg_3 to parallel position.
        leg_4(front_parallel, footup, pincer_up)
        time.sleep(step_delay)
        # Bring leg_3 down.
        leg_4(front_parallel, footdown, pincer_down)
        time.sleep(step_delay)

        # Now right side legs are parallel and left side legs are lateral

    if (flag_leg_formation == 2):

        #flag_leg_formation = 1
        #Lift leg_3
        leg_3(back_parallel, footup, pincer_up)
        time.sleep(step_delay)
        # Move leg_3 to lateral position.
        leg_3(back_lateral, footup, pincer_up)
        time.sleep(step_delay)
        # Bring leg_4 down.
        leg_3(back_lateral, footdown, pincer_down)
        time.sleep(step_delay)

        # Move leg_4 to lateral, and leg_2 to parallel, keep leg_1 back_lateral.
        thread_4 = Thread(target=leg_4, args=(front_lateral, footdown, pincer_down))
        thread_2 = Thread(target=leg_2, args=(back_parallel, footdown, pincer_down))
        thread_1 = Thread(target=leg_1, args=(front_lateral + front_lateral_add, footdown, pincer_down))

        thread_4.start()  # Start the threads.
        thread_2.start()
        thread_1.start()

        thread_4.join()  # Wait that threads was completed.
        thread_2.join()
        thread_1.join()

        time.sleep(step_delay)

        # Lift leg_1 and bring to parallel position
        leg_1(front_lateral + front_lateral_add, footup, pincer_up)
        time.sleep(step_delay)
        # Move leg_1 to lateral position
        leg_1(front_parallel, footup, pincer_up)
        time.sleep(step_delay)
        # Bring leg_1 down
        leg_1(front_parallel, footdown, pincer_down)
        time.sleep(step_delay)

        # Now left side legs are parallel and right side legs are lateral

    if(flag_leg_formation == 1):
        flag_leg_formation = 2
    elif(flag_leg_formation == 2):
        flag_leg_formation = 1

# Function to turn rigth the spider.
def turn_right():
    global flag_leg_formation

    if(flag_leg_formation == 1):

        #flag_leg_formation = 2
        # Always lift the leg in a parallel side. Assuming this function is called after startSpider, which makes the left side legs parallel and right side legs lateral.

        # Lift leg_1
        leg_1(front_parallel, footup, pincer_up)  # probar sin esto.
        time.sleep(step_delay)
        # Move leg_1 to lateral position
        leg_1(front_lateral, footup, pincer_up)
        time.sleep(step_delay)

        # Move leg_2 to lateral, and leg_3 to lateral, Keep leg_4 lateral.
        thread_2 = Thread(target=leg_2, args=(back_lateral, footdown, pincer_down))
        thread_3 = Thread(target=leg_3, args=(back_parallel, footdown, pincer_down))
        thread_4 = Thread(target=leg_4, args=(front_lateral + front_lateral_add, footdown, pincer_down))

        thread_2.start()  # Start the threads.
        thread_3.start()
        thread_4.start()

        # Bring leg_1 down  / This is here, because, need the other leg begin move and next bring down the leg.
        leg_1(front_lateral, footdown, pincer_down)
        #time.sleep(step_delay)

        thread_2.join()  # Wait that threads was completed.
        thread_3.join()
        thread_4.join()

        # Lift leg_4 and bring to parallel position
        # Lift leg 4
        leg_4(front_lateral + front_lateral_add, footup, pincer_up)
        time.sleep(step_delay)
        # Move leg_4 to parallel position
        leg_4(front_parallel, footup, pincer_up)
        time.sleep(step_delay)
        # Bring leg_4 down
        leg_4(front_parallel, footdown, pincer_down)
        time.sleep(step_delay)

        # Now right side legs are parallel and left side legs are lateral

    if (flag_leg_formation == 2):

        #flag_leg_formation = 1
        # Lift leg_3
        leg_3(back_parallel, footup, pincer_up)
        time.sleep(step_delay)
        # Move leg_3 to lateral position
        leg_3(back_lateral, footup, pincer_up)
        time.sleep(step_delay)

        # Move leg_1 to parallel, and leg_4 to lateral, Keep leg_2 to lateral.
        thread_1 = Thread(target=leg_1, args=(front_parallel, footdown, pincer_down))
        thread_4 = Thread(target=leg_4, args=(front_lateral, footdown, pincer_down))
        thread_2 = Thread(target=leg_2, args=(back_lateral + back_lateral_add, footdown, pincer_down))

        thread_1.start()  # Start the threads.
        thread_4.start()
        thread_2.start()

        # Bring leg_3 down  / This is here, because, need the other leg begin move and next bring down the leg.
        leg_3(back_lateral, footdown, pincer_down)

        thread_1.join()  # Wait that threads was completed.
        thread_4.join()
        thread_2.join()

        time.sleep(step_delay)

        # Lift leg_2
        leg_2(back_lateral + back_lateral_add, footup, pincer_up)
        time.sleep(step_delay)
        # Move leg_2 to parallel position
        leg_2(back_parallel, footup, pincer_up)
        time.sleep(step_delay)
        # Bring leg_2 down
        leg_2(back_parallel, footdown, pincer_down)
        time.sleep(step_delay)

        # Now left side legs are parallel and right side legs are lateral.

    if(flag_leg_formation == 1):
        flag_leg_formation = 2
    elif(flag_leg_formation == 2):
        flag_leg_formation = 1

# Function to turn left the spider.
def turn_left():
    global flag_leg_formation

    if (flag_leg_formation == 1):

        #flag_leg_formation = 2
        # Always lift the leg in a parallel side. Assuming this function is called after startSpider, which makes the left side legs parallel and right side legs lateral.

        # Lift leg_2
        leg_2(back_parallel, footup, pincer_up)
        time.sleep(step_delay)
        # Move leg_2 to lateral position.
        leg_2(back_lateral, footup, pincer_up)
        time.sleep(step_delay)

        # Move leg_1 to lateral, and leg_4 to parallel, Keep the leg_3 in lateral.
        thread_1 = Thread(target=leg_1, args=(front_lateral, footdown, pincer_down))
        thread_3 = Thread(target=leg_3, args=(back_lateral + back_lateral_add, footdown, pincer_down))
        thread_4 = Thread(target=leg_4, args=(front_parallel, footdown, pincer_down))

        thread_1.start()   # Start the threads.
        thread_3.start()
        thread_4.start()

        # Bring leg_2 down.
        leg_2(back_lateral, footdown, pincer_down)
        #time.sleep(step_delay)

        thread_1.join()  # Wait that threads was completed.
        thread_3.join()
        thread_4.join()

        # Lift leg_3 and bring to parallel position
        # Lift leg 3
        leg_3(back_lateral + back_lateral_add, footup, pincer_up)
        time.sleep(step_delay)
        # Move leg_3 to parallel position
        leg_3(back_parallel, footup, pincer_up)
        time.sleep(step_delay)
        # Bring leg_3 down
        leg_3(back_parallel, footdown, pincer_down)
        time.sleep(step_delay)

        # Now right side legs are parallel and left side legs are lateral

    if (flag_leg_formation == 2):

        #flag_leg_formation = 1
        # Lift leg_4
        leg_4(front_parallel, footup, pincer_up)
        time.sleep(step_delay)
        # Move leg_4 to lateral position
        leg_4(front_lateral, footup, pincer_up)
        time.sleep(step_delay)

        # Move leg_3 to lateral, and leg_2 to parallel, Keep leg_1 to lateral.
        thread_3 = Thread(target=leg_3, args=(back_lateral, footdown, pincer_down))
        thread_2 = Thread(target=leg_2, args=(back_parallel, footdown, pincer_down))
        thread_1 = Thread(target=leg_1, args=(front_lateral + front_lateral_add, footdown, pincer_down))

        thread_3.start()  # Start the threads.
        thread_2.start()
        thread_1.start()

        # Bring leg_4 down  / This is here, because, need the other leg begin move and next bring down the leg.
        leg_4(front_lateral, footdown, pincer_down)

        thread_3.join()  # Wait that threads was completed.
        thread_2.join()
        thread_1.join()

        time.sleep(step_delay)

        # Lift leg_1
        leg_1(front_lateral + front_lateral_add, footup, pincer_up)
        time.sleep(step_delay)
        # Move leg_1 to parallel position
        leg_1(front_parallel, footup, pincer_up)
        time.sleep(step_delay)
        # Bring leg_1 down
        leg_1(front_parallel, footdown, pincer_down)
        time.sleep(step_delay)

        # Now left side legs are parallel and right side legs are lateral.

    if(flag_leg_formation == 1):
        flag_leg_formation = 2
    elif(flag_leg_formation == 2):
        flag_leg_formation = 1


# Function go to Down Spider.
def stand_downSpider():
    global flag_leg_formation

    # Keep actual position (lateral or parallel) and go to down.
    thread_1 = Thread(target=leg_1, args=(channel_cur[0], 0, 160))
    thread_2 = Thread(target=leg_2, args=(channel_cur[3], 0, 160))
    thread_3 = Thread(target=leg_3, args=(channel_cur[6], 0, 160))
    thread_4 = Thread(target=leg_4, args=(channel_cur[9], 0, 160))

    thread_1.start()  # Start the threads.
    thread_2.start()
    thread_3.start()
    thread_4.start()

    thread_1.join()  # Wait that threads was completed.
    thread_2.join()
    thread_3.join()
    thread_4.join()

    # Move all legs to parallel.
    thread_1 = Thread(target=leg_1, args=(front_parallel, 0, 0))
    thread_2 = Thread(target=leg_2, args=(back_parallel, 0, 0))
    thread_3 = Thread(target=leg_3, args=(back_parallel, 0, 0))
    thread_4 = Thread(target=leg_4, args=(back_parallel, 0, 0))

    thread_1.start()  # Start the threads.
    thread_2.start()
    thread_3.start()
    thread_4.start()

    thread_1.join()   # Wait that threads was completed.
    thread_2.join()
    thread_3.join()
    thread_4.join()

    # Keep all, and go down pincer of legs.
    thread_1 = Thread(target=leg_1, args=(front_parallel, 90, 0))
    thread_2 = Thread(target=leg_2, args=(back_parallel, 90, 0))
    thread_3 = Thread(target=leg_3, args=(back_parallel, 90, 0))
    thread_4 = Thread(target=leg_4, args=(back_parallel, 90, 0))

    thread_1.start()  # Start the threads.
    thread_2.start()
    thread_3.start()
    thread_4.start()

    thread_1.join()   # Wait that threads was completed.
    thread_2.join()
    thread_3.join()
    thread_4.join()

    for x in range(0, 12):
        pwm.set_pwm(x, 0, 0)

    # Flag like initial value, ready to start again the spider.
    flag_leg_formation = 0


def downSpyder():
    global flag_leg_formation

    if flag_leg_formation == 1:
        t1 = Thread(target=leg_1, args=(channel_cur[0], 0, 160))
        t2 = Thread(target=leg_2, args=(channel_cur[3], 0, 160))
        t3 = Thread(target=leg_3, args=(channel_cur[6], 0, 160))
        t4 = Thread(target=leg_4, args=(channel_cur[9], 0, 160))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()

    if flag_leg_formation == 4:

        t1 = Thread(target=leg_1, args=(front_parallel, 0, 200))
        t2 = Thread(target=leg_2, args=(back_parallel, 0, 200))
        t3 = Thread(target=leg_3, args=(back_lateral, 0, 200))
        t4 = Thread(target=leg_4, args=(front_lateral, 0, 200))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()

        t1 = Thread(target=leg_1, args=(front_parallel, footdown, pincer_down))
        t2 = Thread(target=leg_2, args=(back_parallel, footdown, pincer_down))
        t3 = Thread(target=leg_3, args=(back_lateral, footdown, pincer_down))
        t4 = Thread(target=leg_4, args=(front_lateral, footdown, pincer_down))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()

    if flag_leg_formation == 1:
        flag_leg_formation = 4
    else:
        flag_leg_formation = 1

# se arregla la posicion y luego se levanta.
def upSpyder():
    global flag_leg_formation

    if flag_leg_formation == 1:
        leg_1(front_parallel, footup, pincer_down)
        leg_1(front_lateral, footdown, pincer_down)
        leg_2(back_parallel, footup, pincer_down)
        leg_2(back_lateral, footdown, pincer_down)

        t1 = Thread(target=leg_1, args=(front_lateral, 180, 40))
        t2 = Thread(target=leg_2, args=(back_lateral, 180, 40))
        t3 = Thread(target=leg_3, args=(back_lateral, 180, 40))
        t4 = Thread(target=leg_4, args=(front_lateral, 180, 40))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()

    if flag_leg_formation == 2:
        leg_4(front_parallel, footup, pincer_down)
        leg_4(front_lateral, footdown, pincer_down)
        leg_3(back_parallel, footup, pincer_down)
        leg_3(back_lateral, footdown, pincer_down)

        t1 = Thread(target=leg_1, args=(front_lateral, 180, 40))
        t2 = Thread(target=leg_2, args=(back_lateral, 180, 40))
        t3 = Thread(target=leg_3, args=(back_lateral, 180, 40))
        t4 = Thread(target=leg_4, args=(front_lateral, 180, 40))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()

    if flag_leg_formation == 3:
        t1 = Thread(target=leg_1, args=(front_lateral, 90, 40))
        t2 = Thread(target=leg_2, args=(back_lateral, 90, 40))
        t3 = Thread(target=leg_3, args=(back_lateral, 90, 40))
        t4 = Thread(target=leg_4, args=(front_lateral, 90, 40))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()

        time.sleep(1)

        t1 = Thread(target=leg_1, args=(front_lateral, footdown, 40))
        t2 = Thread(target=leg_2, args=(back_lateral, footdown, 40))
        t3 = Thread(target=leg_3, args=(back_lateral, footdown, 40))
        t4 = Thread(target=leg_4, args=(front_lateral, footdown, 40))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()

        t1 = Thread(target=leg_1, args=(front_parallel, 0, 200))
        t2 = Thread(target=leg_2, args=(back_parallel, 0, 200))
        t3 = Thread(target=leg_3, args=(back_lateral, 0, 200))
        t4 = Thread(target=leg_4, args=(front_lateral, 0, 200))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()

        t1 = Thread(target=leg_1, args=(front_parallel, footdown, pincer_down))
        t2 = Thread(target=leg_2, args=(back_parallel, footdown, pincer_down))
        t3 = Thread(target=leg_3, args=(back_lateral, footdown, pincer_down))
        t4 = Thread(target=leg_4, args=(front_lateral, footdown, pincer_down))

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()

    if flag_leg_formation == 1 or flag_leg_formation == 2:
        flag_leg_formation = 3
    else:
        flag_leg_formation = 1

# mueve de lado a lado.
def salute_1():
    global flag_leg_formation

    a = channel_cur[1]
    b = channel_cur[2]
    c = a - 90

    if flag_leg_formation == 1:
        for x in range(0, 5):
            leg_1(front_parallel, c, 40)
            leg_1(0, c, 40)

        leg_1(front_parallel, channel_cur[1], channel_cur[2])
        leg_1(front_parallel, a, b)

    if flag_leg_formation == 2:
        for x in range(0, 5):
            leg_4(front_parallel, c, 40)
            leg_4(0, c, 40)

        leg_4(front_parallel, channel_cur[1], channel_cur[2])
        leg_4(front_parallel, a, b)

# mueve arriba y abajo.
def salute_2():
    global flag_leg_formation

    a = channel_cur[1]
    b = channel_cur[2]
    c = a - 90

    if flag_leg_formation == 1:
        for x in range(0, 5):
            leg_1(0, c, 0)
            leg_1(0, c, 90)

        leg_1(front_parallel, channel_cur[1], channel_cur[2])
        leg_1(front_parallel, a, b)

    if flag_leg_formation == 2:
        for x in range(0, 5):
            leg_4(0, c, 0)
            leg_4(0, c, 90)

        leg_4(front_parallel, channel_cur[1], channel_cur[2])
        leg_4(front_parallel, a, b)


if __name__ == '__main__':  # To execute first the main.
    main()
