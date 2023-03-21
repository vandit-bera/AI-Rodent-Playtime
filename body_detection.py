import cv2
import mediapipe as mp
from helper import *
from matplotlib.animation import FuncAnimation

import pyautogui


def store_reference_position(pose, image):
	# To improve performance, optionally mark the image as not writeable to
	# pass by reference.
	image.flags.writeable = False
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	results = pose.process(image)

	reference_landmark = None
	if results.pose_landmarks:
		reference_landmark = results.pose_landmarks.landmark

	return reference_landmark

def check_jump(landmarks, reference): # this is inverted but it works??
	"""
	# We first apply a scaling factor, by checking the distance between the the shoulders, so
	it can detect a jump.
	
	Define height of jump as 1/5 of the width of the shoulders.
	"""
	vertical_threshold = 0.2 # If there is a vertical increase by 0.1m, then we consider this a jump
	dist_ref = compute_distance(reference[12], reference[11])
	dist_landmarks = compute_distance(landmarks[12], landmarks[11])
	
	dist = (landmarks[11].y - reference[11].y)

	return dist > vertical_threshold * dist_ref

def check_right(reference, landmarks):
	"""
	# We first apply a scaling factor, by checking the distance between the the shoulders, so
	it can detect a jump.
	
	Define height of jump as 1/5 of the width of the shoulders.
	"""
	vertical_threshold = 0.2 # If there is a vertical increase by 0.1m, then we consider this a jump
	# dist_ref = compute_distance(reference[12], reference[11])
	
	dist = abs(landmarks[16].y - landmarks[12].y)

	# return dist > vertical_threshold * dist_ref
	return dist < vertical_threshold

def check_left(reference, landmarks):
	"""
	# We first apply a scaling factor, by checking the distance between the the shoulders, so
	it can detect a jump.
	
	Define height of jump as 1/5 of the width of the shoulders.
	"""
	vertical_threshold = 0.2 # If there is a vertical increase by 0.1m, then we consider this a jump
	# dist_ref = compute_distance(reference[12], reference[11])
	
	dist = abs(landmarks[11].y - landmarks[15].y)

	# return dist > vertical_threshold * dist_ref
	return dist < vertical_threshold

def check_crouch(reference, landmarks):
	"""
	# We first apply a scaling factor, by checking the distance between the the shoulders, so
	it can detect a jump.
	
	Define height of jump as 1/5 of the width of the shoulders.
	
	This doesn't work super well.
	"""
	vertical_threshold = 0.5 # If there is a vertical increase by 0.1m, then we consider this a jump
	dist_ref = compute_distance(reference[12], reference[11])
	dist_landmarks = compute_distance(landmarks[12], landmarks[11])
	
	dist = abs(landmarks[11].y - reference[11].y)

	return dist > vertical_threshold * dist_ref

def process_image_body_detection(pose, image, stored_keys, reference_landmark, key=None, mp_pose=mp.solutions.pose, mp_drawing=mp.solutions.drawing_utils, mp_drawing_styles=mp.solutions.drawing_styles, counter=[0]):
	# To improve performance, optionally mark the image as not writeable to
	# pass by reference.
	image.flags.writeable = False
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	results = pose.process(image)

	# Draw the pose annotation on the image.
	image.flags.writeable = True
	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

	# process_landmark(results.pose_landmarks.landmark)
	if results.pose_landmarks:
		if key:
			print("Key pressed: " + key) # Store the binding
			store_new_pose(results.pose_landmarks.landmark, key, stored_keys)
			print(stored_keys)

		if reference_landmark and check_jump(reference_landmark, results.pose_landmarks.landmark):
			print("jump detected")
			# Press both buttons
			pyautogui.press("up")

		if reference_landmark and check_left(reference_landmark, results.pose_landmarks.landmark):
			print("left detected")
			if counter[0] == 0:
				pyautogui.press("left")
				counter[0] = 1
			
		if reference_landmark and check_right(reference_landmark, results.pose_landmarks.landmark):
			print("right detected")
			if counter[0] == 0:
				pyautogui.press("right")
				counter[0] = 1

		if reference_landmark and check_crouch(reference_landmark, results.pose_landmarks.landmark):
			print("crouch detected")
			pyautogui.press("down")

		# plot_realtime(results.pose_landmarks.landmark) # TODO: Add graph visualization if you have time
		text = "Body is Detected"
		mp_drawing.draw_landmarks(
			image,
			results.pose_landmarks,
			mp_pose.POSE_CONNECTIONS,
			landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
		# Flip the image horizontally for a selfie-view display.
	else:
		text = "No Body Detected"

	image = cv2.flip(image, 1)

	textsize = cv2.getTextSize(text, font, fontScale, thickness)[0]

	# get coords based on boundary
	textX = (image.shape[1] - textsize[0]) // 2
	textY = 900
	image = cv2.putText(image, text, (textX, textY), font, 
						fontScale, color, thickness, cv2.LINE_AA)

	return image


def capture_initial_position(image, counter): 
	"""

	Once the counter reaches 0, we initiate the picture capture
	
	"""
	image = cv2.putText(image, "Countdown: " + str(counter / 10), (600, 100), font, 
						3, color, 12, cv2.LINE_AA)
	
	return image

if __name__ == "__main__":

	mp_drawing = mp.solutions.drawing_utils
	mp_drawing_styles = mp.solutions.drawing_styles
	mp_pose = mp.solutions.pose

	stored_keys = {}
	# For webcam input:
	cap = cv2.VideoCapture(0)
	
	counter = 50
	
	reference_landmark = None
	with mp_pose.Pose(
			min_detection_confidence=0.5,
			min_tracking_confidence=0.5) as pose:
		while cap.isOpened():
			success, image = cap.read()
			if not success:
				print("Ignoring empty camera frame.")
				# If loading a video, use 'break' instead of 'continue'.
				continue


			if counter == 0 and not reference_landmark:
				reference_landmark = store_reference_position(pose, image)

			image = process_image_body_detection(pose, image, stored_keys, reference_landmark)

			if (counter > 0):
				image = capture_initial_position(image, counter)
				counter -= 1

			cv2.imshow('MediaPipe Pose', image)

			if cv2.waitKey(5) & 0xFF == 27:
				break

	cap.release()