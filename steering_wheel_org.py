import cv2
import numpy as np
import pyautogui
import time

# Function to detect and track points
def detect_and_track_points(frame, prev_center_points):
    # Convert frame to HSV for better color filtering
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define color ranges (adjust based on your actual colors)
    light_rose_lower = np.array([160, 100, 100], dtype="uint8")  # Adjust these values
    light_rose_upper = np.array([180, 255, 255], dtype="uint8")  # Adjust these values
    light_green_lower = np.array([40, 100, 100], dtype="uint8")  # Adjust these values
    light_green_upper = np.array([70, 255, 255], dtype="uint8")  # Adjust these values

    # Create masks for each color
    light_rose_mask = cv2.inRange(hsv, light_rose_lower, light_rose_upper)
    light_green_mask = cv2.inRange(hsv, light_green_lower, light_green_upper)

    # Apply morphological operations (optional) for noise reduction
    light_rose_mask = cv2.erode(light_rose_mask, None, iterations=2)
    light_rose_mask = cv2.dilate(light_rose_mask, None, iterations=2)
    light_green_mask = cv2.erode(light_green_mask, None, iterations=2)
    light_green_mask = cv2.dilate(light_green_mask, None, iterations=2)

    center_points = []

    # Find contours in each mask
    light_rose_contours, _ = cv2.findContours(light_rose_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    light_green_contours, _ = cv2.findContours(light_green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Identify largest contours as potential points
    if len(light_rose_contours) > 0:
        c = max(light_rose_contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        center_points.append((x, y))

        # Draw circle on frame for visualization
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)  # Yellow circle for rose color

    if len(light_green_contours) > 0:
        c = max(light_green_contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        center_points.append((x, y))

        # Draw circle on frame for visualization
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)  # Green circle for green color

    # Handle lack of detected points in current frame (persistent tracking)
    if len(center_points) == 0:
        center_points = prev_center_points

    return center_points

# Function to calculate the angle between two points
def calculate_angle(point1, point2):
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]
    angle = np.arctan2(delta_y, delta_x) * 180 / np.pi
    return angle

def main():
    # Initialize the camera capture object
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Initialize variables for tracking
    prev_center_points = []
    key_pressed = None

    while True:
        pyautogui.keyDown('W')
        # Capture frame from the camera
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Detect and track points with persistence
        center_points = detect_and_track_points(frame.copy(), prev_center_points)  # Avoid modifying original frame

        if len(center_points) == 2:
            point1, point2 = center_points[0], center_points[1]
            current_angle = calculate_angle(point1, point2)
            print(current_angle)

            # Calculate dynamic delay based on the absolute value of the angle
            abs_angle = abs(current_angle)
            

            # Simulate holding the A and D keys based on steering angle
            if -10 <= current_angle <= 10:
                if key_pressed is not None:
                    pyautogui.keyUp(key_pressed)
                    key_pressed = None
            elif -20 <= current_angle <= -10:
                if key_pressed != 'left':
                    pyautogui.keyUp('A')
                    pyautogui.keyDown('D')
                    pyautogui.keyUp('D')
                    time.sleep(0.005)
                    
                    key_pressed = 'D'
                print("Turning Right (Small Angle)")
            elif -30 <= current_angle < -20:
                if key_pressed != 'left':
                    pyautogui.keyUp('A')
                    for i in range (2):
                        pyautogui.keyDown('D')
                    
                    
                    key_pressed = 'D'
                print("Turning Right (Medium Angle)")
            elif -50 <= current_angle < -30: 
                if key_pressed != 'left':
                    pyautogui.keyUp('A')
                    for i in range(3):
                        pyautogui.keyDown('D')
                    
                    key_pressed = 'D'
                print("Turning Right (Medium-Large Angle)")
            elif current_angle < -50:
                if key_pressed != 'left':
                    pyautogui.keyUp('A')
                    pyautogui.keyDown('D')
                    
                    key_pressed = 'D'
                print("Turning Right (Large Angle)")
            elif 10 <= current_angle <= 20:
                if key_pressed != 'right':
                    pyautogui.keyUp('D')
                    pyautogui.keyDown('A')
                    pyautogui.keyUp('A')
                    time.sleep(0.005)
                    
                    key_pressed = 'A'
                print("Turning Left (Small Angle)")

            elif 21 <= current_angle <= 30:
                if key_pressed != 'right':
                    pyautogui.keyUp('D')
                    for i in range (2):
                        pyautogui.keyDown('A')
                    
                    key_pressed = 'A'
                print("Turning Left (Medium Angle)")

            elif 31 <= current_angle <= 50:
                if key_pressed != 'right':
                    pyautogui.keyUp('D')
                    
                    for i in range(3):
                        pyautogui.keyDown('A')
                    
                    key_pressed = 'A'
                print("Turning Left (Medium-Large Angle)")

            elif current_angle > 50:
                if key_pressed != 'right':
                    pyautogui.keyUp('D')
                    pyautogui.keyDown('A')
                    
                    key_pressed = 'A'
                print("Turning Left (Large Angle)")

            prev_center_points = center_points  # Update tracked positions

        # Display frame with detected points
        cv2.imshow('Frame', frame)

        # Handle keyboard input for quitting
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
