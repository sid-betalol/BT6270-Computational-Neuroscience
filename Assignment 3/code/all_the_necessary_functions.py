# -*- coding: utf-8 -*-
"""BE19B032_BT6270_assignment3_Hopfield.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_tsG23pHzjKFqUadgnLACS9MdcQ_Uskh

## **BT6270 Computational Neuorscience Assignment-3: Hopfield Networks**

Siddharth Betala (BE19B032)

### Importing the required libraries
"""

import os
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error as mse
from tqdm import tqdm

"""### Function to read data as vectors"""

def data2vec(file_name):
    """
    Function for reading data from files in numpy array format, reshaping it 
    into a column vector, and performing additional pre-processing.
    """
    data = np.loadtxt(file_name+".txt", delimiter=",")
    data_vec = data.reshape(-1,1)
    data_sign = np.sign(data_vec)
    # Make all positions that have 0 as 1
    data_sign[np.where(data_sign==0)] = 1
    clean_data = data_sign
    return clean_data

"""### Function to generate patches"""

def generate_patches(data, size=(90,100)):
	"""
	The patch generation function. The patches are generated at random, 
    and the maximum height and width are specified by the min_x, min_y, max_x, 
    and max_y variables.
	"""
	data = data.reshape(size)
	min_x, min_y = 20, 15
	max_x, max_y = 45, 45
	x = random.randint(0, size[0]-max_x-1)
	y = random.randint(0, size[1]-max_y-1)
	dist_x = random.randint(min_x, max_x)
	dist_y = random.randint(min_y, max_y)
	
	patch = np.zeros(size)
	patch[x:x+dist_x, y:y+dist_y] = data[x:x+dist_x, y:y+dist_y]
	
	patch = patch.reshape(-1,1)
	return patch

"""### All the required visualization functions"""

def show_img(img, title="", size=(90,100)):
    if img.shape[1] == 1:
        img = img.reshape(size)
        
    plt.figure(figsize=[6,6])
    if title:
        plt.title(title)
        
    plt.imshow(img, cmap='gray')
    plt.show()
    print('\n')

def show_patch(img, patch, title="", size=(90,100)):
    """
    Function to enable side-by-side visualisation of an image and the generated 
    patch of the image.
    """
    if img.shape[1] == 1:
        img = img.reshape(size)
    if patch.shape[1] == 1:
        patch = patch.reshape(size)
        
    plt.figure(figsize=[15,6])
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title(title+" - Full Image")
    plt.subplot(1, 2, 2)
    plt.imshow(patch, cmap='gray')
    plt.title(title+" - Patch")
    plt.show()
    print('\n')
	
def show_recons(img, patch_before, patch_after, title="", size=(90,100)):
    """
    Function to enable side-by-side visualisation of the entire image, the 
    generated image prior to the epoch reconstruction, and the reconstructed 
    image after the epoch.
    """
    if img.shape[1] == 1:
        img = img.reshape(size)
    if patch_before.shape[1] == 1:
        patch_before = patch_before.reshape(size)
    if patch_after.shape[1] == 1:
        patch_after = patch_after.reshape(size)
        
    plt.figure(figsize=[15,4])
    plt.subplot(1, 3, 1)
    plt.imshow(img, cmap='gray')
    plt.title(title+" - Full Image")
    plt.subplot(1, 3, 2)
    plt.imshow(patch_before, cmap='gray')
    plt.title(title+" -  Before Reconstruction")
    plt.subplot(1, 3, 3)
    plt.imshow(patch_after, cmap='gray')
    plt.title(title+" -  After Reconstruction")
    plt.show()
    print('\n')

def rmse_plotter(rmse, images, title=""):
    """
    Function to plot the RMSE for each of the images: ball, mona and cat
    """
    for i in range(rmse.shape[1]):
        plt.figure()
        plt.plot(rmse[:,i])
        if title:
            plt.title(title + images[i])
            
        plt.grid(True)
        plt.xlabel("Iterations")
        plt.ylabel("RMSE")
        plt.show()
        print('\n')

"""### Hopfield Networks: Discrete and Continuous
### Function to Damage Weights
"""

