# camera processing
import time
import ultralytics
import cv2
from collections import deque
from functools import cache
from ultralytics.yolo.engine.results import Results, Boxes
from ultralytics.yolo.utils.plotting import Annotator, colors
from ultralytics.yolo.utils.checks import is_ascii
from copy import deepcopy
from translate import Translator

MAX_DEQUE_LEN = 30

class BoundingBox:
	def __init__(self, box, name):
		self.box = box
		self.name = name

def bounding_boxes_from_results(result: Results, names: list[str]):
	boxes = []
	for i in range(len(result)):
		name = names[i]
		box = BoundingBox(result.boxes[i], name)
		boxes.append(box)
	return boxes

def get_most_frequent_classification(classification_frequencies):
	max_element = max(
		classification_frequencies,
		key = lambda x: classification_frequencies.count(x)
	)
	max_element_index = list(reversed(classification_frequencies)).index(max_element)
	return len(classification_frequencies) - max_element_index - 1

mouse_x, mouse_y = 0,0
def mouseCallback(event, x, y, flags, param):
	global mouse_x
	global mouse_y
	mouse_x = x
	mouse_y = y

def video_processing(input_device, language, mic_to_video, video_to_speaker):
	# ultralytics.checks()
	cap = cv2.VideoCapture(input_device)
	model = ultralytics.YOLO("yolov8n.pt")
	show_label_until = 0
	bounding_boxes_deque = deque()
	classification_frequencies = deque()
	cv2.namedWindow('ARTI', cv2.WINDOW_AUTOSIZE)
	cv2.setMouseCallback('ARTI', mouseCallback)
	
	translator = Translator(to_lang=language)
		
	@cache
	def translate_cached(text):
		return translator.translate(text)
	
	while cap.isOpened():
		# Read a frame from the video
		success, frame = cap.read()

		if success:
			# Run YOLOv8 inference on the frame
			result = model.predict(frame, conf = 0.5, device=0, verbose=False)[0]

			classifications_dict = result.names
			classifications_ids = [
				int(result.boxes[i].cls) for i in range(len(result.boxes))
			]
			ids_set = set(classifications_ids)
			classification_freq = set((id, classifications_ids.count(id)) for id in ids_set)
			names = [classifications_dict[id] for id in classifications_ids]

			classification_frequencies.appendleft(classification_freq)
			while len(classification_frequencies) > MAX_DEQUE_LEN:
				classification_frequencies.pop()
			
			bounding_boxes = bounding_boxes_from_results(result, names)
			bounding_boxes_deque.appendleft(bounding_boxes)
			while len(bounding_boxes_deque) > MAX_DEQUE_LEN:
				bounding_boxes_deque.pop()
			# get most frequent classification_freq in the last 60 frames or so
			most_freq: int = get_most_frequent_classification(classification_frequencies)

			# get the most frequent set of bounding_boxes correspoinding to the most frequent `classification_freq`
			stable_bounding_boxes: list[BoundingBox] = bounding_boxes_deque[most_freq]

			annotator = Annotator(deepcopy(result.orig_img),
								line_width=None,
								font_size=None,
								font='Arial.ttf',
								pil=True,
								example=result.names)
			
			if stable_bounding_boxes:
				# get smallest bounding box containing mouse
				smallest_box = None
				smallest_area = float('inf')
				for bb in reversed(stable_bounding_boxes):
					d = bb.box
					x1, y1, x2, y2 = d.xyxy[0]
					
					if x1 < mouse_x < x2 and y1 < mouse_y < y2:
						area = abs((x2 - x1) * (y2 - y1))
						if area < smallest_area:
							smallest_box = d
							smallest_area = area
			
				if smallest_box:
					d = smallest_box
					c, conf, id = int(d.cls), float(d.conf), None if d.id is None else int(d.id.item())
					name = ('' if id is None else f'id:{id} ') + result.names[c]
					translated_name = translate_cached(name)

					# if we get a msg, show the label for 5 seconds and send a word to the speaker
					timestamp = time.time()
					if not mic_to_video.empty():
						if timestamp >= show_label_until:
							mic_to_video.get(block=False)
							show_label_until = timestamp + 5
							video_to_speaker.put(translated_name)
						else:
							mic_to_video.get(block=False)
					print_label = timestamp < show_label_until

					label = (f'{translated_name} {conf:.2f}' if conf else translated_name) if print_label else None
					
					# This is to avoid an internal case in the anotator, where it requires PIL when the label is non_ascii
					# if not is_ascii(label): label = None
					
					annotator.box_label(d.xyxy.squeeze(), label, color=colors(c, True))
			
			my_frame = annotator.result()
			cv2.imshow("ARTI", my_frame)

			# Break the loop if 'q' is pressed
			if cv2.waitKey(1) & 0xFF == ord("q"):
				break
		else:
			break
		
	cap.release()
	cv2.destroyAllWindows()