from watchdog.events import FileSystemEventHandler
import os

class file_observer(FileSystemEventHandler):
    
    def __init__(self, callback, **kwargs):
        super(file_observer, self).__init__(**kwargs)
        self.callback = callback

    def on_created(self, event):
        if (event.is_directory):
            pass
        if (os.path.splitext(event.src_path)[1] == '.SC2Replay'):
            self.callback(new_replay= event.src_path)