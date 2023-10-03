from transcribe_given_audio_file import Transcribe_ATC
import numpy as np
import requests
import subprocess

transcription_buffer = []

# this object does the transcription
transcribe = Transcribe_ATC()


def fetch_stream():
    # Read stream, save to wav
    stream_url = "http://d.liveatc.net/kdab_del_gnd"
    return requests.get(stream_url, stream=True)


def get_transcription_array(filename):
    # Convert mp3 to wav
    subprocess.call(["ffmpeg", "-y", "-i", filename, "stream.wav"])
    # TODO address error: Estimating duration from bitrate, this may be inaccurate
    # [src/libmpg123/layer3.c:INT123_do_layer3():1773] error: part2_3_length (1088) too large for available bit count (712)

    # Pass file to model, get transcription result
    return transcribe.transcribe_audio("stream.wav")


def audio_fetch_and_transcribe():
    global transcription_buffer

    r = fetch_stream()
    filename = "stream.mp3"

    for block in r.iter_content(6144):
        # Write 3 seconds of streamed data to the file
        with open(filename, "wb") as f:
            f.write(block)
        f.close()

        # Transcribe
        transcription = get_transcription_array(filename)
        if transcription:
            transcription_buffer += transcription.split(" ")  # Add new words to array
            transcription_buffer = transcription_buffer[
                -20:
            ]  # Truncate the array to only the last 20

        print(f"transcription_buffer: {transcription_buffer}")


def get_latest_transcription():
    return " ".join(transcription_buffer)
