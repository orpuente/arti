# pip install pyaudio requests websockets
import threading
from queue import Queue
from video import video_processing
from microphone import microphone_processing
from speaker import speaker

LANGUAGE = 'es'
AUDIO_INPUT = 1
VIDEO_INPUT = 0

# Queues

def main():
	mic_to_video = Queue(maxsize=50)
	video_to_speaker = Queue(maxsize=50)
	t1 = threading.Thread(target=microphone_processing, args=(AUDIO_INPUT, mic_to_video), daemon=True)
	t2 = threading.Thread(target=video_processing, args=(VIDEO_INPUT, LANGUAGE, mic_to_video, video_to_speaker))
	t3 = threading.Thread(target=speaker, args=(LANGUAGE, video_to_speaker), daemon=True)
	t1.start()
	t2.start()
	t3.start()
	t2.join()

if __name__ == '__main__':
	main()