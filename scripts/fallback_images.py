import os
import shutil

# Marvel
for i in range(1, 31):
    path = f"public/assets/characters/marvel/marvel-{i:03d}.jpg"
    if not os.path.exists(path) or os.path.getsize(path) < 1000:
        shutil.copy("public/assets/characters/marvel/marvel-001.jpg", path)
        print(f"Filled fallback for {path}")

# Football
for i in range(1, 31):
    path = f"public/assets/characters/football/fb-{i:03d}.jpg"
    if not os.path.exists(path) or os.path.getsize(path) < 1000:
        shutil.copy("public/assets/characters/football/fb-001.jpg", path)
        print(f"Filled fallback for {path}")

print("All 30 Marvel and 30 Football image files exist!")
