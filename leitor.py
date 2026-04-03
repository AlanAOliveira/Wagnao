import json
import base64
from datetime import datetime
from pathlib import Path
import cv2

def capture_and_save_image(json_file: str = "images.json"):
    """
    Captures an image from the webcam and stores it as a base64 blob in a JSON file.
    
    Args:
        json_file: Path to the JSON file where the image blob will be stored
    """
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    print("Press SPACE to capture, ESC to cancel")
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame")
            break
        
        # Display the frame
        cv2.imshow("Capture Image", frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == 32:  # SPACE key
            # Convert frame to JPEG bytes
            _, buffer = cv2.imencode('.jpg', frame)
            image_blob = base64.b64encode(buffer).decode('utf-8')
            # Save image to a unique file
            image_filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jpg"
            with open(image_filename, 'wb') as img_file:
                img_file.write(buffer)
            print(f"Image saved to {image_filename}")
            # Create data entry
            data = {
                "timestamp": datetime.now().isoformat(),
                "image": image_blob
            }
            
            # Load existing data or create new
            try:
                with open(json_file, 'r') as f:
                    images = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                images = []
            
            # Append new image
            images.append(data)
            
            # Save to JSON
            with open(json_file, 'w') as f:
                json.dump(images, f, indent=2)
            
            print(f"Image saved to {json_file}")
            break
        
        elif key == 27:  # ESC key
            print("Capture cancelled")
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_save_image()