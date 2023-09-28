import subprocess


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


class Combiner:

    def train(self, video_filepath):
        pass

    def combine(self, audio_filepath, video_filepath, output_filepath):
        return output_filepath


class MockCombiner(Combiner):
    pass


class Wav2LipCombiner(Combiner):

    def train(self, video_filepath):
        pass

    def combine(self, audio_filepath, video_filepath, output_filepath):

        command = f'''python /app/lib/wav2lip-hq/inference.py \
            --checkpoint_path "/app/lib/wav2lip-hq/checkpoints/wav2lip_gan.pth" \
            --segmentation_path "/app/lib/wav2lip-hq/checkpoints/face_segmentation.pth" \
            --sr_path "/app/lib/wav2lip-hq/checkpoints/esrgan_yunying.pth" \
            --save_frames \
            --face {video_filepath} \
            --audio {audio_filepath} \
            --outfile {output_filepath}'''
        for line in execute(command):
            print(line, end="")
        return output_filepath


