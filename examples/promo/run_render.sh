#!/usr/bin/env bash
cd "$(dirname "$0")"
FF=$(python -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
mkdir -p out
for n in a b c main; do
  echo "== render $n"
  node render.mjs cfg_$n.json || { echo "RENDER FAILED $n"; exit 1; }
  "$FF" -y -loglevel error -framerate 30 -i frames_$n/%05d.jpg -i audio_$n.wav -c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart out/$n.mp4 || { echo "ENCODE FAILED $n"; exit 1; }
  echo "done $n"
done
echo ALLDONE
