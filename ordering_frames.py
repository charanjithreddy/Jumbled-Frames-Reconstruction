import os
import cv2
import numpy as np
from itertools import permutations
import time
from concurrent.futures import ProcessPoolExecutor
from skimage.metrics import structural_similarity as ssim

# Input and output folders
FRAME_FOLDER = "extracted_frames"  # folder containing input frames
OUTPUT_FOLDER = "reconstructed_frames"  # folder to save ordered frames

# Ensure output folder exists
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def load_frames():
    """Load all frames from the folder"""
    if not os.path.exists(FRAME_FOLDER):
        raise FileNotFoundError(f"Folder '{FRAME_FOLDER}' not found!")
    files = sorted([f for f in os.listdir(FRAME_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg'))])
    frames = [cv2.imread(os.path.join(FRAME_FOLDER, f)) for f in files]
    return frames, files

def frame_difference(f1, f2):
    """Compute perceptual difference between two frames using SSIM"""
    # Convert to grayscale
    f1_gray = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
    f2_gray = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)
    
    # Resize to smaller dimensions for speed (optional)
    f1_small = cv2.resize(f1_gray, (64, 64))
    f2_small = cv2.resize(f2_gray, (64, 64))
    
    # Compute SSIM (1 = identical, 0 = very different)
    score, _ = ssim(f1_small, f2_small, full=True)
    
    # Return difference (smaller = more similar)
    return 1 - score

def compute_score_for_perm(args):
    """Wrapper for parallel execution (args = (perm, frames))"""
    perm, frames = args
    return sum(frame_difference(frames[perm[i]], frames[perm[i+1]]) for i in range(len(perm)-1))

def order_frames_greedy(frames):
    """Order frames using greedy nearest-neighbor approach"""
    start_time = time.time()
    n = len(frames)
    if n <= 1:
        return frames

    remaining = list(range(n))
    ordered = [remaining.pop(0)]  # start with first frame
    cnt=1;
    while remaining:
        last = ordered[-1]
        # find frame with minimum difference from last
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

    """Save the frames in order into the output folder"""
    for idx, frame in enumerate(ordered_frames):
        # Keep original extension
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
