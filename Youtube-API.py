#!/usr/bin/python3
from googleapiclient.discovery import build
import os
import subprocess


def api_call():
    try:
        expanded_path = os.path.expandvars('$HOME/.bashrc')
        
        temp_api = subprocess.run(
            ['bash', '-c', f'source {expanded_path} && echo $YOUTUBE_API_KEY'],
            capture_output=True,
            text=True
        )
        api_key = temp_api.stdout.strip()

        if api_key:
            print("API key set from bashrc\n")

        if api_key == "":
            api_key_temp = "/home/src/Scripts-For-Dev-Env/temp-holder.txt"
            print("No API key found, setting temporary placeholder.")

            input_user = input("\nCopy and paste your Youtube API key\n ")

            subprocess.run([f"echo {input_user} > {api_key_temp}"], shell=True, check=True)
            user_api_key = subprocess.check_output(["cat", api_key_temp], text=True).strip()

            channel_api_key = user_api_key
            youtube = build('youtube', 'v3', developerKey=channel_api_key)

        channel_id = subprocess.run(
            ['bash', '-c', f'source {expanded_path} && echo $YOUTUBE_CHANNEL_ID'],
            capture_output=True,
            text=True
        )
        yt_id = channel_id.stdout.strip()

        if yt_id:
            print("API key set from bashrc\n")

        if yt_id == "":
            chan_id_temp = f"/home/src/Scripts-For-Dev-Env/temp-id-holder.txt"
            print("\nNo channel key found, setting temporary placeholder.")

            input_user = input("\nCopy and paste your Youtube channel id\n ")

            subprocess.run([f"echo {input_user} > {chan_id_temp}"], shell=True, check=True)
            user_id = subprocess.check_output(["cat", chan_id_temp], text=True).strip()

            channel_id_key = user_id
            channel_id = channel_id_key

        response = youtube.channels().list(
            part='statistics',
            id=channel_id

        ).execute()

        stats = response['items'][0]['statistics']

        subscriber_count = stats.get('subscriberCount', 'Unknown')
        video_count = stats.get('videoCount', 'Unknown')
        view_count = stats.get('viewCount', 'Unknown')

        print("Subscribers:", int(subscriber_count))
        print("Videos on channel:", int(video_count))
        print("Total Views:", int(view_count))

        temp = "/home/src/Scripts-For-Dev-Env/temp-holder.txt"
        tempfile = "/home/src/Scripts-For-Dev-Env/temp-id-holder.txt"
        
        if len(str(temp)) > 0:
            with open(temp, 'w') as f:
                f.write('')

        if len(str(tempfile)) > 0:
            with open(tempfile, 'w') as f:
                f.write('')

    except IndexError:
        pass


if __name__ == '__main__':
    api_call()
    
    
