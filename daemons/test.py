import threading
import time
import sys
import os

"""
AOS Daemon

Can be used either by cloning this and editing the code, or by creating a new file and subclassing from this class.
AOS does not enforce either paradigm, whatever is needed is acceptable.
"""
class AOSDaemon:
    def __init__(self, pipe = "test"):
        self.running = True
        self.pipe_name = pipe

    # Subclass overrides
    def __on_timer__(self):
        "Event that runs every second."
        pass

    def __on_message__(self, message):
        "Event that runs when pipe gets a message."
        pass


    def __on_close__(self):
        "Event that runs when process has been closed"
        pass

    def __timer__(self, delay = 1):
        while self.running:
            time.sleep(delay)
            self.__on_timer__()


    def log(self, text, prefix = "(>"):
        print(prefix, text)

    def __listen__(self):
        """Function to listen for input"""
        self.pipe_path = f'/tmp/{self.pipe_name}'
        if not os.path.exists(self.pipe_path):
            os.mkfifo(self.pipe_path)
        self.log(f"Listening on {self.pipe_path}..")
        # Open the pipe for reading
        with open(self.pipe_path, 'r') as pipe:
            while self.running:
                message = pipe.read().strip()
#
                if message:
                    self.log(message)
                    if message in ["end", "quit", "shutdown", "kill"]:
                        self.log("Received kill signal!", "!!")
                        self.close()

                    if message == "info":
                        self.send("aos_reply", "This is a test daemon message.")

                    self.__on_message__(message)

        # Clean up
        os.remove(self.pipe_path)

    def close(self):
        self.log("Calling shutdown events...", "!!")
        self.__on_close__()

        self.log("Terminating threads...", "!!")
        self.running = False

        try:
            self.log("Cleaning filesystem...", "!!")
            os.remove(self.pipe_path)
        except Exception as e:
            print(e)

        self.log("Sending exit signal...", "!!")
        sys.exit(0)

    def send(self, pipe_name, message):
        pipe_path = f'/tmp/{pipe_name}'

        # Open the pipe for writing
        with open(pipe_path, 'w') as pipe:
            pipe.write(message + '\n')
            pipe.flush()

    def __run__(self):
        # Create and start the timer thread
        self.timer_thread = threading.Thread(target=self.__timer__)
        self.timer_thread.daemon = True  # Set as daemon so it exits when the main program does
        self.timer_thread.start()

        # Create and start the input listener thread
        self.input_thread = threading.Thread(target=self.__listen__)
        self.input_thread.daemon = True
        self.input_thread.start()

        # Keep the main thread alive
        while self.running:
            time.sleep(1)

if __name__ == "__main__":
    d = AOSDaemon()
    try:
        d.__run__()

    except KeyboardInterrupt:
        d.log("KeyboardInterrupt", "!!")
        os.remove(d.pipe_path)
        sys.exit(0)
