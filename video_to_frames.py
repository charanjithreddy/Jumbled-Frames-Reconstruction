import os
import cv2;
class video_to_frames():
    def convert_video_to_frames(self,video_path,output_directory):
        try:
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
        except OSError:
            print("Error while creating output directory");
        cap = cv2.VideoCapture(video_path)

        frame_count = 0
        while True:
            ret, frame = cap.read()

            if not ret:
                break
            frame_filename = os.path.join(output_directory, f"frame_{frame_count:04d}.jpg")

            cv2.imwrite(frame_filename, frame)

            print(f"Frame {frame_count} saved as {frame_filename}")
            frame_count += 1

        cap.release()
        cv2.destroyAllWindows() 
        print(f"Successfully extracted {frame_count} frames to {output_directory}")