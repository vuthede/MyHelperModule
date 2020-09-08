from pytube import YouTube
import os
import json 
import pandas as pd

def download_one_video(id, save_path):
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    
    try:
        YouTube(f'http://youtube.com/watch?v={id}').streams.filter(progressive=True).first().download(save_path)
    except:
        print(f'Failed to downdload video with id :{id}')


def download_all_data(json_data_file, output="data", check_exist=True, cache="downloaded_video.csv"):
    if not os.path.isdir(output):
        os.makedirs(output)

    # Get data list
    data_list = json.load(open(json_data_file, 'rb'))["videos"]

    # Download data
    if check_exist:
        if os.path.isfile(cache):
            df = pd.read_csv(cache, header=None)
            existed_code = list(df[0])
        else:
            existed_code = []
    
    for instrument in data_list.keys():
        ids = data_list[instrument]
        for f in ids:
            code = f'{instrument}****{f}'

            if check_exist and code in existed_code:
                print(f'The instrument {instrument} with videoID=={f} existed. Ignored to download it!')
                continue

            download_one_video(f, f'./{output}/{instrument}')
            existed_code.append(code)
            df = pd.DataFrame(data={"code": existed_code})
            df.to_csv(cache, header=False)
            print(f"Donwload videoID {f} to ./{output}/{instrument}")




if __name__=="__main__":
    download_all_data(json_data_file='./MUSIC_dataset/MUSIC21_solo_videos.json')
