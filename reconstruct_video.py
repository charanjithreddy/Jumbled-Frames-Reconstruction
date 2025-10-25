import cv2
import os

def reconstruct_video_main():
    reconstructed_folder = r"./reconstructed_frames"
    output_video = os.path.abspath("./reconstructed_video.mp4")

    # GEtting all frames from reconstructed frames i.e. in correct order
    frames = sorted(
        [os.path.join(reconstructed_folder, f) for f in os.listdir(reconstructed_folder)
         if f.lower().endswith(('.jpg', '.png'))]
    )

    if not frames:
        print("No frames found in reconstructed_frames folder!")
        return

    # Reading the first frame to get dimensions
    first_frame = cv2.imread(frames[0])
    if first_frame is None:
        print("Could not read the first frame.")
        return

    height, width, _ = first_frame.shape

    # Creating a video writer
    out = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

    # Writing all frames using the video writer
    for f in frames:
        frame = cv2.imread(f)
        if frame is not None:
            out.write(frame)

    out.release()
    print(f"🎞️ Reconstructed video saved at: {output_video}")

    # opening video in default player if it exists
    if os.path.exists(output_video):
        os.startfile(output_video)
    else:
        print("Video file not found after saving.")


if __name__ == "__main__":
    reconstruct_video_main()
