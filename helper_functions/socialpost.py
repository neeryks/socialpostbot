import requests
from savedfile  import graph_api
class InstaPost:
    
    def upload_media(self, media, caption,id):
        url = f'https://graph.facebook.com/v17.0/{id}/media'
        payload = {'video_url': media,'media_type':'REELS', 'caption': caption, 'access_token': graph_api()}
        r = requests.post(url, data=payload)
        print(r.text)
        return r.json()['id']
        
    def publish(self, container_id,id):
        url = f'https://graph.facebook.com/v17.0/medias_publish?creation_id={container_id}&access_token={graph_api()}'
        payload = {'access_token': graph_api()}
        r = requests.post(url, data=payload)
        print(r.text)
        return r.json()['id']