# ******************************************************** #
#         |||||||||||||      ||||    ||||    ||||          #
#        ||||                ||||    ||||    ||||          #
#        ||||                ||||    ||||    ||||          #
#        ||||    ||||||||    ||||    ||||    ||||          #
#        ||||        ||||    ||||    ||||    ||||          #
#         |||||||||||||||    ||||||||||||    ||||          #
#                                                          #
# *********** Developers: A.Sakamoto & R.Soriano ********* #

# Import necessary packages.
from Tkinter import *
import tkFont

#import movement_spider_v4
import KKT4_V2
#---------------------------
KKT4_V2.init_camera()

# Window for mode one.
def window_mode_one():

    # FUNCTIONS

    def turn_on():
        KKT4_V2.startSpider()

    def turn_off():
        KKT4_V2.stand_downSpider()
        modeOne.destroy()

    def foward():
        KKT4_V2.forward()

    def backward():
        KKT4_V2.backward()

    def turn_right():
        KKT4_V2.turn_right()

    def turn_left():
        KKT4_V2.turn_left()

    def salute_one():
        KKT4_V2.salute_1()

    def salute_two():
        KKT4_V2.salute_2()

    def go_up():
        KKT4_V2.upSpyder()

    def go_down():
        KKT4_V2.downSpyder()

    modeOne = Toplevel()
    modeOne.title("KKT4 Robot - MODE 1 - ")
    modeOne.geometry("900x720+460+150")
    modeOne.resizable(0, 0)
    modeOne.config(bg="#00264d")

    powerControlframe = LabelFrame(modeOne, text=" Power Control ",  height=120, width=950, bd='4', fg='white', bg='#00264d', font=myFont1)
    powerControlframe.grid(pady=20, padx=15)

    turn_on = Button(powerControlframe, bd=0, bg='#00264d', image=iconOn, activebackground="green", cursor="spider", command=turn_on)
    turn_on.pack()

    turn_off = Button(powerControlframe, bd=0, bg='#00264d', image=iconOff, activebackground="red", cursor="spider", command=turn_off)
    turn_off.pack()

    moveControlframe = LabelFrame(modeOne, text=" Movement Control ",  height=260, width=750, bd='4', fg='white', bg='#00264d', font=myFont1)
    moveControlframe.grid(pady=20, padx=75)

    turn_foward = Button(moveControlframe, bd=0, bg='#00264d', image=iconUp, activebackground="red", cursor="spider", command=foward)
    turn_foward.place(x=100, y=10)

    turn_left = Button(moveControlframe, bd=0, bg='#00264d', image=iconLeft, activebackground="red", cursor="spider", command=turn_left)
    turn_left.place(x=30, y=70)

    turn_back = Button(moveControlframe, bd=0, bg='#00264d', image=iconDown, activebackground="red", cursor="spider", command=backward)
    turn_back.place(y=140, x=100)

    turn_right = Button(moveControlframe, bd=0, bg='#00264d', image=iconRight, activebackground="red", cursor="spider", command=turn_right)
    turn_right.place(y=70, x=170)

    wave_hand_0 = Button(moveControlframe, bd=0, bg='#00264d', image=iconWave_0, activebackground="red", cursor="spider", command=salute_one)
    wave_hand_0.place(y=70, x=310)

    label_wave = Label(moveControlframe, text="Salute 1", fg='white', bg='#00264d', font=myFont1)
    label_wave.place(y=150, x=310)

    wave_hand_1 = Button(moveControlframe, bd=0, bg='#00264d', image=iconWave_1, activebackground="red", cursor="spider", command=salute_two)
    wave_hand_1.place(y=70, x=410)

    label_wave_1 = Label(moveControlframe, text="Salute 2", fg='white', bg='#00264d', font=myFont1)
    label_wave_1.place(y=150, x=410)

    sit_down = Button(moveControlframe, bd=0, bg='#00264d', image=iconGoDown, activebackground="red", cursor="spider", command=go_down)
    sit_down.place(y=70, x=510)

    label_sit = Label(moveControlframe, text="Sit down", fg='white', bg='#00264d', font=myFont1)
    label_sit.place(y=150, x=510)

    Up_scared = Button(moveControlframe, bd=-1, bg='#00264d', image=iconUpScared, activebackground="red", cursor="spider", command=go_up)
    Up_scared.place(y=70, x=610)

    label_scared = Label(moveControlframe, text="Scared", fg='white', bg='#00264d', font=myFont1)
    label_scared.place(y=150, x=610)
    
        #  ------- FRAME to put instructions  ----.
    labelframe_1 = LabelFrame(modeOne, text=" Instructions", font=myFont, height=120, width=950, bd='4', fg='white', bg='#00264d')
    labelframe_1.grid(pady=15, padx=20)
    
    label_mode_one = Label(labelframe_1, text=" Mode 1:\n \n 1- Before pressing any button, press On button \n 2- Press any button to move. \n 3- Press Off button, to close.", justify=LEFT, fg='white', font=myFont1, bg='#00264d')
    label_mode_one.grid(column=0, row=0, padx=25, pady=5)

    modeOne.mainloop()

