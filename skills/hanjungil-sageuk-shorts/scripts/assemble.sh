set -e
cd "$(dirname "$0")"
FR=24; VF="scale=1080:608:flags=lanczos,setsar=1"
# normalize audio pieces
for c in kr cn jp; do
  ffmpeg -v error -y -ss 3 -i bgm_$c.mp3 -t 12 -af "loudnorm=I=-29:TP=-3,afade=t=in:d=0.03" -ar 48000 -ac 2 bgmn_$c.wav
done
ffmpeg -v error -y -i nar_intro.mp3 -af "loudnorm=I=-15:TP=-1.5" -ar 48000 -ac 2 narn_intro.wav
ffmpeg -v error -y -i nar_outro.mp3 -af "loudnorm=I=-15:TP=-1.5" -ar 48000 -ac 2 narn_outro.wav
# intro 3.9s: montage of start images
D=1.3
for c in kr cn jp; do
  ffmpeg -v error -y -loop 1 -t $D -i start_$c.png -vf "scale=1920:-1,zoompan=z='1+0.0025*on':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x608:fps=$FR,setsar=1" -frames:v $(python3 -c "print(round($D*$FR))") -r $FR mont_$c.mp4
done
ffmpeg -v error -y -i mont_kr.mp4 -i mont_cn.mp4 -i mont_jp.mp4 -filter_complex "[0][1][2]concat=n=3:v=1:a=0" mont.mp4
ffmpeg -v error -y -loop 1 -i ov_intro.png -i mont.mp4 -i narn_intro.wav -i bgm_intro.mp3 -filter_complex \
 "[0]format=yuv420p[bg];[bg][1]overlay=0:540:shortest=1,fps=$FR,format=yuv420p[v];[3]atrim=0.5:4.4,asetpts=PTS-STARTPTS,loudnorm=I=-27,aresample=48000,afade=t=in:d=0.3[b];[2][b]amix=inputs=2:duration=longest:normalize=0,apad,atrim=0:3.9[a]" \
 -map "[v]" -map "[a]" -t 3.9 -r $FR -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -ac 2 seg0.mp4
# country cuts
for c in kr cn jp; do
  Z="$VF"
  [ $c = jp ] && Z="scale=2560:-1,zoompan=z='1+0.4*on/121':x='iw/2-iw/zoom/2':y='(ih-ih/zoom)*0.12':d=1:s=1080x608:fps=24,setsar=1"
  T=$(python3 -c "import layout;a,b=layout.CUTS['$c']['sub'];print(f'between(t,{a},{b})')")
  ffmpeg -v error -y -loop 1 -i ov_$c.png -i cut_$c.mp4 -i bgmn_$c.wav -loop 1 -i sub_$c.png -filter_complex \
   "[0]format=yuv420p[bg];[1:v]$Z[cv0];[cv0][3]overlay=0:0:enable='$T':shortest=1[cv];[bg][cv]overlay=0:540:shortest=1,fps=$FR,format=yuv420p[v];[1:a]loudnorm=I=-15:TP=-1.5,aresample=48000,afade=t=in:d=0.05[d];[d][2]amix=inputs=2:duration=first:normalize=0[a]" \
   -map "[v]" -map "[a]" -r $FR -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -ac 2 seg_$c.mp4
done
# king reversal (breaths cut)
KD=$(ffprobe -v error -show_entries format=duration -of csv=p=0 cut_king_fast.mp4)
KE=$(python3 -c "print($KD+3)")
ffmpeg -v error -y -ss 3 -i bgm_king.mp3 -t 14 -af "loudnorm=I=-24:TP=-3,afade=t=in:d=0.03" -ar 48000 -ac 2 bgmn_king.wav
ffmpeg -v error -y -loop 1 -i ov_king.png -i cut_king_fast.mp4 -i bgmn_king.wav -loop 1 -i sub_king0.png -loop 1 -i sub_king1.png -loop 1 -i sub_king2.png -filter_complex \
 "[0]format=yuv420p[bg];[1:v]$VF[k0];[k0][3]overlay=0:0:enable='between(t,0,1.17)':shortest=1[k1];[k1][4]overlay=0:0:enable='between(t,1.17,3.62)'[k2];[k2][5]overlay=0:0:enable='gte(t,3.62)'[cv];[bg][cv]overlay=0:540:shortest=1,fps=$FR,format=yuv420p[v];[1:a]loudnorm=I=-14:TP=-1.5,aresample=48000[d];[2]atrim=0:$KD[b];[d][b]amix=inputs=2:duration=first:normalize=0[a]" \
 -map "[v]" -map "[a]" -t $KD -r $FR -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -ac 2 seg_king.mp4
# outro thumbs from last frames
for c in kr cn jp; do ffmpeg -v error -y -sseof -0.3 -i cut_$c.mp4 -frames:v 1 last_$c.png; done
python3 layout.py
ffmpeg -v error -y -loop 1 -t 2.8 -i ov_outro.png -i narn_outro.wav -i bgmn_king.wav -filter_complex \
 "[0]fps=$FR,format=yuv420p,fade=t=out:st=2.5:d=0.3[v];[2]atrim=$KD:$KE,asetpts=PTS-STARTPTS,volume=-3dB[b];[1][b]amix=inputs=2:duration=longest:normalize=0,apad,atrim=0:2.8[a]" \
 -map "[v]" -map "[a]" -t 2.8 -r $FR -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -ac 2 seg9.mp4
printf "file seg0.mp4\nfile seg_kr.mp4\nfile seg_cn.mp4\nfile seg_jp.mp4\nfile seg_king.mp4\nfile seg9.mp4\n" > list.txt
ffmpeg -v error -y -f concat -safe 0 -i list.txt -c:v libx264 -crf 19 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart final_v3.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 final_v3.mp4
