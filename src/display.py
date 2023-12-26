import curses
import cv2

N_FRAMES = 500
class LetterDisplay:
    def __init__(self):
        #get default video source
        self.video_source = cv2.VideoCapture(0)
        if not self.video_source.isOpened():
           print("Failed to open default video source. Exiting...")
           exit(1)
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        self.gradient_string = " .:-=+*#%@"

    def start(self):
        for c in range(0, N_FRAMES):
            #get 1 video frame
            ret, frame = self.video_source.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #scale the image to the size of the terminal
            frame = self.scale(frame=frame)
            #draw the frame
            self.draw(frame=frame)
            self.stdscr.refresh()

    def clean(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def scale(self, frame):
        max_height, max_width =  self.stdscr.getmaxyx()
        return cv2.resize(frame, (max_width, max_height))

    def draw(self, frame):
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