# Window for mode two.
def window_mode_two():

    def turn_on_automatic_mode():
        KKT4_V2.startSpider()

    def turn_off_automatic_mode():
        KKT4_V2.stand_downSpider()
        modeTwo.destroy()

    def start_automatic():
        KKT4_V2.main(mode=2)

    modeTwo = Toplevel()
    modeTwo.title("KKT4 Robot - MODE 2 - ")

    modeTwo.geometry("600x600+345+150")
    modeTwo.resizable(0, 0)
    modeTwo.config(bg="#00264d")

    powerControlframe = LabelFrame(modeTwo, text=" Power Control ",  height=120, width=950, bd='4', fg='white', bg='#00264d', font=myFont1)
    powerControlframe.grid(pady=15, padx=15)

    turn_on_auto = Button(powerControlframe, bd=0, bg='#00264d', image=iconOn, activebackground="green", cursor="spider", command=turn_on_automatic_mode)
    turn_on_auto.pack()

    turn_off_auto = Button(powerControlframe, bd=0, bg='#00264d', image=iconOff, activebackground="red", cursor="spider", command=turn_off_automatic_mode)
    turn_off_auto.pack()

    start_auto = Button(powerControlframe, bd=0, bg='#00264d', image=iconStart, activebackground="red", cursor="spider", command=start_automatic)
    start_auto.pack()
    
    #  ------- FRAME to put instructions  ----.
    labelframe_2 = LabelFrame(modeTwo, text=" Instructions", font=myFont, height=120, width=950, bd='4', fg='white', bg='#00264d')
    labelframe_2.grid(pady=15, padx=20)
    
    label_mode_two = Label(labelframe_2, text=" Mode 2:\n \n 1- Before pressing any button, press On button \n 2- Press Spider button to init. \n 3- Ready. \n 4- If you want exit mode, close \n Autonomous mode windows \n then press Off button.", justify=LEFT, fg='white', font=myFont1, bg='#00264d')
    label_mode_two.grid(column=0, row=0, padx=25, pady=5)

# Window for mode three.
def window_mode_three():

    def turn_on_automatic_mode():
        KKT4_V2.startSpider()

    def turn_off_automatic_mode():
        KKT4_V2.stand_downSpider()
        modeThree.destroy()

    def start_automatic():
        KKT4_V2.main(mode=3)

    modeThree = Toplevel()
    modeThree.title("KKT4 Robot - MODE 3 - ")

    modeThree.geometry("600x600+345+150")
    modeThree.resizable(0, 0)
    modeThree.config(bg="#00264d")

    powerControlframe = LabelFrame(modeThree, text=" Controller Spider ",  height=120, width=950, bd='4', fg='white', bg='#00264d', font=myFont1)
    powerControlframe.grid(pady=15, padx=15)

    turn_on_auto = Button(powerControlframe, bd=0, bg='#00264d', image=iconOn, activebackground="green", cursor="spider", command=turn_on_automatic_mode)
    turn_on_auto.pack()

    turn_off_auto = Button(powerControlframe, bd=0, bg='#00264d', image=iconOff, activebackground="red", cursor="spider", command=turn_off_automatic_mode)
    turn_off_auto.pack()

    start_auto = Button(powerControlframe, bd=0, bg='#00264d', image=iconStart, activebackground="red", cursor="spider", command=start_automatic)
    start_auto.pack()
    
    #  ------- FRAME to put instructions  ----.
    labelframe_3 = LabelFrame(modeThree, text=" Instructions", font=myFont, height=120, width=950, bd='4', fg='white', bg='#00264d')
    labelframe_3.grid(pady=15, padx=20)
    
    label_mode_three = Label(labelframe_3, text=" Mode 3:\n \n 1- Before pressing any button, press On button \n 2- Press Spider button to init. \n 3- Ready. \n 4- If you want exit mode, close \n Autonomous mode windows \n then press Off button.", justify=LEFT, fg='white', font=myFont1, bg='#00264d')
    label_mode_three.grid(column=0, row=0, padx=25, pady=5)


