# Importing necessary libraries
import cv2
import mediapipe as mp
import time
import tkinter as tk
from tkinter import messagebox

# Initializing MediaPipe Hands and video capture
hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)

# Initializing variables
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
# A list of booleans indicating whether a "Yes" response to each question indicates extroversion
yes_means_extrovert = [True, False, True, False, True, False, True, False, False, False]
responses = []

# Set the timer duration (in seconds)
timer_duration = 2

# Function to determine response based on hand gesture
def determine_response(hand_landmarks):
    if hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_MCP].y:
        return "Yes"
    else:
        return "No"

# Main loop for reading video frames and processing hand gestures
question_index = 0
last_seen = time.time()  # Initialize the last seen time
while question_index < len(questions):
    ret, frame = cap.read()
    if not ret:
        break
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # If hand landmarks are detected
    if results.multi_hand_landmarks:
        last_seen = time.time()  # Update the last seen time
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
            gesture = determine_response(hand_landmarks)
            cv2.putText(frame, f"Answer: {gesture}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    else:
        elapsed_time = time.time() - last_seen
        remaining_time = max(0, timer_duration - int(elapsed_time))
        cv2.putText(frame, f"Submitting {gesture} in: {remaining_time}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # If no hand is detected and timer_duration seconds have passed, register the answer and move to the next question
        if gesture != "No answer" and elapsed_time >= timer_duration:
            responses.append(gesture)
            question_index += 1
            gesture = "No answer"

    # Displaying the current question
    if question_index < len(questions):
        cv2.putText(frame, questions[question_index], (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    frame = cv2.resize(frame, (1280, 720))
    cv2.imshow('Hand Tracking', frame)

    # Breaking the loop if all questions have been asked or 'q' is pressed
    if question_index == len(questions) or cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Releasing video capture and destroying windows after loop
cap.release()
cv2.destroyAllWindows()

# Counting responses and determining result
extrovert_count = sum(response == "Yes" and yes_means_extrovert[i] or response == "No" and not yes_means_extrovert[i] for i, response in enumerate(responses))
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
messagebox.showinfo("Personality Test Result", result)