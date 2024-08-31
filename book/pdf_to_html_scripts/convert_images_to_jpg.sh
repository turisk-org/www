
set -e
set -x

for x in `ls images/*.png`; do
  ffmpeg -i $x ${x:0:-3}jpg
done