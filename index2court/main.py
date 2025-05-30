import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
import pandas as pd
from Constant import Constant
import pickle
import numpy as np
import cv2

color_class = pickle.load( open( "../player_classify/new_threshold.pkl", "rb" ) )
color_type = [(51,51,255), (255,51,51), (51,255,51), (32,32,32)]

matrix = np.load("transform.npy")

for i in range(4,80):
    fname = 'output{0:03d}'.format(i)

    data = pd.read_json('../yolo/jazz_thunder/result/output{0:03d}.json'.format(i))
    '''
    ax = plt.axes(xlim=(Constant.X_MIN,Constant.X_MAX), ylim=(Constant.Y_MIN, Constant.Y_MAX))
    ax.axis('off')
    ax.grid(False)  # Remove grid
    #print(color_class[fname])
    #print(data['bottomright'])
    '''
    
    img= cv2.imread('court.png')
    for j in range(len(data['bottomright'])):
        pts = np.array([[(data['bottomright'][j]['x']+data['topleft'][j]['x'])/2, data['bottomright'][j]['y']]], dtype = "float32")
        pts = np.array([pts])
        pts = cv2.perspectiveTransform(pts, matrix[i-4])
        cv2.circle(img, (pts[0][0][0], pts[0][0][1]), 10, color_type[color_class[fname][j]], -1)
    img = cv2.resize(img, (940, 500)) 
    cv2.imwrite('game_result/myfig_{0:03d}.jpg'.format(i), img)
    
    '''
    player_circles = [plt.Circle((0, 0), Constant.PLAYER_CIRCLE_SIZE, color=color_type[color_class[fname][j]]) for (j,player) in enumerate(data['bottomright'])]
    for (j, circle) in enumerate(player_circles):
        pts = np.array([[data['bottomright'][j]['x'], data['bottomright'][j]['y']]], dtype = "float32")
        pts = np.array([pts])
        pts = cv2.perspectiveTransform(pts, matrix[i-4])

        circle.center = pts[0][0][0]/2, pts[0][0][1]
        ax.add_patch(circle)
    
    court = plt.imread("court.png")
    plt.imshow(court, zorder=0, extent=[Constant.X_MIN, Constant.X_MAX - Constant.DIFF,
                                        Constant.Y_MAX, Constant.Y_MIN])
    plt.show()
    plt.savefig('game/myfig_{0:03d}.jpg'.format(i))
    plt.close()
    '''
    
