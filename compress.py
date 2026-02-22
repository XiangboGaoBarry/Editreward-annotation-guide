import os
import subprocess
from pathlib import Path
import shutil

video_dir = Path("assets/videos")
temp_dir = Path("assets/videos_temp")
temp_dir.mkdir(exist_ok=True)

success = True
for vid in video_dir.glob("*.mp4"):
    out_path = temp_dir / vid.name
    cmd = [
        "ffmpeg", "-y", "-i", str(vid),
        "-vf", "scale=-2:720",
        "-c:v", "libx264", "-crf", "28", "-preset", "faster",
        "-c:a", "aac", "-b:a", "128k",
        str(out_path)
    ]
    print(f"Compressing {vid.name}...")
    res = subprocess.run(cmd, capture_output=True)
    if res.returncode != 0:
        print(f"Error compressing {vid.name}: \n{res.stderr.decode('utf-8')}")
        success = False

if success:
    print("Replacing original videos...")
    for vid in temp_dir.glob("*.mp4"):
        shutil.move(str(vid), str(video_dir / vid.name))
    temp_dir.rmdir()
    
    # Calculate new total size
    total_size = sum(f.stat().st_size for f in video_dir.glob("*.mp4"))
    print(f"Compression complete! New total size: {total_size / (1024*1024):.2f} MB")
else:
    print("Compression failed for some videos. Check logs.")
