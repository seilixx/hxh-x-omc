import os
import shutil

# Marvel
all_marvel = [f"marvel-{i:03d}.jpg" for i in range(1, 31)]
marvel_dir = "public/assets/characters/marvel"
existing_marvel = [f for f in os.listdir(marvel_dir) if f.endswith(".jpg") and os.path.getsize(os.path.join(marvel_dir, f)) > 1000]

missing_marvel = [f for f in all_marvel if f not in existing_marvel]
print(f"Missing Marvel ({len(missing_marvel)}): {missing_marvel}")

# Football
all_fb = [f"fb-{i:03d}.jpg" for i in range(1, 31)]
fb_dir = "public/assets/characters/football"
existing_fb = [f for f in os.listdir(fb_dir) if f.endswith(".jpg") and os.path.getsize(os.path.join(fb_dir, f)) > 1000]

missing_fb = [f for f in all_fb if f not in existing_fb]
print(f"Missing Football ({len(missing_fb)}): {missing_fb}")
