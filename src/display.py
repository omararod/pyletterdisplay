import curses
import time
import cv2

class LetterDisplay:
    def __init__(self):
        #get default video source
        self.video_source = cv2.VideoCapture(0)
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        self.gradient_string = " .:-=+*#%@"

    def start(self):
        for c in range(0, 500):
            #get 1 video frame
            ret, frame = self.video_source.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #self.stdscr.addstr(0,10,"orig size {} {}".format(c, frame.shape))
            frame = self.scale(frame=frame)
            #self.stdscr.addstr(1,10,"resized {} {}".format(c, frame.shape))
            #self.stdscr.addstr(2,0,"sdf {} {}".format(frame[10,10], self.gradient_string[3]))
            self.draw(frame=frame)
            self.stdscr.refresh()
            #time.sleep(0.5)



    def clean(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def scale(self, frame):
        #based on https://stackoverflow.com/a/64884087
        max_height, max_width =  self.stdscr.getmaxyx()
        '''
        height, width = frame.shape[:2]
        f1 = max_width / width
        f2 = max_height / height
        f = min(f1, f2)  # resizing factor
        dim = (int(frame.shape[1] * f), int(frame.shape[0] * f))
        return cv2.resize(frame, dim)'''
        return cv2.resize(frame, (max_width, max_height))


    
    def draw(self, frame):
        max_height, max_width =  self.stdscr.getmaxyx()
        n_levels : int = len(self.gradient_string)
        bucket_size = int(256)/int(n_levels)

        height, width = frame.shape[:2]
        for h in range(0,height):
            for w in range(0,width):
                gradient_index : int = int( int(frame[h,w])/int(bucket_size))
                if gradient_index >= n_levels:
                    gradient_index = n_levels -1

                try:
                    self.stdscr.addstr(h, w, self.gradient_string[gradient_index])
                except curses.error:
                    pass


if __name__ == "__main__":
    display = LetterDisplay()
    display.start()
    display.clean()
