import pdb
import os
import sys
import numpy as np
from scipy.misc import imread, imsave
from Tkinter import *
from tkFileDialog import askopenfilename
#import Image, ImageTk
from PIL import Image, ImageTk
Label={0:'bedroom',
       1:'kitchen',
       2:'dining_room',
       3:'conference_room',
       4:'living_room',
       5:'bridge',
       6:'tower',
       7:'classroom',
       8:'church_outdoor',
       9:'restaurant'}

def check_coor(File, name):
    def quit(root):
        root.quit()

    root = Tk()
    root.title('%s'%name) 
    root.geometry("400x400+600+200")
    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=8, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)

    #adding the image
    #File = askopenfilename(parent=root, initialdir="C:/",title='Choose an image.')
    img = ImageTk.PhotoImage(Image.open(File))
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    def printcoords(event):
        global _number
        _number = 0 
        root.destroy()
    canvas.bind("<Button 1>",printcoords)

    def printcoords2(event):     
        global _number
        _number = 1
        root.destroy()
    canvas.bind("<Button 3>",printcoords2)

    def printcoords2(event):     
        global _number
        _number = 2
        root.destroy()
    canvas.bind("<Button 2>",printcoords2)

    root.mainloop()
    return _number
from os import listdir
DATA_SETING = 'preclass_10000'  # 100,1000,10000
USING_MODEL = 'with_pretrain'
USING_MODEL = 'without_pretrain'
#PATH = '.'
PATH = 'LSUN_10_10000_test_accuary'
images1_path = listdir(PATH + '/samples_%s_with_pretrain/single_images/'%DATA_SETING)
images2_path = listdir(PATH + '/samples_%s_without_pretrain/single_images/'%DATA_SETING)
n_files = range(len(images1_path))
random_state = np.random.RandomState(np.random.randint(2000))
random_state.shuffle(n_files)
baseline, proposed = 0, 0
privious_coor = 0 
margin = 10
high_begin = 150 
weith_begin = 200 
num_samples = 2000
num_valid_pairs = 100
#A =  check_coor('./begin.png', name = 'Start')
for _index, _exact_image in enumerate(n_files):
    if _index ==num_samples:
       break 
    image_set = 255*np.zeros((400, 400, 3))
    img1 = Image.open(PATH + '/samples_%s_with_pretrain/single_images/%d.png'%(DATA_SETING,_exact_image))
    img1 = img1.resize([128,128])
    image1 = np.array(img1.convert('RGB'))
    img2 = Image.open(PATH + '/samples_%s_without_pretrain/single_images/%d.png'%(DATA_SETING,_exact_image))
    img2 = img2.resize([128,128])
    image2 = np.array(img2.convert('RGB'))
    birthmark = np.mod(np.random.randint(20180528), 2)
    name = Label[np.divide(_exact_image, 1000)]  
    # print('birthmark = ', birthmark)
    if birthmark == 0:
        image_set[high_begin-64:high_begin+64, weith_begin-128 - margin: weith_begin- margin, :] = image2
        image_set[high_begin-64:high_begin+64, weith_begin + margin:weith_begin+128+ margin, :] = image1
    else:
        image_set[high_begin-64:high_begin+64, weith_begin-128 - margin: weith_begin- margin, :] = image1
        image_set[high_begin-64:high_begin+64, weith_begin + margin:weith_begin+128+ margin, :] = image2

    if not os.path.exists('test'):
        os.makedirs('test')
    imsave('./test/%d.png'%birthmark, image_set)
    A =  check_coor('./test/%d.png'%birthmark, name)
    if A ==2:
        print('Give up')
        with open('%s_log.txt'%DATA_SETING, 'a+') as _file:
            _file.write('Give up\n')
        continue
    if birthmark == 0:
        if A ==  0:
            print('left, baseline',birthmark)
            baseline +=1
            with open('%s_log.txt'%DATA_SETING, 'a+') as _file:
                _file.write('left, baseline : %d\n'%birthmark)
        else:
            print('right, proposed',birthmark)
            proposed +=1
            with open('%s_log.txt'%DATA_SETING, 'a+') as _file:
                _file.write('right, proposed : %d\n'%birthmark)
    else:
        if A ==  0:
            print('right, proposed',birthmark)
            proposed +=1
            with open('%s_log.txt'%DATA_SETING, 'a+') as _file:
                _file.write('right, proposed : %d\n'%birthmark)
        else:
            print('left, baseline',birthmark)
            baseline +=1
            with open('%s_log.txt'%DATA_SETING, 'a+') as _file:
                _file.write('left, baseline : %d\n'%birthmark)
    if (baseline + proposed) == num_valid_pairs: 
        print('Proposed method: %d, Ratio: %f'%(proposed, 1.0*proposed / (proposed + baseline)))
        print('Baseline method: %d, Ratio: %f'%(baseline, 1.0*baseline / (proposed + baseline)))
        with open('%s_human_study.txt'%DATA_SETING, 'a+') as _file:
            _file.write('Proposed method: %d, Ratio: %f, Baseline method: %d, Ratio: %f\n'%(proposed, 1.0*proposed / (proposed + baseline), baseline, 1.0*baseline / (proposed + baseline)))
        with open('%s_log.txt'%DATA_SETING, 'a+') as _file:
            _file.write('end')
        sys.exit()
