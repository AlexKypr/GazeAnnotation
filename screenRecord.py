
import time
import cv2
import mss
import numpy

frame_width = 1280
frame_height = 720
frameRate = 30.0
outputPath = "screen.avi"
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(outputPath, fourcc, frameRate,
                      (frame_width, frame_height))



with mss.mss() as sct:
    # Capture whole screen
    monitor = sct.monitors[1]

    while 'Screen capturing':
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = numpy.array(sct.grab(monitor))
        img = cv2.resize(img, (frame_width, frame_height))
        frame = img
        frame = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.putText(frame, "FPS: %f" % (1.0 / (time.time() - last_time)),
                    (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        out.write(frame)
        cv2.imshow('frame', frame)

        # Display the picture
        #cv2.imshow('OpenCV/Numpy normal', img)

        # Display the picture in grayscale
        # cv2.imshow('OpenCV/Numpy grayscale',
        # cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

        #print('fps: {0}'.format(1 / (time.time()-last_time)))



        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
'''

from mss import mss
from PIL import Image

def capture_screenshot():
    # Capture entire screen
    with mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        # Convert to PIL/Pillow Image
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

img = capture_screenshot()
img.show()
'''
