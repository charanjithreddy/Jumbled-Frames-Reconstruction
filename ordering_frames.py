import os
import cv2
import numpy as np
from itertools import permutations
import time
from concurrent.futures import ProcessPoolExecutor
from skimage.metrics import structural_similarity as ssim


FRAME_FOLDER = "extracted_frames"  # folder containing input frames

OUTPUT_FOLDER = "reconstructed_frames"  # folder to save ordered frames

# creating output folder 
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def load_frames():
    #loading all frames from input folder
    if not os.path.exists(FRAME_FOLDER):
        raise FileNotFoundError(f"Folder '{FRAME_FOLDER}' not found!")
    files = sorted([f for f in os.listdir(FRAME_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg'))])
    frames = [cv2.imread(os.path.join(FRAME_FOLDER, f)) for f in files]
    return frames, files

def frame_difference(f1, f2):
    """Computing perceptual difference between two frames using SSIM"""
    # Converting to grayscale using cvtColor
    f1_gray = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
    f2_gray = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)
    
    # Resizing to smaller dimensions for speed
    f1_small = cv2.resize(f1_gray, (64, 64))
    f2_small = cv2.resize(f2_gray, (64, 64))
    
    # Compute SSIM (SSIM ranges from 1 to 0: 1->identical and 0->completely different)
    score, _ = ssim(f1_small, f2_small, full=True)
    
    # Return difference (smaller = more similar)
    return 1 - score

def order_frames_greedy(frames):
    """Ordering frames using the greedy nearest-neighbor approach"""
    start_time = time.time()
    n = len(frames)
    if n <= 1:
        return frames

    remaining = list(range(n))
    ordered = [remaining.pop(0)]  # starting with first frame
    cnt=1;
    while remaining:
        last = ordered[-1]
        # findig the frame with minimum difference from last
        next_idx = min(remaining, key=lambda i: frame_difference(frames[last], frames[i]))
        ordered.append(next_idx)
        remaining.remove(next_idx)
        print(cnt,"   ",time.time()-start_time)
        cnt+=1;

    end_time = time.time()
    print(f"Time taken (greedy, {n} frames): {end_time - start_time:.4f} seconds")
    return [frames[i] for i in ordered][::-1]

def save_ordered_frames(ordered_frames, original_files):
    #clearing the output folder
    for f in os.listdir(OUTPUT_FOLDER):
        file_path = os.path.join(OUTPUT_FOLDER, f)
        if os.path.isfile(file_path):
            os.remove(file_path)

    """Saving the frames in original order into the output folder"""
    for idx, frame in enumerate(ordered_frames):
        # Maintaining original extension
        ext = os.path.splitext(original_files[idx])[1]
        filename = os.path.join(OUTPUT_FOLDER, f"{idx+1:03d}{ext}")
        cv2.imwrite(filename, frame)
    print(f"Saved {len(ordered_frames)} ordered frames to '{OUTPUT_FOLDER}'")

def main():
    print("Loading frames...")
    frames, files = load_frames()
    print(f"{len(frames)} frames loaded.")

    print("Ordering frames...")
    ordered_frames = order_frames_greedy(frames)

    print("Saving ordered frames...")
    save_ordered_frames(ordered_frames, files)

if __name__ == "__main__":
    main()
