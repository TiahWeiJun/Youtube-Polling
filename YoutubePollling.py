from json.decoder import JSONDecodeError
import requests, json
import time
from plyer import notification
from decouple import config

def look_for_new_vdeo(channel_id):
    
    base_video_url = "https://youtube.com/watch?v="

    #url for api call
    url = "https://www.googleapis.com/youtube/v3/search?key={}&channelId={}&part=snippet,id&order=date&maxResults=1".format(config("API_KEY"),channel_id)
    raw_response = requests.get(url)

    response = raw_response.json()

    # Get the latest video id
    vidID = response['items'][0]['id']['videoId']

    
    new_video = False
    with open('videoid.json', 'r') as json_file:
        try:
            data = json.load(json_file)
            #Check if the received video id is the same as before
            if (data['videoId'] != vidID):
                new_video = True
        except JSONDecodeError:
            new_video = True
        
    #If there is a new video
    if new_video:
        with open('videoid.json', 'w') as json_file:
            data = {"videoId": vidID}
            json.dump(data, json_file)

        newVidUrl = base_video_url + vidID
        notification.notify(
        title="You have a new video to watch!",
        message = newVidUrl,
        timeout = 5
        )

#Polling every 60 seconds
while True:
    channel_id = "UCWr0mx597DnSGLFk1WfvSkQ"
    look_for_new_vdeo(channel_id)
    time.sleep(60)



