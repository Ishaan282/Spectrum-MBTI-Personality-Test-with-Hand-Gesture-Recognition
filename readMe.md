# Spectrum: MBTI Personality Test with Hand Gesture Recognition

## Description
Spectrum is an innovative project that combines the Myers-Briggs Type Indicator (MBTI) personality test with advanced hand gesture recognition technology. Our system allows users to complete the MBTI assessment using simple hand gestures, making the process more engaging and accessible.


## Features
- Hand Gesture-Based Responses: Users can respond to MBTI questions by opening or closing their hands, representing 'yes' and 'no' answers respectively.
- Real-Time Gesture Recognition: Utilizes OpenCV and Mediapipe for accurate and real-time hand tracking and gesture recognition.
- Personality Trait Mapping: Maps hand gestures to MBTI responses, helping users understand their personality traits such as introversion, extroversion, and ambiversion.
- User-Friendly Interface: Developed using Tkinter for smooth and interactive user experience.

## Technologies Used
- Python
- OpenCV: For capturing and processing video frames from the camera.
- Mediapipe: For real-time hand tracking and landmark detection.
- Tkinter: For creating the graphical user interface.
- Time: For efficient timing and synchronization within the application.

## How It Works
1. **Camera Initialization**: When you run the application, it opens the camera to start capturing video frames.
2. **Question Display**: The system displays MBTI questions on the screen.
3. **Gesture Recognition**: Users respond by showing an open hand for 'yes' or a closed hand for 'no'. The system uses OpenCV and Mediapipe to recognize these gestures in real-time.
4. **Answer Submission**: If the user takes their hand out of the screen, the system remembers the last gesture and submits the answer after a predefined time limit.
5. **Result Display**: After all questions are answered, a popup using Tkinter displays the user's personality type based on their responses.

## Team
- [Ishaan Singla](https://github.com/Ishaan1106)
- [Samiksha Singh](https://github.com/SamikshaSingh25)
- [Sameer Chandra](https://github.com/MajesterSmith)
- [Sanjal](https://github.com/SanjalJain)

## Installation
- Clone the repository
- Navigate to the project folder
- run `main.py`

## Usage
- Run the main application: python main.py
- The assesment question will be visible on your screen.
- Open your hand for 'yes' and close your hand for 'no' to answer the questions.
- to submit the response just take your hand out from camera and it will submit the answer.
- at the end View your personality assessment results upon completion.

# requirement 
- python 3.x
- openCV
- Tkinter
- Time