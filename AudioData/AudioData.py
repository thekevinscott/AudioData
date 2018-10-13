from .utils import getLabelFromFile, getFilesFromDir
import os

DEFAULTS = {
    'channels': 1,
    'bytes': 2,
    'frame_rate': 44100,
}

class AudioData:
    def __init__(self, channels:int = DEFAULTS['channels'], bytes:int =
            DEFAULTS['bytes'], frame_rate:int = DEFAULTS['frame_rate']):

        assert frame_rate > 0, "Frame rate must be greater than 0"

        self._files = {}

        self.set_channels(channels)
        self.set_bytes(bytes)
        self.set_frame_rate(frame_rate)

    def set_channels(self, channels:int):
        assert channels >= 1 and channels <= 2, "Channels must be between 1 and 2 channels"
        self.channels = channels

    def set_bytes(self, bytes:int):
        assert bytes > 0, "Bytes must be greater than 0"
        self.bytes = bytes

    def set_frame_rate(self, frame_rate:int):
        assert frame_rate > 0, "Frame Rate must be greater than 0"
        self.frame_rate = frame_rate

    def clear_data(self, type:str = None):
        if type is not None:
            self._files[type] = []
        else:
            self._files = {}

    def add_data(self, type: str, data, label = None):
        for file in data:
            if type not in self._files:
                self._files[type] = []

            if os.path.isdir(file):
                files = getFilesFromDir(file, r"(.*)\.wav$")
                for file in files:
                    self._add_file(type, file, label)
            else:
                self._add_file(type, file, label)

    def _add_file(self, type, file, label):
        if label is None:
            file_label = getLabelFromFile(file)
        else:
            file_label = label

        self._files[type].append({
            'file': file,
            'label': file_label,
        })
