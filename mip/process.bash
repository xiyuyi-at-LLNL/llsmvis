for i in `seq 0 50`
do
    convert  black.pgm channel1_$i.pgm black.pgm -combine -set colorspace sRGB channel1_green$i.png;
    convert  channel2_$i.pgm black.pgm  black.pgm -combine -set colorspace sRGB channel2_red$i.png;
    convert  black.pgm  black.pgm channel3_$i.pgm -combine -set colorspace sRGB channel3_blue$i.png;
    convert  channel2_$i.pgm channel1_$i.pgm channel3_$i.pgm -combine -set colorspace sRGB channel_combined$i.png;
done
    ffmpeg -framerate 24 -i channel1_green%d.png -c:v libx264 -profile:v high -crf 10 -pix_fmt yuv420p -threads 20 channel1_green.mp4;
    ffmpeg -framerate 24 -i channel2_red%d.png -c:v libx264 -profile:v high -crf 10 -pix_fmt yuv420p -threads 20 channel2_red.mp4;
    ffmpeg -framerate 24 -i channel3_blue%d.png -c:v libx264 -profile:v high -crf 10 -pix_fmt yuv420p -threads 20 channel3_blue.mp4;
    ffmpeg -framerate 24 -i channel_combined%d.png -c:v libx264 -profile:v high -crf 10 -pix_fmt yuv420p -threads 20 channel_combined.mp4;

