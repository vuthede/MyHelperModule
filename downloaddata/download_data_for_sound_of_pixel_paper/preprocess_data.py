import subprocess
import os
import cv2
import glob

def audio_resampling(input, output, ar=11025):
    prefix = os.path.dirname(output)
    if not os.path.isdir(prefix):
        os.makedirs(prefix)

    cmd = ['ffmpeg', '-i', f'{input}','-ar', f'{ar}',  f'{output}']
    subprocess.run(cmd)


def video2frames(input, output, fps=8):
   

    cap = cv2.VideoCapture(input)
    fps_ori = cap.get(cv2.CAP_PROP_FPS)
    sampling_ratio = int(fps_ori/fps)

    if sampling_ratio <=0:
        return False

    if not os.path.isdir(output):
        os.makedirs(output)
    
    i = 0
    j=0
    while True:
        ret, img = cap.read(1)

        if not ret:
            break

        if i%sampling_ratio==0:
            j +=1

            cv2.imwrite(f'{output}/{j:06d}.jpg', img)
        
        i +=1
    
    return True
        
def preprocess_all_data(indata, outdata):
    videos = glob.glob(f'{indata}/*/*.mp4')
    print(len(videos))
    for video in videos:
        print(f"Samling frame of {video} ........................")
        instrument = video.split("/")[-2]
        ok = video2frames(input=video, output=f'{outdata}/frames/{instrument}/{os.path.basename(video)}', fps=8)
        print(f"Samling audio of {video} ........................")
        if ok:
            audio_resampling(input=video, output=f'{outdata}/audio/{instrument}/{os.path.basename(video)}'.replace(".mp4",".mp3"))


if __name__=="__main__":
    preprocess_all_data("./data", outdata="./datasam")



#video2frames(input='./datatmp/acoustic.mp4', output="./datatmp/frames/acoustic.mp4")
# audio_resampling(input='./data/accordion/Accordion cover - Love story (Indila).mp4',
#                 output="audio.mp3")
