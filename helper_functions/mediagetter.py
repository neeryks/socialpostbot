from savedfile import pexels_api
import requests
import json
import mysql.connector
import azure.cognitiveservices.speech as speechsdk
import savedfile
import PIL.Image
from PIL import ImageDraw, ImageFont
from moviepy.editor import TextClip, CompositeVideoClip


class downloader():
    def __init__(self):
        self.my_videodb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="H.no194/3A",
        database="video_db")


    def video_downloader(self,id):
        response = requests.get(f"https://api.pexels.com/videos/videos/{id}", headers={"Authorization": pexels_api()})
        data = json.loads(response.text)["video_files"]
        for dat in data:
            if dat["width"] == 720 and dat["height"] == 1280 or dat["width"] == 1280 and dat["height"] == 720:
                link = dat["link"]
                break
            else:
                pass      
        with open("static_media/video_demo.mp4", "wb") as f:
            f.write(requests.get(link).content)
            print("Video downloaded")
            f.close()

    def create_database(self):
        return self.my_videodb.cursor().execute("CREATE DATABASE video_db")
    
    def create_table(self):
        return self.my_videodb.cursor().execute("CREATE TABLE videos (id INT AUTO_INCREMENT PRIMARY KEY, video_id VARCHAR(255) )")
    
    def create_column(self):
        return self.my_videodb.cursor().execute("ALTER TABLE videos ADD COLUMN used VARCHAR(255) DEFAULT 'No'")
    
    def insert_video(self,video_id):
        cursor = self.my_videodb.cursor()
        cursor.execute(f"INSERT INTO videos (video_id) VALUES ('{video_id}');")
        self.my_videodb.commit()
        print(cursor.rowcount, "records inserted.")

    def get_random_video(self):
        cursor = self.my_videodb.cursor()
        cursor.execute("SELECT * FROM videos ORDER BY RAND() LIMIT 1")
        myresult = cursor.fetchall()[0][1]
        return myresult
    
    def show_columns(self):
        cursor = self.my_videodb.cursor()
        cursor.execute("SHOW COLUMNS FROM videos")
        for x in cursor:
            print(x)

    def show_all_video_id(self):
        cursor = self.my_videodb.cursor()
        cursor.execute("SELECT * FROM videos")
        myresult = cursor.fetchall()
        for x in myresult:
            print(x[1])
        return myresult
    
    def delete_video_byid(self,id):
        cursor = self.my_videodb.cursor()
        cursor.execute(f"DELETE FROM videos WHERE id = {id};")
        self.my_videodb.commit()
        print(cursor.rowcount, "record(s) deleted")

    def delete_video_byvideo_id(self,video_id):
        cursor = self.my_videodb.cursor()
        cursor.execute(f"DELETE FROM videos WHERE video_id = '{video_id}';")
        self.my_videodb.commit()
        print(cursor.rowcount, "record(s) deleted")

    def quote_audio(self,text):

        speech_key = savedfile.speech_key()
        service_region = "centralindia"
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        speech_config.speech_synthesis_voice_name = "en-US-DavisNeural"
        text = f"""<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xml:lang="en-US">
                    <voice name="en-US-DavisNeural" style="friendly">
                    {text}
                    </voice>
                    </speak>"""
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        result = speech_synthesizer.speak_ssml_async(text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
        
        with open("saved_media/quote.mp3", "wb") as f:
            f.write(result.audio_data)
            f.close()
        return "quote.mp3"

    def textwarper(self,text,characters):
        text_list = text.split(" ")
        liapp = []
        addedtext = ""
        for tex in enumerate(text_list):
            if len(addedtext) <= characters:
                addedtext = addedtext +" "+ tex[1]
            else:
                liapp.append(addedtext)
                addedtext = tex[1]
        liapp.append(addedtext)   
        return liapp               

    def image_maker(self,text):

        img = PIL.Image.open("static_media/backg.png")
        dr = ImageDraw.Draw(img)
        myFont = ImageFont.truetype('static_media/bar.ttf', 220)
        list_of_text = self.textwarper(text, 35)
        height_to_start = (len(list_of_text)/2)*-200
        for te in list_of_text:
            dr.text((img.width/2, img.height/2+height_to_start), f"{te}", fill=(255,255,255), font=myFont, anchor="mm", align="center")
            height_to_start = height_to_start + 200
        img.save("saved_media/image.png")
        return "image.png"
