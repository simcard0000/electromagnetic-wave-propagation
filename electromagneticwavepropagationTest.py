# -*- coding: utf-8 -*-
"""
2019: @simcard0000
"""
from numpy import arange, sin, pi
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d
import tkinter as tkr
from multiprocessing import Process, freeze_support
from pynput import keyboard

def infopop():
    class buildframe(tkr.Frame):
        def __init__(self, master=None):
            #"self" is the main widget that holds and organizes the others within it
            #Below, makes a sort of object to make function calls in "buildframe"
            super().__init__(master)
            self.master = master
            self.pack()
            self.make_widgets()
            self.configure(background="grey")
        def make_widgets(self):
            def control_button():
                #Instructions for manipulating the graph
                self.outputbox.configure(text = "By focusing in the window with the graph, you can manipulate the animation in a few ways. " + 
                                         "The up arrow key will speed up the waves, while the down arrow key will slow them down. " +
                                         "The right arrow key can be used to increase the amplitude, and the left arrow key to decrease it. " +
                                         "The 'page up' key will increase the wavelength, and the 'page down' key will decrease it. " + 
                                         "To stop and start the animation, press the spacebar.")
            def info_button():
                #Credits section
                self.outputbox.configure(text = "~Made by Simran Thind for SPH4U.There's an Easter egg in this program; have you found it yet? " + 
                                         "Pro-tip: Try the keyboard..." )
            self.titlelabel = tkr.Label(self, text = "What do you want to do?", font=("Times New Roman", 15), background = "darkred")
            self.titlelabel.pack()
            #All the text doesn't just show up together, you can press the buttons to see something specific
            self.buttonforcontrols = tkr.Button(self, text = "Manipulate the Graph", font=("Times New Roman", 12), command=control_button, cursor="diamond_cross", activebackground='darkblue')
            self.buttonforcontrols.pack()
            self.buttonforabout = tkr.Button(self, text = "Learn More" , font=("Times New Roman", 12), command=info_button, cursor="diamond_cross", activebackground="darkblue")
            self.buttonforabout.pack()
            self.outputbox = tkr.Label(self, font=("Times New Roman", 12),wraplength=500, background="grey")
            self.outputbox.pack()
    
    #Creating a tk interpreter; Tkinter is essentially a cover/easier implementation for tcl/tk
    root = tkr.Tk()
    root.title("Controls for Electromagnetic Wave Propagation")
    root.geometry("500x300+50+50")
    root.configure(background="grey")
    root.resizable(False, False)
    #Making a window for everything to be in; setting size
    showinfopop = buildframe(master=root)
    showinfopop.mainloop()
