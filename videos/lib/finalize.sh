#!/usr/bin/env bash
# Resample every episode's audio to 48 kHz (video copied) and join them into the full video.
set -e
cd "$(dirname "$0")/.."
mkdir -p completo
list=completo/lista.txt; : > "$list"
for f in ep1-como-vuela/renders/ep1-como-vuela-un-avion.mp4 \
         ep2-por-dentro-y-por-fuera/renders/ep2-el-avion-por-dentro-y-por-fuera.mp4 \
         ep3-sistemas/renders/ep3-los-sistemas-del-avion.mp4 \
         ep4-oxigeno-comunicaciones/renders/ep4-oxigeno-comunicaciones-y-cajas-negras.mp4 \
         ep5-instrumentos-navegacion/renders/ep5-instrumentos-y-navegacion.mp4 \
         ep6-meteorologia/renders/ep6-meteorologia-para-volar.mp4 \
         ep7-cabina-tcp/renders/ep7-la-cabina-y-el-tcp.mp4; do
  sr=$(ffprobe -v error -select_streams a -show_entries stream=sample_rate -of csv=p=0 "$f")
  if [ "$sr" != "48000" ]; then
    ffmpeg -v error -y -i "$f" -c:v copy -c:a aac -b:a 192k -ar 48000 "${f%.mp4}.tmp.mp4" && mv "${f%.mp4}.tmp.mp4" "$f"
  fi
  echo "file '$(pwd)/$f'" >> "$list"
done
ffmpeg -v error -y -f concat -safe 0 -i "$list" -c copy -movflags +faststart completo/conocimiento-del-avion-completo.mp4
rm -f "$list"
ffprobe -v error -show_entries format=duration,size -of csv=p=0 completo/conocimiento-del-avion-completo.mp4
