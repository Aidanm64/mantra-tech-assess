import os


class Combiner:

    def train(self, video_filepath):
        pass

    def combine(self, audio_filepath, video_filepath, output_filepath):
        return output_file_path


class MockCombiner(Combiner):
    pass


class Wav2LipCombiner(Combiner):

    def train(self, video_filepath):
        pass

    def combine(self, audio_filepath, video_filepath, output_filepath):
        return output_filepath