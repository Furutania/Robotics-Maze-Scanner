# Maze Scanner
Uses Python openCV2 to identify features of a maze and translates data to a bitmap

## Preprocessing
To ensure a clean output, the corners of maze must be identified by the user via clicking the top left, top right, bottom right, bottem left corners in that order

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
The black and white image is then passed through a custom filter to identify valid walls. Currently, the maze is formated to be a 5x5 grid, but this will work with any configuration by changing a few values

![example](https://github.com/Furutania/Robotics-Maze-Scanner/assets/97645214/2a43fc3e-0a43-46e3-999a-e6adb3186609)

## Creating a usable datastructure


![output2](https://github.com/Furutania/Robotics-Maze-Scanner/assets/97645214/be619bed-3262-4f0b-82ad-c76c52614dcc)
