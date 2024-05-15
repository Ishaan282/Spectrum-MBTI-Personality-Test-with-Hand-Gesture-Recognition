import cv2 #video capture
import mediapipe as mp #for handdetection
import time
import tkinter as tk 
from tkinter import messagebox

# Initializing MediaPipe Hands and video capture
hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)

#questions and responses
gesture = "No answer"
questions = ["Question 1: Do you enjoy social gatherings?", 
            "Question 2: Do you prefer spending time alone?", 
            "Question 3: Do you find it easy to talk to new people?",
            "Question 4: Do you prefer deep conversations over small talk?",
            "Question 5: Do you feel energized after spending time with others?",
            "Question 6: Do you often think deeply about things?",
            "Question 7: Do you enjoy being the center of attention?",
            "Question 8: Do you prefer listening rather than talking?",
            "Question 9: Do you like to plan activities in advance?",
            "Question 10: Do you often feel drained after social interactions?"]

yes_means_extrovert = [True, False, True, False, True, False, True, False, False, False]
responses = []

timer_duration = 3

# hand position to determine response
def determine_response(hand_landmarks):
    if hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_MCP].y:
        return "Yes" 
    else:
        return "No"


# Function to process the frame and return the results
def process_frame(frame):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return hands.process(image)

# Function to handle the case when hand landmarks are detected
def handle_landmarks(frame, hand_landmarks):
    # Draw the hand landmarks on the frame
    mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
    # Determine the gesture based on the hand landmarks
    gesture = determine_response(hand_landmarks)
    # Display the current gesture on the frame
    cv2.putText(frame, f"Answer: {gesture}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return gesture

# Function to handle the case when no hand landmarks are detected
def handle_no_landmarks(frame, gesture, last_seen):
    # Calculate the elapsed time since the last seen hand
    elapsed_time = time.time() - last_seen
    # Calculate the remaining time before the current gesture is registered as the answer
    remaining_time = max(0, timer_duration - int(elapsed_time))
    # Display the remaining time on the frame
    cv2.putText(frame, f"Submitting {gesture} in: {remaining_time}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    # If the timer has expired and there is a current gesture, return True
    if gesture != "No answer" and elapsed_time >= timer_duration:
        return True
    return False

question_index = 0
last_seen = time.time()  # if the hand is not seen submit the answer 
while question_index < len(questions):
    ret, frame = cap.read()
    if not ret: 
        break
    results = process_frame(frame)

    # If hand landmarks are detected
    if results.multi_hand_landmarks:
        last_seen = time.time()  # Update the last seen time
        for hand_landmarks in results.multi_hand_landmarks:
            gesture = handle_landmarks(frame, hand_landmarks)
    else:
        if handle_no_landmarks(frame, gesture, last_seen):
            responses.append(gesture)
            question_index += 1
            gesture = "No answer"

    # Displaying the current question
    if question_index < len(questions):
        cv2.putText(frame, questions[question_index], (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    frame = cv2.resize(frame, (1280, 720))
    cv2.imshow('Hand Tracking', frame)

    #exti condition
    if question_index == len(questions) or cv2.waitKey(1) & 0xFF == ord('q'):
        break


# turning off the camera
cap.release()
cv2.destroyAllWindows()

# Counting responses and determining result
extrovert_count = sum((response == "Yes" and yes_means_extrovert[i]) for i, response in enumerate(responses))
extrovert_count += sum((response == "No" and not yes_means_extrovert[i]) for i, response in enumerate(responses))
introvert_count = len(responses) - extrovert_count
if extrovert_count > introvert_count:
    result = "Result: Extrovert"
elif introvert_count > extrovert_count:
    result = "Result: Introvert"
else:
    result = "Result: Balanced"

# Displaying result in a message box
root = tk.Tk()
root.withdraw()  # Hide the main window
messagebox.showinfo("Personality Test Result :- ", result)