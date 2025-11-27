from googleapiclient.discovery import build

api_key = 'PASTE_YOUR_API_KEY_HERE'

youtube = build('youtube', 'v3', developerKey=api_key)
channel_id = 'PASTE_YOUR_CHANNEL_ID_HERE'

response = youtube.channels().list(
    part='statistics',
    id=channel_id

).execute()

stats = response['items'][0]['statistics']

subscriber_count = stats.get('subscriberCount', 'Unknown')
video_count = stats.get('videoCount', 'Unknown')
view_count = stats.get('viewCount', 'Unknown')


print("Subscribers:",int(subscriber_count))
print("Videos on channel:",int(video_count))
print("Total Views:",int(view_count))





