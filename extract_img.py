from imageio import imread, imsave

import os
import pdb

path ='sample'
target_path = 'extract_sample'

for i in os.listdir(path):
    target_imgdir = os.path.join(target_path, i)
    if not os.path.exists(target_imgdir):
        os.makedirs(target_imgdir)

    imgdir = os.path.join(path, i)
    img = imread(imgdir)
    h_,w_,_ = img.shape
    for ii in range(int(h_/256)):
        for jj in range(int(w_/256)):
            img_ = img[ii*256:(ii+1)*256, jj*256:(jj+1)*256, :]
            imsave(os.path.join(target_imgdir, 'row_%d_col_%d.png'%(ii,jj)), img_)

