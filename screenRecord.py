import time
import cv2
import mss
import numpy
from pynput import mouse, keyboard
from threading import Thread
from queue import Queue
import logging
'''
Used to save the monitored screen
'''
def screen_record(in_q):
    logging.basicConfig(filename="screen_log.txt", level=logging.DEBUG, format="%(asctime)s: %(message)s")
    frame_width = 1280
    frame_height = 720
    frameRate = 25.0
    i = 0
    outputPath = "screen.avi"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(outputPath, fourcc, frameRate, (frame_width, frame_height))

    with mss.mss() as sct:
        # Capture whole screen
        monitor = sct.monitors[1]
        while "Screen capturing":
            i +=1
            #print("Iteration: %d" % i)
            #last_time = time.time()
            # Get raw pixels from the screen, save it to a Numpy array
            img = numpy.array(sct.grab(monitor))
            img = cv2.resize(img, (frame_width, frame_height))
            frame = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            logging.info("Frame: ({0})".format(i))
            out.write(frame)

            #Checking if 'Esc' has been pressed to terminate
            #The information is send by the other thread

             #   break
            #cv2.imshow('frame', frame)
            #if cv2.waitKey(25) & 0xFF == ord("q"):
            #    cv2.destroyAllWindows()
            #    break
            if not(in_q.empty()):
                break
            #cv2.putText(frame, "FPS: %f" % (1.0 / (time.time() - last_time)),
                    # (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            #print("FPS: %f" % (1.0 / (time.time() - last_time)))
            # Press "q" to quit
            #if in_q.get() == _sentinel:
            #    break
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
        logging.info("Mouse moved to ({0}, {1})".format(x, y))

    def on_click(x, y, button, pressed):
        logging.info("Mouse clicked at ({0}, {1}) with {2}".format(x, y, button))

    def on_scroll(x, y, dx, dy):
        logging.info("Mouse scrolled at ({0}, {1}, {2}, {3})".format(x, y, dx, dy))

    def on_press(key):
        # Collect events until pressed Esc key
        if key == keyboard.Key.esc:
            #Sending information to terminate the other thread
            out_q.put(_sentinel)
            mouse_listener.stop()
            key_listener.stop()
    #logging.basicConfig(filename="mouse_log.txt",level=logging.DEBUG, format = "%(asctime)s: %(message)s")
    mouse_listener = mouse.Listener(on_move = on_move, on_click=on_click, on_scroll=on_scroll)
    mouse_listener.start()
    key_listener = keyboard.Listener(on_press=on_press)
    key_listener.start()



if __name__ == '__main__':
    _sentinel = object()
    q = Queue()
    t1 = Thread(target = screen_record, args =(q, ))
    t2 = Thread(target = listen, args =(q, ))
    t1.start()
    last_time = time.time()
    t2.start()
    q.join()
    print((time.time() - last_time))
