# English through Kazakh Legends — Reels pipeline

Templates and published videos for the Instagram Reels series
**English through Kazakh Legends · Аңыздар арқылы ағылшын тілі** (@danny_t.007).

## Layout
- `template/legends/` — cut-paper canvas animation (`index.html`, `renderAt(t)`), music/SFX generator (`audio.py`), frame renderer (`render.cjs`), snapshot tool (`snap.cjs`), fonts (Lora, Montserrat; both cover ә ғ қ ң ө ұ ү һ і).
- `docs/` — series bibles and the content plan.
- `reels/<date>-<slug>/` — published files. Served by GitHub Pages at
  `https://danreal21213023.github.io/kazakh-legends-reels/reels/<date>-<slug>/reel.mp4` so Instagram can fetch them.

## Render an episode
```
node render.cjs 0 <frames> frames            # 30 fps, 1080x1920 JPEG frames
python3 audio.py                             # mix_full.wav + mix_voicebed.wav
ffmpeg -framerate 30 -i frames/f%05d.jpg -i mix_full.wav -c:v libx264 -b:v 3800k -pix_fmt yuv420p -c:a aac -movflags +faststart reel.mp4
```
Keep published MP4s under ~20 MB.

Fonts are licensed under the SIL Open Font License.
