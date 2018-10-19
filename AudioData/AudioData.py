from .utils import get_label_from_file, get_files_from_dir
from .utils import get_sliced_audio_files, get_transformed_files
from .utils import shuffle_chunks, separate_chunks, split_data
import os
import numpy as np
from typing import Dict, List
from .vggish_input import waveform_to_examples
from pydub import AudioSegment

DEFAULTS = {
    'channels': 1,
    'bytes': 2,
    'sample_rate': 44100,
}

class AudioData:
    def __init__(self, channels:int = DEFAULTS['channels'], bytes:int =
            DEFAULTS['bytes'], sample_rate:int = DEFAULTS['sample_rate']):

        assert sample_rate > 0, "Frame rate must be greater than 0"

        self._files = {} # type: Dict[str, List[Dict]]

        self.set_channels(channels)
        self.set_bytes(bytes)
        self.set_sample_rate(sample_rate)

    def set_channels(self, channels:int):
        assert channels >= 1 and channels <= 2, "Channels must be between 1 and 2 channels"
        self.channels = channels
        self.reprocess_audio()

    def set_bytes(self, bytes:int):
        assert bytes > 0, "Bytes must be greater than 0"
        self.bytes = bytes
        self.reprocess_audio()

    def set_sample_rate(self, sample_rate:int):
        assert sample_rate > 0, "Frame Rate must be greater than 0"
        self.sample_rate = sample_rate
        self.reprocess_audio()

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

    def load(self, path):
        audio = AudioSegment.from_file(path)
        audio = self.preprocess_audio(audio)
        return audio

    def reprocess_audio(self):
        for file in self._files:
            audio = self.load(file['file'])
            file['audio'] = audio

    def _add_file(self, type, file, label):
        if label is None:
            file_label = get_label_from_file(file)
        else:
            file_label = label

        audio = self.load(file)
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
        chunks = self.slice_into_single_sample_chunks(files)

        #4. shuffle
        chunks = shuffle_chunks(chunks, shuffle)

        #5. separate into components
        samples, audio, labels, refs = separate_chunks(chunks, [
            'samples',
            'audio',
            'label',
            [
                'file',
                'start_index',
            ],
        ])

        #6. split the data
        splits = split_data(split, samples, labels, refs)

        return splits

    def preprocess_audio(self, audio):
        channels = self.channels
        bytes = self.bytes
        sample_rate = self.sample_rate

        if audio.channels != channels:
            audio = audio.set_channels(channels)

        if audio.sample_width != bytes:
            audio = audio.set_sample_width(bytes)

        if audio.frame_rate != sample_rate:
            audio = audio.set_frame_rate(sample_rate)

        return audio

    def waveform_to_examples(self, samples):
        return waveform_to_examples(np.array(samples), sample_rate=self.sample_rate)

    def slice_into_single_sample_chunks(self, files):
        chunks = []
        for file in files:
            audio = file['audio']
            samples = audio.get_array_of_samples()
            sample_rate = self.sample_rate
            assert audio.frame_rate == self.sample_rate
            assert audio.sample_width == self.bytes
            assert audio.channels == self.channels
            for i in range(0, len(samples), sample_rate):
                start = i
                end = start + sample_rate
                if len(samples) >= end:
                    sliced_samples = samples[start:end]
                    vggish_samples = self.waveform_to_examples(sliced_samples)
                    assert len(vggish_samples) == 1
                    chunks.append({
                        'samples': sliced_samples,
                        'vggish_samples': vggish_samples,
                        'file': file['file'],
                        'start_index': i + file['start_index'],
                        # 'audio': file['audio'][start:end],
                        'label': file['label'],
                    })
        return chunks
