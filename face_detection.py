import cv2
import mediapipe as mp
from helper import *
import pyautogui

def check_mouth_open(landmarks):
	return (landmarks[14].y - landmarks[13].y) > 0.05


def process_image_face_detection(face_mesh, image, stored_keys, key=None, mp_drawing=mp.solutions.drawing_utils, mp_drawing_styles=mp.solutions.drawing_styles, mp_face_mesh=mp.solutions.face_mesh):
	"""
	store is an additional argument if you want to store it to the dict of stored_keys
	
	"""
	# To improve performance, optionally mark the image as not writeable to
	# pass by reference.
	image.flags.writeable = False
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	results = face_mesh.process(image)

	# Draw the face mesh annotations on the image.
	image.flags.writeable = True
	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
	if results.multi_face_landmarks:
		for face_landmarks in results.multi_face_landmarks:
			if key:
				store_new_pose(face_landmarks.landmark, key, stored_keys)

			if check_mouth_open(face_landmarks.landmark):
				text = "Mouth is Open"
				pyautogui.press("up")
			else:
				text = "Mouth is Closed"

			# text = search_face_pose(face_landmarks.landmark, stored_keys) # TODO: Add counter if this is too slow
			mp_drawing.draw_landmarks(
					image=image,
					landmark_list=face_landmarks,
					connections=mp_face_mesh.FACEMESH_TESSELATION,
					landmark_drawing_spec=None,
					connection_drawing_spec=mp_drawing_styles
					.get_default_face_mesh_tesselation_style())
			mp_drawing.draw_landmarks(
					image=image,
					landmark_list=face_landmarks,
					connections=mp_face_mesh.FACEMESH_CONTOURS,
					landmark_drawing_spec=None,
					connection_drawing_spec=mp_drawing_styles
					.get_default_face_mesh_contours_style())
			mp_drawing.draw_landmarks(
					image=image,
					landmark_list=face_landmarks,
					connections=mp_face_mesh.FACEMESH_IRISES,
					landmark_drawing_spec=None,
					connection_drawing_spec=mp_drawing_styles
					.get_default_face_mesh_iris_connections_style())

		image = cv2.flip(image, 1)
		# get boundary of this text
		textsize = cv2.getTextSize(text, font, fontScale, thickness)[0]

		# get coords based on boundary
		textX = (image.shape[1] - textsize[0]) // 2
		textY = 900

		image = cv2.putText(image, text, (textX, textY), font, 
							fontScale, color, thickness, cv2.LINE_AA)
	else:
		image = cv2.flip(image, 1)
		text = "No Face Detected"
		textsize = cv2.getTextSize(text, font, fontScale, thickness)[0]

		# get coords based on boundary
		textX = (image.shape[1] - textsize[0]) // 2
		textY = 900

		image = cv2.putText(image, text, (textX, textY), font, 
							fontScale, color, thickness, cv2.LINE_AA)
	
	return image

if __name__ == "__main__":
	stored_keys = {}

	mp_drawing = mp.solutions.drawing_utils
	mp_drawing_styles = mp.solutions.drawing_styles
	mp_face_mesh = mp.solutions.face_mesh

	# For webcam input:
	cap = cv2.VideoCapture(0)
	with mp_face_mesh.FaceMesh(
			max_num_faces=1,
			refine_landmarks=True,
			min_detection_confidence=0.5,
			min_tracking_confidence=0.5) as face_mesh:
		while cap.isOpened():
			success, image = cap.read()
			if not success:
				print("Ignoring empty camera frame.")
				# If loading a video, use 'break' instead of 'continue'.
				continue

			if cv2.waitKey(33) == ord('a'): # not really used, storing the dict of keys for face
				process_image_face_detection(face_mesh, image, stored_keys, 'a')
			else:
				image = process_image_face_detection(face_mesh, image, stored_keys)
			
			# Flip the image horizontally for a selfie-view display.
			cv2.imshow('MediaPipe Face Mesh', image)
			if cv2.waitKey(5) & 0xFF == 27:
				break
	cap.release()