def thegraph():
    #This is the second large function, thegraph is for running the wave graph in a separate processor
    graph = plt.figure(figsize=(10,10))
    graphwindow = graph.canvas.window()
    graphwindow.setFixedSize(700, 700)
    graph.canvas.set_window_title("Graph for Electromagnetic Wave Propagation")
    #Creating a figure for the graph and setting the size for the window
    xinterval = arange(-2.0, 2.0, 0.05)
    basicxinterval = arange(-2.0, 2.0, 0.05)
    arrowxinterval = arange(-2.0, 2.01, 0.15)
    basicarrowxinterval = arange(-2.0, 2.01, 0.15)
    #These return ranges of values; used for plotting the sine waves and arrows under them
    animlimit = 0
    #A counter for how long the animation should run
    global egg
    egg = False
    global amplitude
    amplitude = 2
    #A variable so that the amplitude can be changed
    global wavelength
    wavelength = pi
    #pi's a nice number
    global checkclose
    checkclose = False
    #A variable for checking the state of the graph window
    global speed
    speed = 0.02
    #A variable so that the speed (how fast the animation moves/wave speed)
    def on_key_press(key):
        #A function to listen in to any key presses while the animation runs,
        #also enclosing the while loop for the animation
        global speed
        global amplitude
        global wavelength
        global egg
        #Caps Lock and Shift turn the turn the surprise on and off, respectively
        if key == keyboard.Key.caps_lock:
            egg = True
        if key == keyboard.Key.shift:
            egg = False
        #Pressing the "page up" button will increase
        #the wavelength while pressing the "page down" button on your keyboard
        #will decrease the wavelength.
        if key == keyboard.Key.page_up:
            wavelength -= 0.01
        if key == keyboard.Key.page_down:
            wavelength += 0.01
        #Pressing the left and right arrow keys will decrease and increase the
        #amplitude of the electromagnetic wave, respectively
        if key == keyboard.Key.right:
            amplitude += 0.01
        if key == keyboard.Key.left:
            amplitude -= 0.01
        #Pressing the up and down arrow keys will increase and decrease speed, respectively
        if key == keyboard.Key.up:
            speed += 0.01
        if key == keyboard.Key.down:
            speed -= 0.01
            #To ensure that the electromagnetic wave doesn't go "backwards", there's a limit
            if speed < 0.01:
                speed = 0.01
        if key == keyboard.Key.space:
            #The space bar can be used for both starting and stopping the animation
            if speed > 0:
                speed = 0
            elif speed <= 0:
                speed = 0.02
        #Variables below get passed out to be used in the animation while loop
        return (speed, amplitude, wavelength, egg)
    with keyboard.Listener(on_press=on_key_press):
        while (animlimit <= 5000):
            #Here to break out of the animation cleanly
            if animlimit == 5000 or checkclose == True:
                break
            plt.clf()
            #Clearing the figure to update and redraw
            graphaxes = axes3d.Axes3D(graph)
            if egg == False:
                graphaxes.set_axis_off()
                #"B oscillates in the yz plane!"
                plt.plot(basicxinterval, -amplitude*sin(wavelength*xinterval), color="red", zs=0, zdir="z")
                #"E oscillates in the xz plane!"
                plt.plot(basicxinterval, amplitude*sin(wavelength*xinterval),color="blue", zs=0, zdir="y")
                #Arrows for the wave in the magnetic field
                graphaxes.quiver(basicarrowxinterval,0,0,  0,-amplitude*sin(wavelength*arrowxinterval),0,  arrow_length_ratio=0.10, color="firebrick")
                #Arrows for the wave in the electric field
                graphaxes.quiver(basicarrowxinterval,0,0,  0,0,amplitude*sin(wavelength*arrowxinterval),  arrow_length_ratio=0.10, color="navy")
                #making some pseudo-axes with arrows to match the note we had in class
                graphaxes.quiver([-2,0], [0,0], [-2,0], [0,0], [0, 0], [2,0],length=2,arrow_length_ratio=0.03,color="black")
                graphaxes.quiver([-2,0], [0,0], [0,0], [2,0], [0, 0], [0,0],length=2,arrow_length_ratio=0.03,color="black")
                graphaxes.quiver([-2,0], [2,0], [0,0], [0,0], [-2, 0], [0,0],length=2,arrow_length_ratio=0.03,color="black")
                #The labels for the axes
                font = {"fontname": "Times New Roman", "size": "12"}
                graphaxes.text2D(0.04, 0.8, "X, ℰ (electric field)", transform=graphaxes.transAxes, **font)
                graphaxes.text2D(0.01, 0.41, "Y, B (magnetic field)", transform=graphaxes.transAxes, **font)
                graphaxes.text2D(0.78, 0.4, "Z, dir. of propagation", transform=graphaxes.transAxes, **font)
            if egg == True:
                with plt.xkcd():
                    #With the easter egg, colours, labels, and axes would be different in design, but it's still the same wave
                    graphaxes.set_facecolor("black")
                    plt.plot(basicxinterval, -amplitude*sin(wavelength*xinterval), color="darkolivegreen", zs=0, zdir="z")
                    plt.plot(basicxinterval, amplitude*sin(wavelength*xinterval),color="fuchsia", zs=0, zdir="y")
                    graphaxes.quiver(basicarrowxinterval,0,0,  0,0,amplitude*sin(wavelength*arrowxinterval),  arrow_length_ratio=0.10, color="purple")
                    graphaxes.quiver(basicarrowxinterval,0,0,  0,-amplitude*sin(wavelength*arrowxinterval),0,  arrow_length_ratio=0.10, color="seagreen")
                    font = {"fontname": "Comic Sans MS", "size": "10", "color":"white"}
                    graphaxes.set_xlabel("Z, direction of propagation -->", **font)
                    graphaxes.set_ylabel("Y - B (magnetic field)", **font)
                    graphaxes.set_zlabel("X - E (electric field)", **font)
            plt.title("Electromagnetic Wave Propagation", fontweight="bold", **font)
            graphaxes.set_xlim3d(-2, 2)
            graphaxes.set_ylim3d(-2, 2)
            graphaxes.set_zlim3d(-2, 2)
            graphaxes.set_xticklabels([])
            graphaxes.set_yticklabels([])
            graphaxes.set_zticklabels([])
            graph.gca().set_aspect("equal", adjustable="box")
            #increasing the animation limit
            animlimit += 1
            #to make the movement for propagation, speed is subtracted from the x intervals for plotting
            arrowxinterval -= speed
            xinterval -= speed
            def closethegraph(evt):
                #checking if the window of the graph closed
                global checkclose
                checkclose = True
                return checkclose
            #matching matplotlib to the function above
            graph.canvas.mpl_connect("close_event", closethegraph)
            #pausing the animation for updating
            plt.pause(0.001)      
if __name__ == "__main__":
    #The exe can only run in Windows environments
    freeze_support()
    showinggraph = Process(name="showinggraph", target=thegraph)
    showinginfopop = Process(name="showinginfopop",target=infopop)
    showinginfopop.start()
    showinggraph.run()
