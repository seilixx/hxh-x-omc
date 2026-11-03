# Character Images Directory

You can place local character portraits here to replace or override external images.

## Directory Structure:
- `hunter-x-hunter/` : e.g., `gon-freecss.png`, `killua-zoldyck.png`
- `naruto/`          : e.g., `naruto-uzumaki.png`, `sasuke-uchiha.png`
- `jujutsu-kaisen/`  : e.g., `yuji-itadori.png`, `satoru-gojo.png`
- `one-piece/`       : e.g., `monkey-d-luffy.png`, `roronoa-zoro.png`

## How it works:
1. Place the character portrait image (.png, .jpg, .webp) in the corresponding anime folder.
2. Update the `image` field in `src/data/<anime>/characters.ts` to `/assets/characters/<anime>/<filename>.png`.
3. If an image is not found or fails to load, the game automatically uses the dynamic Hunter Association Silhouette Avatar with character metadata!
