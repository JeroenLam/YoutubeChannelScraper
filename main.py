import os
import time
from dotenv import load_dotenv
from jsonDownload import *

cur_time = time.asctime(time.localtime())

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

# read file
with open('data.txt', 'r') as myfile:
    data=myfile.read()
#os.rename('data.txt', 'backup.txt')
data = eval(data)

# Retreiving channel data
url_channel = 'https://www.googleapis.com/youtube/v3/channels?part=contentDetails%2Cstatistics&id=' + CHANNEL_ID +'&key=' + API_TOKEN
dict_channel_data = dl_json2dict(url_channel)

# Assert if the data field exists
try:
    data["general"]
except:
    data["general"] = {}
    data["general"]["time"] = []
    data["general"]["viewCount"] = []
    data["general"]["subscriberCount"] = []
    data["general"]["videoCount"] = []

# Add new data to the structure
channel_stats = dict_channel_data["items"][-1]["statistics"]
data["general"]["time"].append(cur_time)
data["general"]["viewCount"].append(channel_stats["viewCount"])
data["general"]["subscriberCount"].append(channel_stats["subscriberCount"])
data["general"]["videoCount"].append(channel_stats["videoCount"])

## Retreiving playlist id for video list
playlist_id = dict_channel_data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

# Retreiving video data
url_uploads = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=' + playlist_id + '&key=' + API_TOKEN
dict_upload_data = dl_json2dict(url_uploads)

# Find all videos
while 1:
    for video in dict_upload_data["items"]:
        vid_id = video["snippet"]["resourceId"]["videoId"]

        # Check if video is in database, if not add datastructure
        try:
            data[vid_id]
        except:
            data[vid_id] = {}
            data[vid_id]["title"] = video["snippet"]["title"]
            data[vid_id]["publishedAt"] = video["snippet"]["publishedAt"]
            data[vid_id]["time"] = []
            data[vid_id]["viewCount"] = []
            data[vid_id]["likeCount"] = []
            data[vid_id]["dislikeCount"] = []
            data[vid_id]["favoriteCount"] = []
            data[vid_id]["commentCount"] = []

        # Download statistics
        url_video_stats = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id=' + vid_id + '&key=' + API_TOKEN
        dict_vid_stats = dl_json2dict(url_video_stats)
        stats = dict_vid_stats["items"][0]["statistics"]

        # Set time and statistics
        data[vid_id]["time"].append(cur_time)
        for stat in stats:
            data[vid_id][stat].append(stats[stat])

    try:
        next_page = dict_upload_data["nextPageToken"]
    except:
        break
    url_uploads = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=' + playlist_id + '&key=' + API_TOKEN + '&pageToken=' + next_page
    dict_upload_data = dl_json2dict(url_uploads)

# Write data to file
f = open("data.txt", "wt")
f.write(str(data))
f.close()