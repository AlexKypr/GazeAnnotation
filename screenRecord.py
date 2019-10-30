import time
import cv2
import mss
import numpy
from pynput import mouse, keyboard
from threading import Thread
from queue import Queue

'''
Used to save the monitored screen
'''
def screen_record(in_q):
    frame_width = 1280
    frame_height = 720
    frameRate = 25.0
    #i = 0
    outputPath = "screen.avi"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(outputPath, fourcc, frameRate, (frame_width, frame_height))

    with mss.mss() as sct:
        # Capture whole screen
        monitor = sct.monitors[1]
        while "Screen capturing":
            #i +=1
            #print("Iteration: %d" % i)
            #last_time = time.time()
            # Get raw pixels from the screen, save it to a Numpy array
            img = numpy.array(sct.grab(monitor))
            img = cv2.resize(img, (frame_width, frame_height))
            frame = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
            if in_q.get() == _sentinel:
                break
             #   break
            #cv2.imshow('frame', frame)
            #cv2.putText(frame, "FPS: %f" % (1.0 / (time.time() - last_time)),
                    # (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            #print("FPS: %f" % (1.0 / (time.time() - last_time)))
            # Press "q" to quit
            #k = cv2.waitKey(0)
            #print("eftase edw")
            #print(cv2.waitKey(0))
            #if cv2.waitKey(25) & 0xFF == ord("q"):
            #    cv2.destroyAllWindows()
            #    break
            #if cv2.waitKey(0) == 27:
               # print("MPHKEE")
               #cv2.destroyAllWindows()
               #break

'''
Used to monitor the movement, click and scrolling behavior of mouse
'''
def listen(out_q):
    def on_move(x, y):
        print(x, y)

    def on_click(x, y, button, pressed):
        print(x, y, button, pressed)

    def on_scroll(x, y, dx, dy):
        print(x, y, dx, dy)

    def on_press(key):
        if key == keyboard.Key.esc:
            # Collect events until pressed Esc key
            out_q.put(_sentinel)
            mouse_listener.stop()
            key_listener.stop()

    mouse_listener = mouse.Listener(on_move = on_move, on_click=on_click, on_scroll=on_scroll)
    mouse_listener.start()
    with keyboard.Listener(on_press=on_press) as key_listener:
        key_listener.join()



if __name__ == '__main__':
    _sentinel = object()
    q = Queue()
    t1 = Thread(target = screen_record, args =(q, ))
    t2 = Thread(target = listen, args =(q, ))
    t1.start()
    t2.start()

    q.join()

