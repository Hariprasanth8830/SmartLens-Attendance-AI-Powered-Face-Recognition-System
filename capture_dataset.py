import cv2
import os

def capture_images(name, register_number, enroll_number, num_images=10):
    # Combine strings to create folder name
    # e.g. John_23UIT040_230242
    student_name = f"{name}_{register_number}_{enroll_number}"
    
    # Ensure the dataset folder and the student's subfolder exist
    dataset_path = os.path.join("dataset", student_name)
    os.makedirs(dataset_path, exist_ok=True)
    
    # Open the webcam
    cap = cv2.VideoCapture(0)
    print(f"\n[INFO] Starting capture for '{student_name}'...")
    print("[INFO] Press 's' to save an image, 'q' to quit early.")
    print(f"[INFO] Need {num_images} images total.\n")
    
    count = 0
    while count < num_images:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Is your webcam connected?")
            break
            
        # Display the live feed
        cv2.imshow("Capture Faces (Press 's' to save, 'q' to quit)", frame)
        
        # Wait for key press
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            # Save the image when 's' is pressed
            img_path = os.path.join(dataset_path, f"{student_name}_{count+1}.jpg")
            cv2.imwrite(img_path, frame)
            count += 1
            print(f"✅ Captured {count}/{num_images} images.")
        elif key == ord('q'):
            print("Quitting early...")
            break
            
    cap.release()
    cv2.destroyAllWindows()
    print(f"\n🎉 Finished capturing {count} images for {student_name}.")
    print("You can now go to the dashboard and click 'Model Training'!")

if __name__ == "__main__":
    print("=== Dataset Capture Helper ===")
    name = input("Enter the student's name: ").strip()
    register_number = input("Enter the student's register number (e.g. 23UIT040): ").strip()
    enroll_number = input("Enter the student's enroll number (e.g. 230242): ").strip()
    
    if name and register_number and enroll_number:
        capture_images(name, register_number, enroll_number)
    else:
        print("Name, Register Number, and Enroll Number cannot be empty.")
