# VGGishAudioData

Convenience methods for parsing audio into formats VGGish can read.

## Quickstart

## Installation

## API

All methods return self unless otherwise noted.

### `init`

Initializes the model, and accepts a number of arguments for initializing the object.

Defaults to a single channel (mono), 44100 frame rate, 16 bits (CD quality) with no transforms and no initial data.

```
audioData = AudioData(channels=1, frame_rate=44100, bits=32)
```

### `set_channels`

Set the number of channels for audio files. Defaults to a single channel (mono).

```
audioData.set_channels(2)
```

### `set_frame_rate`

```
audioData.set_frame_rate(44100)
```

### `set_bits`

```
audioData.set_bits(16)
```

### `add_data`

Adds data for later retrieval.

```
audioData.add_data(type='train', data=['/path/to/file.wav', '/path/to/dir/of/files'], label='some_label')

# can also infer labels from the file or directory names. These will be labeled "label_one" and "label_two"
audioData.add_data(type='train', data=[
  'data/label_one/file.wav', # a single file
  'data/label_two', # a directory of files
])
```

### `get_data`

Retrieves data for a particular `type`. Optionally will perform on-the-fly data augmentation if `transforms` is specified.

Specify `returns` to select which information to retrieve for the audio samples. Options are 'audio' (a pydub audio segment), `samples` (a numpy array of samples representing the audio), `label` (the associated label), `file` (the original file path the audio came from) and `start` (the starting index of the audio chunk).

Returns an array of dicts representing each chunk of audio.

```
audioData.get_data(type='train')

# split training data into train and validation sets
audioData.get_data(type='train', split=.1)

# shuffle the data
audioData.get_data(type='train', shuffle=True)

# perform transforms on the data
audioData.get_data(type='train', transforms=[])

# use a rolling start window (a random value is chosen from a full sample chunk) to introduce more variability into the training samples
audioData.get_data(type='train', random_window=True)

# specify the type of information to be returned
audioData.get_data(type='train', returns=['audio', 'samples', 'label', 'file', 'start'])
```
