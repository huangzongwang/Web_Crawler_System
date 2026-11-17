
import os
import subprocess


directory="data\\material\\principle\\"
directory_out="data\\material\\principle2\\"

os.makedirs(directory_out, exist_ok=True)

contents=[os.path.join(directory, folder) for folder in os.listdir(directory) if os.path.isfile(os.path.join(directory, folder))]

for i in contents:
    file_name=os.path.basename(i).split('.')[0]
    out_name=directory_out+file_name+".mp4"
    merge_command=f'ffmpeg -y \
        -i "{i}" \
        -filter_complex " \
        split[a][b];[a]scale=720:1280,boxblur=10:5[1];[b]scale=720:-2[2];[1][2]overlay=0:(H-h)/2 \
        " -c:v libx264 -crf 18 -preset veryfast -aspect 9:16 -f mp4 \
        "{out_name}"'
    
    print(merge_command)

    subprocess.run(merge_command)