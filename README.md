# AI-mouse

# Used
Python

OpenCV

Mediapipe

Automation

# How it works
The webcam takes a snapshot and uses it as a frame and on this frame Mediapipe library is used which is a cross-platform framework for building multimodal applied machine learning pipelines.

The library uses pretrained models to map the hands in an image and provides 21 key points for each hand along with their coordinates in the image with each key referring to a certain point on the hand.

The point for the index finger is used to retrieve the coordinate for the tip of the finger in the image which is then scaled to the width and length of the screen.

This is done for many frames per second to track the finger and then move the pointer on the scaled coordinates, effectively following the finger.

Certain methods are installed to let the user use Left and Right click.

In case of specific or predefined gestures:

The image first goes through pre-processing, in which at the correct light levels the general tone of skin colour is detected and isolated and image is taken through a binarization process.

After which largest contours is detected and checked against a database of pre-defined gestures.

If it matches the action is performed and if the match is a false, it tries again with the second largest contour until it finds a hit.
