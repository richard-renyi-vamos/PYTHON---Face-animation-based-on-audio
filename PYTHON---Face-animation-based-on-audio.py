import pyaudio
import numpy as np
import cv2

# Function to draw a face
def draw_face(mouth_open):
    face = np.ones((400, 400, 3), dtype="uint8") * 255

    # Draw face outline (circle)
    cv2.circle(face, (200, 200), 100, (0, 0, 0), 2)

    # Draw eyes
    cv2.circle(face, (160, 170), 15, (0, 0, 0), -1)
    cv2.circle(face, (240, 170), 15, (0, 0, 0), -1)

    # Draw mouth based on sound level
    if mouth_open:
        cv2.ellipse(face, (200, 250), (40, 20), 0, 0, 360, (0, 0, 0), -1)  # Open mouth
    else:
        cv2.ellipse(face, (200, 250), (40, 10), 0, 0, 360, (0, 0, 0), -1)  # Closed mouth

    return face

# Function to get audio input and detect volume level
def audio_callback(in_data, frame_count, time_info, status):
    global volume_level
    audio_data = np.frombuffer(in_data, dtype=np.int16)
    volume_level = np.linalg.norm(audio_data) / 1000  # Normalize volume
    return (in_data, pyaudio.paContinue)

# Audio stream setup
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024,
                stream_callback=audio_callback)

stream.start_stream()

# Main loop to animate face based on audio
try:
    while True:
        # Determine if mouth should be open based on volume level
        mouth_open = volume_level > 0.1  # Adjust threshold as needed
        
        # Draw the face
        face = draw_face(mouth_open)
        
        # Display the face
        cv2.imshow("Animated Face", face)
        
        # Break loop on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()
    cv2.destroyAllWindows()