def discrete_hopfield(S, W, V_new, max_epochs, dummy=0, every=10, size=(90,100)):
    rmse = []
    ims = []
    
    for i in tqdm(range(max_epochs), desc="Training Discrete Hopfield Network"):
        V = V_new.copy()
        V_new = np.sign(np.matmul(W,V))
        
        if dummy and i%every==0:
            for j in range(V_new.shape[1]):
                show_recons(S[:,j].reshape(-1,1), V[:,j].reshape(-1,1), V_new[:,j].reshape(-1,1), title="Epochs:" + str(i) + "; " + images[j])
                
        rmse_new = []
        ims_new = []
        
        for j in range(V.shape[1]):
            rmse_new.append(mse(S[:,j], V[:,j]))
            ims_new.append([plt.imshow(V[:,j].reshape(size), cmap="gray")])
            
        rmse.append(rmse_new)
        ims.append(ims_new)
        
    V = V_new.copy()
    rmse_new = []
    for j in range(V.shape[1]):
        rmse_new.append(mse(S[:,j], V[:,j]))
        
    rmse.append(rmse_new)
    
    for j in range(V.shape[1]):
        show_recons(S[:,j].reshape(-1,1), V[:,j].reshape(-1,1), V_new[:,j].reshape(-1,1), title="Epochs:" + str(i+1) + "; " + images[j])
        
    return rmse, V, ims

def continuous_hopfield(S, W, V_new, max_epochs, LAMBDA=10, dt=0.01, dummy=0, every=10, size=(90,100)):
	rmse = []
	V_hist = []
	
	U_new = V_new.copy()
	for i in tqdm(range(max_epochs), desc="Training Continuous Hopfield Network"):
		U = U_new.copy()
		V = V_new.copy()
		
		U_new = U + (-U + np.matmul(W, V))*dt
		V_new = np.tanh(LAMBDA*U_new)
		
		if dummy and i%every==0:
			for j in range(V_new.shape[1]):
				show_recons(S[:,j].reshape(-1,1), V[:,j].reshape(-1,1), V_new[:,j].reshape(-1,1), title="Epochs:" + str(i) + "; " + images[j])

		rmse_new = []
		for j in range(V.shape[1]):
			rmse_new.append(mse(S[:,j], V[:,j]))
		rmse.append(rmse_new)
		
		V_hist.append(V)

	V = V_new.copy()
	rmse_new = []
	for j in range(V.shape[1]):
		rmse_new.append(mse(S[:,j], V[:,j]))
	rmse.append(rmse_new)
	V_hist.append(V)
	
	for j in range(V.shape[1]):
		show_recons(S[:,j].reshape(-1,1), V[:,j].reshape(-1,1), V_new[:,j].reshape(-1,1), title="Epochs:" + str(i+1) + "; " + images[j])

	return rmse, V, V_hist

def damage_weights(W, p):
	"""
	Function to damage the weights based on the specified damage fraction.
	"""
	W_damaged = W.copy()
	N = W.shape[0]
	pos = np.random.randint(0, N*N-1, size=(int(N*N*p),1))
	W_damaged = W_damaged.reshape(-1,1)
	W_damaged[pos] = 0
	
	return W_damaged.reshape(N,N)

# Reading the data as vectors
ball = data2vec('ball')
mona = data2vec('mona')
cat = data2vec('cat')

#patches for all 3 images
ball_patch = generate_patches(ball)
mona_patch = generate_patches(mona)
cat_patch = generate_patches(cat)

show_patch(ball, ball_patch, "Ball")
show_patch(mona, mona_patch, "Mona")
show_patch(cat, cat_patch, "Cat")

# Translating concatenation along the column
S = np.c_[ball, mona, cat]
V = np.c_[ball_patch, mona_patch, cat_patch]

V_init = V.copy()
V_new = V.copy()

# Calculate weights
N = S.shape[0]
W = (1/N)*(np.matmul(S, S.T))

images = ["Ball", "Mona", "Cat"]

# To generate plots by using the .py file, use similar framework as given ahead in the notebook