```shell
sudo apt install ffmpeg

ffmpeg -i explode.mp3 -c:a libvorbis -q:a 4 explode.ogg
```