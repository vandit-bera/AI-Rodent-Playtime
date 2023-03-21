from re import search
from typing import List
import cv2
import mediapipe as mp
from helper import *

def process_image_hand_detection(hands, image, stored_keys, key=None, mp_hands=mp.solutions.hands, mp_drawing=mp.solutions.drawing_utils, mp_drawing_styles=mp.solutions.drawing_styles):
	# To improve performance, optionally mark the image as not writeable to
	# pass by reference.
	text = ""
	image.flags.writeable = False
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	results = hands.process(image)

	# Draw the hand annotations on the image.
	image.flags.writeable = True
	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
	if results.multi_hand_landmarks:
		for hand_landmarks in results.multi_hand_world_landmarks:
			process_landmark(hand_landmarks.landmark)
			if key:
				print("Key pressed: " + key)
				store_new_pose(hand_landmarks.landmark, key, stored_keys)
				print(stored_keys)

			text = search_hand_pose(hand_landmarks.landmark, stored_keys)
			if text:
				image_text = "Key Detected: " + text
			else:
				image_text = "Hand is Detected"

		for hand_landmarks in results.multi_hand_landmarks:
			mp_drawing.draw_landmarks(
				image,
				hand_landmarks,
				mp_hands.HAND_CONNECTIONS,
				mp_drawing_styles.get_default_hand_landmarks_style(),
				mp_drawing_styles.get_default_hand_connections_style())

		# Flip the image horizontally for a selfie-view display.
		image = cv2.flip(image, 1)

		textsize = cv2.getTextSize(image_text, font, fontScale, thickness)[0]
		# get coords based on boundary
		textX = (image.shape[1] - textsize[0]) // 2
		textY = 900

		image = cv2.putText(image, image_text, (textX, textY), font, 
							fontScale, color, thickness, cv2.LINE_AA)
	else:
		image = cv2.flip(image, 1)
		image_text = "No Hands Detected"
		image = cv2.putText(image, image_text, org, font, 
							fontScale, color, thickness, cv2.LINE_AA)
	
	return image, text

if __name__ == "__main__":
	stored_keys = {}
	cap = cv2.VideoCapture(0)

	mp_drawing = mp.solutions.drawing_utils
	mp_drawing_styles = mp.solutions.drawing_styles
	mp_hands = mp.solutions.hands

	with mp_hands.Hands(
		static_image_mode=False,
		max_num_hands=1, # TODO: Implement Multiplayer with multiple hands
		model_complexity=0, # for faster speed
		min_detection_confidence=0.8,
		min_tracking_confidence=0.5) as hands:
		while cap.isOpened():
			success, image = cap.read()
			if not success:
				print("Ignoring empty camera frame.")
				# If loading a video, use 'break' instead of 'continue'.
				continue

			if cv2.waitKey(33) == ord('a'):
				image = process_image_hand_detection(hands, image, stored_keys,'a')
			else:
				image = process_image_hand_detection(hands, image, stored_keys)
			cv2.imshow('MediaPipe Hands', image)
			if cv2.waitKey(5) & 0xFF == 27:
				break

	cap.release()