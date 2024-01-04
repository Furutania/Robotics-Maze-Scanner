# Maze Scanner
Uses Python openCV2 to identify features of a maze and translates data to a bitmap

## Preprocessing
To ensure a clean output, the corners of maze must be identified by the user via clicking the top left, top right, bottom right, bottom left corners in that order

In the future this could be done by the program via edge detection but due to time limitations it was done manually

## CV2 Thresholds 

To identify maze walls, the image is passed through color thresholds 
```
    def filter(self, low, high, img):
        theMask = cv2.inRange(img, low, high)
        # TODO: Work here
        hsv_color = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        masked = cv2.bitwise_and(hsv_color, img, mask=theMask)
        greyScale = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
        blackAndWhite = cv2.threshold(greyScale, 10, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        return blackAndWhite
```
The black and white image is then passed through a custom filter to identify valid walls. Currently, the maze is formatted to be a 5x5 grid, but this will work with any configuration by changing a few values

![example](https://github.com/Furutania/Robotics-Maze-Scanner/assets/97645214/2a43fc3e-0a43-46e3-999a-e6adb3186609)

## Creating a usable data structure
The wall filter returns a 2d array where 0s represents empty spaces and 1s represent the walls

![output](https://github.com/Furutania/Robotics-Maze-Scanner/assets/97645214/6bd07461-89a8-4c89-ae66-97cbbf73e5b0)

As we can see the produced map accurately reflects the walls of the maze

Then we can quickly edit the array identify legal positions, here its marked with 8s
![output2](https://github.com/Furutania/Robotics-Maze-Scanner/assets/97645214/be619bed-3262-4f0b-82ad-c76c52614dcc)

## Movement
By solving the 2d array with BFS we'll have a list of coordinates that the robot will need to make to complete the maze. We can translate these coordinates to points in the camera stream and tell the robot to travel to them

The robot is able to identify its position by the colors on its shell. Similar to the wall color threshold, by identifying the sky blue and orange colors we are able to locate the robot and its orientation
