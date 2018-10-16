from .utils import get_label_from_file, get_files_from_dir
from .utils import get_sliced_audio_files, get_transformed_files
from .utils import shuffle_chunks, separate_chunks, split_data
from .utils import load
import os
from typing import Dict, List
from .vggish_input import waveform_to_examples

DEFAULTS = {
    'channels': 1,
    'bytes': 2,
    'frame_rate': 44100,
}

class AudioData:
    def __init__(self, channels:int = DEFAULTS['channels'], bytes:int =
            DEFAULTS['bytes'], frame_rate:int = DEFAULTS['frame_rate']):

        assert frame_rate > 0, "Frame rate must be greater than 0"

        self._files = {} # type: Dict[str, List[Dict]]

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
                files = get_files_from_dir(file, r"(.*)\.wav$")
                for file in files:
                    self._add_file(type, file, label)
            else:
                assert os.path.isfile(file), "File %s is not valid" % (file)
                self._add_file(type, file, label)

    def _add_file(self, type, file, label):
        if label is None:
            file_label = get_label_from_file(file)
        else:
            file_label = label

        audio = load(file)
        self._files[type].append({
            'audio': audio,
            'file': file,
            'label': file_label,
        })

    """ Returns a tuple:
   samples - either a single numpy array, (,96,64), or two numpy arrays, if
   split

   labels - either a single array of labels, or two arrays, if split. NOT one
   hot encoded

   audio_segments - an array of objects, that contain a 1 second pydub segment, the path
   of the file, and the starting index (in samples) of the file

    """
    def get_data(self, type: str, split: float = None, shuffle: bool = False,
            transforms = [], random_window: bool = True, returns = []):
        files = self._files[type].copy()

        #1. if random window, slice off one second of audio files
        files = get_sliced_audio_files(files, random_window)

        #2. transform those files
        files = get_transformed_files(files, transforms)

        #3. slice into chunks
        chunks = self.slice_into_chunks(files, channels=self.channels, bytes=self.bytes, frame_rate=self.frame_rate)

        #4. balance data
        print('also balance data')

        #5. shuffle
        chunks = shuffle_chunks(chunks, shuffle)

        #6. separate into components
        samples, audio, labels, refs = separate_chunks(chunks, [
            'samples',
            'audio',
            'label',
            [
                'file',
                'start_index',
            ],
        ])

        #7. split the data
        splits = split_data(split, samples, labels, refs)

        return splits

    def preprocess_audio(self, audio, channels:int = None, bytes: int = None,
            frame_rate: int = None):
        if channels is None:
            channels = self.channels
        if bytes is None:
            bytes = self.bytes
        if frame_rate is None:
            frame_rate = self.frame_rate

        audio = audio.set_channels(channels)
        audio = audio.set_sample_width(bytes)
        audio = audio.set_frame_rate(frame_rate)
        return audio

    def slice_into_chunks(self, files, **kwargs):
        chunks = []
        for file in files:
            audio = self.preprocess_audio(file['audio'], **kwargs)
            samples = audio.get_samples_as_array()
            print('update this to handle other frame rates')
            frame_rate = 44100
            for i in range(0, len(samples), frame_rate):
                start = i
                end = start + frame_rate
                if len(samples) >= end:
                    sliced_samples = samples[start:end]
                    chunks.append({
                        'samples': sliced_samples,
                        'vggish_samples': waveform_to_examples(sliced_samples),
                        'file': file['file'],
                        'start_index': i + file['start_index'],
                        # 'audio': file['audio'][start:end],
                        'label': file['label'],
                    })
        return chunks
