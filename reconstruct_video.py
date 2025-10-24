import cv2
import os

reconstructed_folder = r"./reconstructed_frames"
output_video = r"./reconstructed_video.mp4"

frames = sorted(
    [os.path.join(reconstructed_folder, f) for f in os.listdir(reconstructed_folder) if f.endswith('.jpg')]
)

first_frame = cv2.imread(frames[0])
height, width, _ = first_frame.shape

out = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

for f in frames:
    frame = cv2.imread(f)
    out.write(frame)

out.release()
print(f"🎞️ Reconstructed video saved at {output_video}")
