#####################################################################

# Example : harris feature points from a video file
# specified on the command line (e.g. python FILE.py video_file) or from an
# attached web camera

# Author : Toby Breckon, toby.breckon@durham.ac.uk

# Copyright (c) 2015 School of Engineering & Computing Science,
#                    Durham University, UK
# License : LGPL - http://www.gnu.org/licenses/lgpl.html

#####################################################################

import cv2
import sys
import numpy as np

#####################################################################

keep_processing = True;
camera_to_use = 1; # 0 if you have one camera, 1 or > 1 otherwise

#####################################################################

# this function is called as a call-back everytime the trackbar is moved
# (here we just do nothing)

def nothing(x):
    pass

#####################################################################

# define video capture object

cap = cv2.VideoCapture();

# define display window name

windowName = "Live Camera Input"; # window name

# if command line arguments are provided try to read video_name
# otherwise default to capture from attached H/W camera

if (((len(sys.argv) == 2) and (cap.open(str(sys.argv[1]))))
    or (cap.open(camera_to_use))):

    # create window by name (as resizable)

    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL);

    # add some track bar controllers for settings

    neighbourhood = 3;
    cv2.createTrackbar("neighbourhood, N", windowName, neighbourhood, 15, nothing);

    while (keep_processing):

        # if video file successfully open then read frame from video

        if (cap.isOpened):
            ret, frame = cap.read();

        # convert to single channel grayscale image
        # with 32-bit float representation per pixel

        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY);
        gray = np.float32(gray);

        # get parameters from track bars

        neighbourhood = cv2.getTrackbarPos("neighbourhood, N", windowName);

        # check neighbourhood is greater than 3 and odd

        neighbourhood = max(3, neighbourhood);
        if not(neighbourhood % 2):
            neighbourhood = neighbourhood + 1;

        # find harris corners (via the good features to track function)

        corners = cv2.goodFeaturesToTrack(gray, maxCorners=500,qualityLevel=0.01,minDistance=10,blockSize=neighbourhood,useHarrisDetector=True, k=0.01);
        corners = np.int0(corners)

        for i in corners:
            x,y = i.ravel()
            cv2.circle(frame,(x,y),3,(0,255,0),-1)

        # alternatively get the raw harris eigenvalue response

        # dst = cv2.cornerHarris(gray,neighbourhood,neighbourhood, 0.01);

        # Threshold for an optimal value, it may vary depending on the image.

        # frame[dst>0.005*dst.max()]=[0,255,0]

        # display image

        cv2.imshow(windowName,frame);

        # start the event loop - essential

        # cv2.waitKey() is a keyboard binding function (argument is the time in milliseconds).
        # It waits for specified milliseconds for any keyboard event.
        # If you press any key in that time, the program continues.
        # If 0 is passed, it waits indefinitely for a key stroke.
        # (bitwise and with 0xFF to extract least significant byte of multi-byte response)

        key = cv2.waitKey(40) & 0xFF; # wait 40ms (i.e. 1000ms / 25 fps = 40 ms)

        # It can also be set to detect specific key strokes by recording which key is pressed

        # e.g. if user presses "x" then exit

        if (key == ord('x')):
            keep_processing = False;

    # close all windows

    cv2.destroyAllWindows()

else:
    print("No video file specified or camera connected.");

#####################################################################


