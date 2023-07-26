from tkinter import Tk, font
import  PySimpleGUI as sg
root = Tk()
font_tuple = font.families()
root.destroy()
#Creates a Empty list to hold font names
FontList=[]
for font in font_tuple:
    FontList.append(font)
#size 28, 28 is optimized for my Android phone please tweak as per your screen
#Scrolled popup to accommodate big list
sg.popup_scrolled(FontList, title='All fonts installed using PySimpleGUI', size=(28,28), grab_anywhere=True)