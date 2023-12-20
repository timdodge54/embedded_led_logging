import cv2
import numpy as np
import numpy.typing as npt


class Led_Detector:
    """Class that detects led blinking and decripts it into moris code"""

    def __init__(
        self,
        capture_frequency: int = 30,
        dot_length: int = 4,
        dash_length: int = 8,
        space_length: int = 4,
        char_end_length: int = 16
    ) -> None:
        """Initialize.

        Args:
            capture_frequency: The frequency of the capture. Defaults to 30.
            dot_length: The number of frames that the led should be on
                for a dot. Defaults to 4.
            dash_length: The number of frames that the led should be on
                for a dash. Defaults to 8.
            space_length: The number of frames that the led should be off
                for a space. Defaults to 4.
            word_end_length: The number of frames that the led should be off
                for a word end. Defaults to 16.
        """
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FPS, capture_frequency)
        self.cap_interval = int(1 / capture_frequency * 1000)
        self.dot_length = dot_length
        self.dash_length = dash_length
        self.space_length = space_length
        self.char_end_length = char_end_length
        self.prev_state = 0
        self.prev_state_counter = 0
        self.charectar_buffer = []

    def detect(self):
        """Detects the led and thresholds the video to binary image"""
        # read the frame
        _, frame = self.cap.read()
        frame_with_conturs = frame.copy()

        # convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # threshold into binary image where 1 if 255> i > 200  and 0 otherwise
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        self.iterate_state(thresh)

        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame_with_conturs, contours, -1, (0, 255, 0), 2)
        # Draw frame with contours
        cv2.imshow('frame', frame_with_conturs)
        cv2.imshow('thresh', thresh)

    def detect_loop(self):
        """The main loop that calls the detect function."""
        while True:
            self.detect()
            key = cv2.waitKey(self.cap_interval) & 0xFF
            if key == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

    def iterate_state(self, threshold: npt.NDArray[np.uint8]):
        """Process the threshold, iterates state, and detect if char is done.

            Args:
                threshold (np.array): The thresholded image.

        """
        all_zeros = np.all(threshold == 0)
        if all_zeros:
            if self.prev_state == 0:
                # iterate the number of times the led was off
                self.prev_state_counter += 1
            else:
                self.prev_state = 0
                if self.prev_state_counter >= self.char_end_length:
                    self.decode()
                else:
                    if self.prev_state_counter <= self.dot_length:
                        self.char_buffer.append('.')
                    else:
                        self.char_buffer.append('-')
            self.prev_state_counter = 0
        else:
            if self.prev_state == 1:
                self.prev_state_counter += 1
            if self.prev_state == 0:
                self.prev_state_counter = 0

    def decode(self):
        """Decodes a char when a char end is detected."""
        self.char_buffer = []


if __name__ == "__main__":
    led = Led_Detector()
    led.detect_loop()
