# 🧠 Algorithm Explanation

## 🎯 Overview
The goal of this project is to reconstruct a video from a set of **jumbled frames**.  
The main challenge is to restore the correct frame order **without timestamps or metadata**.  
To achieve this, the project uses **image similarity metrics** and a **greedy nearest-neighbor algorithm** that arranges frames based on visual continuity.

---

## ⚙️ Techniques and Algorithms Used

### 1. Frame Similarity Measurement
Each frame is compared with others using the **Structural Similarity Index (SSIM)** from `scikit-image`.

- **SSIM** measures perceptual similarity based on luminance, contrast, and structural patterns.  
- It outputs a score between `0` and `1`, where:
  - `1` → frames are nearly identical  
  - `0` → frames are very different  

To represent dissimilarity, the project defines:

D(f₁, f₂) = 1 - SSIM(f₁, f₂)


Lower `D` values indicate frames that are likely consecutive in the video.

---

### 2. Frame Ordering Algorithm
To reconstruct the sequence, a **Greedy Nearest-Neighbor Algorithm** is implemented:

1. Pick an arbitrary starting frame.  
2. Find the frame with **minimum distance (highest SSIM)** to the current frame.  
3. Append it to the reconstructed sequence.  
4. Repeat until all frames are ordered.

This produces an efficient near-optimal sequence without brute-force computation.

---

### 3. Optimization Techniques
- **Downscaled frames (64×64)** for faster processing while preserving structural patterns.  
- **Grayscale conversion** to simplify similarity calculation.  
- **Optional parallelism** using `concurrent.futures` for faster SSIM computation on large frame sets.  
- **Greedy ordering** reduces time complexity from `O(n!)` (brute force) to `O(n²)`.

---

## 🧩 Design Considerations

| Aspect | Decision | Reasoning |
|--------|-----------|-----------|
| **Similarity Metric** | SSIM | Better aligns with human visual perception. |
| **Algorithm Type** | Greedy Nearest-Neighbor | Efficient frame ordering with good accuracy. |
| **Time Complexity** | O(n²) | Each frame compared once with every other frame. |
| **Parallelism** | Optional multiprocessing | Utilizes multi-core systems efficiently. |
| **Trade-off** | Accuracy vs. Speed | Balances precision with computational efficiency. |

---

## 💡 Why This Approach
- **Interpretability:** SSIM provides intuitive results consistent with visual continuity.  
- **Efficiency:** Greedy approach scales well for hundreds of frames.  
- **Flexibility:** Can be extended with advanced feature extractors (ORB/SIFT) or ML models for higher accuracy.

