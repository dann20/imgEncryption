import os
import numpy

from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

import imageutil
import matrixutil
import crypto

def loadImage():
    try:
        loadImage.fileDir = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select Image File', filetypes=(("JPG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")))
        # file = Image.open(fln)
        loadImage.image = imageutil.load_image(loadImage.fileDir)
        var.set("Loaded image " + str(loadImage.fileDir) + ".")
    except:
        var.set('Unsuccessfully loaded image')

def addImagetoLabel(imageDir, lbl):
    img = Image.open(imageDir)
    img.thumbnail((350,350))
    img = ImageTk.PhotoImage(img)
    lbl.configure(image=img)
    lbl.image = img

def mainAlgo():
    if not(hasattr(loadImage, 'image')):
        var.set('No image loaded to process.')
    else:
        var.set("Processing.....")
        a = (crypto.a_matrix(2, 1, 2, 2), matrixutil.vector(0.6, 0.2, 0.8, 0.6).T)
        cm1 = (crypto.cat_map(2, 1), matrixutil.vector(0.9, 0.72).T)
        cm2 = (crypto.cat_map(3, 2), matrixutil.vector(0.235, 0.821).T)
        block_size = 35
        std_limit = 3

        #Algoritmo
        cypheredImage, mask, shape = crypto.cypher_image(loadImage.image, *a, *cm1, *cm2, block_size, std_limit)
        decypheredImage = crypto.decypher_image(cypheredImage, mask, shape, *a, *cm1, *cm2, block_size)

        cypheredImageDir = loadImage.fileDir.rstrip('.jpg') + '_cyphered.png'
        decypheredImageDir = loadImage.fileDir.rstrip('.jpg') + '_decyphered.png'
        imageutil.save_image(cypheredImage, cypheredImageDir)
        imageutil.save_image(decypheredImage, decypheredImageDir)
        var.set("Done saving images.")
        addImagetoLabel(cypheredImageDir, lbl2)
        var2.set("Cyphered Image")
        addImagetoLabel(decypheredImageDir, lbl3)
        var3.set("Decyphered Image")

root = Tk()

frm = Frame(root)
frm.pack(side=BOTTOM, padx=15, pady=15)

var = StringVar()
lbl = Label(root, textvariable=var, relief=RAISED)
lbl.pack(side=BOTTOM)

frmImg2 = Frame(root)
frmImg3 = Frame(root)

lbl2 = Label(master=frmImg2)
lbl2.pack(fill=BOTH, side=TOP)
var2 = StringVar()
lblText2 = Label(master=frmImg2, textvariable=var2)
lblText2.pack(side=BOTTOM, pady=5)

lbl3 = Label(master=frmImg3)
lbl3.pack(fill=BOTH, side=TOP)
var3 = StringVar()
lblText3 = Label(master=frmImg3, textvariable=var3)
lblText3.pack(side=BOTTOM, pady=5)

frmImg2.pack(side=LEFT, expand=True)
frmImg3.pack(side=LEFT, expand=True)

btn = Button(frm, text="Browse Image", command=loadImage)
btn.pack(side=LEFT)

btn2 = Button(frm, text="Run", command=mainAlgo)
btn2.pack(side=LEFT, padx=10)

btn3 = Button(frm, text="Exit", command=lambda: exit())
btn3.pack(side=LEFT, padx=10)

root.title('Image Encryption')
root.geometry("500x500")
root.mainloop()
