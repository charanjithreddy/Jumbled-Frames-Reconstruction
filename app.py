from video_to_frames import video_to_frames
from ordering_frames import main as order_frames_main
from reconstruct_video import reconstruct_video_main

video_path = "C:\\Users\\lenovo\\OneDrive\\Desktop\\JUMBLED FRAMES RECONSTRUCTION\\jumbled_video.mp4"
output_directory = "extracted_frames"
print("Start: Conversion of given jumbled video into frames");
video_to_frames().convert_video_to_frames(video_path,output_directory)
print("End: Converted given jumbled video into frames");
print();

print("Start: Ordering of the jumbled frames");
order_frames_main()
print("End: Ordered the jumbled frames")
print()
print("Start: Assemlung the ordered frames back to video")
reconstruct_video_main()
print("End: Original video retrieved");