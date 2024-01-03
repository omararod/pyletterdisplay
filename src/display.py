import curses
import cv2
import signal

COLOR_MODE = cv2.COLOR_BGR2GRAY
#we assume 8-bit color since it seems to be OpenCV default for black & white
PIXEL_LEVELS = 256

class LetterDisplay:
    def __init__(self):
        self.continue_running = True
        #get default video source
        self.video_source = cv2.VideoCapture(0)
        if not self.video_source.isOpened():
           print("Failed to open default video source. Exiting...")
           exit(1)
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        #string with characters representing the levels of gray to be used from darker to lighter
        self.gradient_string = " .:-=+*#%@"

    '''
    Starts the application. It performs the following actions on a loop:
    - Get a frame from the default video source
    - Converts the frame to black & white
    - Scales the frame to the terminal's max rows and columns
    - Calls the draw function
    '''
    def start(self):
        while self.continue_running:
            #get 1 video frame
            ret, frame = self.video_source.read()
            if ret == False:
                print("Failed obtaining frame from video source")
                break
            frame = cv2.cvtColor(frame, COLOR_MODE)
            #scale the image to the size of the terminal
            frame = self.scale(frame=frame)
            #draw the frame
            self.draw(frame=frame)
            
    '''
    Restores the terminal to its pre-curses state
    '''
    def clean(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    '''
    Scales an OpenCV frame to the max row and column size of the terminal
    '''
    def scale(self, frame):
        max_height, max_width =  self.stdscr.getmaxyx()
        return cv2.resize(frame, (max_width, max_height))

    '''
    Maps each pixel of a scaled OpenCV frame to a character corresponding 
    to its gray level and prints it on screen 
    '''
    def draw(self, frame):
        n_levels : int = len(self.gradient_string)
        bucket_size = int(PIXEL_LEVELS)/int(n_levels)

        height, width = frame.shape[:2]
        #loop over the frame's pixels
        for h in range(0,height):
            for w in range(0,width):
                #map gray level to a character
                gradient_index : int = int( int(frame[h,w])/int(bucket_size))
                if gradient_index >= n_levels:
                    gradient_index = n_levels -1
                try:
                    self.stdscr.addstr(h, w, self.gradient_string[gradient_index])
                except curses.error:
                    pass
        #refresh the terminal
        self.stdscr.refresh()
    
    def signal_handler(self, sig, frame):
        #set to false so the loop in the start() function stops
        self.continue_running = False
        print("Stopping application...")


if __name__ == "__main__":
    display = LetterDisplay()
    signal.signal(signal.SIGINT, display.signal_handler)
    display.start()
    display.clean()