#--------------------------------------------------------
    # GUI DEFINITIONS
# Main Windows
win = Tk()
win.title("KK_T4 ROBOT Control GUI")
win.geometry("1120x820+470+150")
win.resizable(0, 0)
win.config(bg="#00264d")

#  Styles of fonts to use in the code.
myFont = tkFont.Font(family='Consolas', size=14, weight="bold")
myFont1 = tkFont.Font(family='Consolas', size=11, weight="bold")

#  ------- GET images icon to buttons ----------------
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
# --------------------------------------------------

# ----- FRAME TO MAIN MENU MODES -----
mainMenuModesframe = Frame(win, bg="#00264d", width=900, height=720)
mainMenuModesframe.pack()
mainMenuModesframe.place(x=20, y=25)


#---------------------------- mainMenuModesframe -----------------------------#
#--- WIDGETS ---#

photo = PhotoImage(file="kkta.png")
w = Label(mainMenuModesframe, image=photo)
w.photo = photo
w.grid(pady=10)

# Button, MODE 1
mode_one = Button(mainMenuModesframe, text="Mode 1",  bg='bisque2', font=myFont, height=2, width=20, activebackground="red", activeforeground="orange", cursor="spider", command=window_mode_one)
mode_one.grid(pady=15)
# Button, MODE 2
mode_two = Button(mainMenuModesframe, text="Mode 2",  bg='bisque2', font=myFont, height=2, width=20, activebackground="red", activeforeground="orange", cursor="spider", command=window_mode_two)
mode_two.grid(pady=15)

# Button, MODE 3
mode_three = Button(mainMenuModesframe, text="Mode 3", font=myFont, bg='bisque2', height=2, width=20, activebackground="red", activeforeground="orange", cursor="spider", command=window_mode_three)
mode_three.grid(pady=15)

#  ------- FRAME to put features of each one modes.
labelframe = LabelFrame(mainMenuModesframe, text=" MODES FEATURES ", font=myFont, height=120, width=950, bd='4', fg='white', bg='#00264d')
labelframe.grid(pady=15, padx=5)

label_mode_one = Label(labelframe, text=" Mode One:\n \n - Mode manual spider. \n - Panel controller movements spider.", justify=LEFT, fg='white', font=myFont1, bg='#00264d')
label_mode_one.grid(column=0, row=0, padx=25, pady=5)

label_mode_two = Label(labelframe, text=" Mode Two:\n \n - Mode autonomous spider. \n - Auto movements spider. \n - Not panel controller. \n - The spider keeps walking until it \n finds an obstacle that indicates \n an instruction.", fg='white', bg='#00264d', justify=LEFT, font=myFont1)
label_mode_two.grid(column=1, row=0, padx=25, pady=15)

label_mode_three = Label(labelframe, text=" Mode Three:\n \n - Mode autonomous spider. \n - Auto movements spider. \n - Not panel controller. \n - Image mode.The spider indicates if \n the image that was shown \n is the correct one.", fg='white', bg='#00264d', justify=LEFT, font=myFont1)
label_mode_three.grid(column=2, row=0, padx=25, pady=15)


win.mainloop()  # Loops forever
