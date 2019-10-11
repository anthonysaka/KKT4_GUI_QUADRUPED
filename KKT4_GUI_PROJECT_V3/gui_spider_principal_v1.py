from Tkinter import *
#import Tkinter.font

import movement_spider_v4
import KKT4


# FUNCTIONS

def start():  # Wait key press to move.
    movement_spider_v4.main()

def turn_on():
    movement_spider_v4.startSpider()

def turn_off():
    movement_spider_v4.stand_downSpider()

def foward():
    movement_spider_v4.forward()

def backward():
    movement_spider_v4.backward()

def turn_right():
    movement_spider_v4.turn_right()

def turn_left():
    movement_spider_v4.turn_left()

def salute_one():
    movement_spider_v4.salute_1()

def salute_two():
    movement_spider_v4.salute_2()

def go_up():
    movement_spider_v4.upSpyder()

def go_down():
    movement_spider_v4.downSpyder()

def turn_on_automatic_mode():
    KKT4.startSpider()

def turn_off_automatic_mode():
    #global flag_auto = False
    KKT4.stand_downSpider()

def start_automatic():
    KKT4.main()
    #KKT4.decide()


def window_mode_one():

    modeOne = Toplevel()
    modeOne.title("KK_T4 Robot - MODE 1 - ")
    modeOne.geometry("1000x720+345+150")
    modeOne.resizable(0, 0)
    modeOne.config(bg="#00264d")

    powerControlframe = LabelFrame(modeOne, text=" Power Control ",  height=120, width=950, bd='4', fg='white', bg='#00264d')
    powerControlframe.grid(pady=15, padx=15)

    turn_on = Button(powerControlframe, bd=0, bg='#00264d', image=iconOn, activebackground="green", cursor="spider", command=turn_on)
    turn_on.pack()

    turn_off = Button(powerControlframe, bd=0, bg='#00264d', image=iconOff, activebackground="red", cursor="spider", command=turn_off)
    turn_off.pack()

    moveControlframe = LabelFrame(modeOne, text=" Movement Control ",  height=400, width=950, bd='4', fg='white', bg='#00264d')
    moveControlframe.grid(pady=15, padx=25)

    turn_foward = Button(moveControlframe, bd=0, bg='#00264d', image=iconUp, activebackground="red", cursor="spider", command=foward)
    turn_foward.place(x=100, y=10)

    turn_left = Button(moveControlframe, bd=0, bg='#00264d', image=iconLeft, activebackground="red", cursor="spider", command=turn_left)
    turn_left.place(x=30, y=70)

    turn_back = Button(moveControlframe, bd=0, bg='#00264d', image=iconDown, activebackground="red", cursor="spider", command=backward)
    turn_back.place(y=140, x=100)

    turn_right = Button(moveControlframe, bd=0, bg='#00264d', image=iconRight, activebackground="red", cursor="spider", command=turn_right)
    turn_right.place(y=70, x=170)

    wave_hand_0 = Button(moveControlframe, bd=0, bg='#00264d', image=iconWave_0, activebackground="red", cursor="spider", command=salute_one)
    wave_hand_0.place(y=70, x=270)

    label_wave = Label(moveControlframe, text=" WAVE ONE", relief=RAISED)
    label_wave.place(y=150, x=260)

    wave_hand_1 = Button(moveControlframe, bd=0, bg='#00264d', image=iconWave_1, activebackground="red", cursor="spider", command=salute_two)
    wave_hand_1.place(y=70, x=370)

    sit_down = Button(moveControlframe, bd=0, bg='#00264d', image=iconGoDown, activebackground="red", cursor="spider", command=go_down)
    sit_down.place(y=70, x=470)

    Up_scared = Button(moveControlframe, bd=0, bg='#00264d', image=iconUpScared, activebackground="red", cursor="spider", command=go_up)
    Up_scared.place(y=70, x=570)

    win.protocol("WM_DELETE_WINDOW", turn_off)  # Cleanup when user press closes window

    modeOne.mainloop()

        

def window_mode_two():

    modeTwo = Toplevel()
    modeTwo.title("KK_T4 Robot - MODE 2 - ")

    modeTwo.geometry("600x600+345+150")
    modeTwo.resizable(0, 0)
    modeTwo.config(bg="#00264d")

    powerControlframe = LabelFrame(modeTwo, text=" Power Control ",  height=120, width=950, bd='4', fg='white', bg='#00264d')
    powerControlframe.grid(pady=15, padx=15)

    turn_on_auto = Button(powerControlframe, bd=0, bg='#00264d', image=iconOn, activebackground="green", cursor="spider", command=turn_on_automatic_mode)
    turn_on_auto.pack()

    turn_off_auto = Button(powerControlframe, bd=0, bg='#00264d', image=iconOff, activebackground="red", cursor="spider", command=turn_off_automatic_mode)
    turn_off_auto.pack()

    start_auto = Button(powerControlframe, bd=0, bg='#00264d', image=iconStart, activebackground="red", cursor="spider", command=start_automatic)
    start_auto.pack()

    ### GUI DEFINITIONS ###


win = Tk()
win.title("KK_T4 ROBOT Control GUI")
win.geometry("1020x720+470+150")
win.resizable(0, 0)
win.config(bg="#00264d")


iconStart = PhotoImage(file="spider-start.png")
iconOn = PhotoImage(file="switch-on.png")
iconOff = PhotoImage(file="switch-off.png")

iconUp = PhotoImage(file="up-chevron.png")
iconDown = PhotoImage(file="down-chevron.png")
iconLeft = PhotoImage(file="left-chevron.png")
iconRight = PhotoImage(file="right-chevron.png")

iconWave_0 = PhotoImage(file="waving-hand-1.png")
iconWave_1 = PhotoImage(file="waving-hand.png")

iconGoDown = PhotoImage(file="go-sit-down.png")
iconUpScared = PhotoImage(file="scared.png")

mainMenuModesframe = Frame(win, bg="#00264d", width=900, height=720)
mainMenuModesframe.pack()
mainMenuModesframe.place(x=20, y=25)


####################################### mainMenuModesframe ####################################
### WIDGETS ###

photo = PhotoImage(file="kkta.png")
w = Label(mainMenuModesframe, image=photo)
w.photo = photo
w.grid(pady=10)

# Button, MODE 1
mode_one = Button(mainMenuModesframe, text="Mode 1",  bg='bisque2', height=2, width=20, activebackground="red", activeforeground="orange", cursor="spider", command=window_mode_one)
mode_one.grid(pady=15)
# Button, MODE 2
mode_two = Button(mainMenuModesframe, text="Mode 2",  bg='bisque2', height=2, width=20, activebackground="red", activeforeground="orange", cursor="spider", command=window_mode_two)
mode_two.grid(pady=15)

# Button MODE 3
#mode_three = Button(mainMenuModesframe, text="Mode 3", font=myFont, bg='bisque2', height=2, width=20, activebackground="red", activeforeground="orange", cursor="spider")
#mode_three.grid(pady=15)

labelframe = LabelFrame(mainMenuModesframe, text=" MODES FEATURES ", height=120, width=950, bd='4', fg='white', bg='#00264d')
labelframe.grid(pady=15, padx=15)


win.mainloop()  # Loops forever
