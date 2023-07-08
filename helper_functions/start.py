from moviepy.video.fx.all import crop
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import AudioFileClip
from moviepy.editor import TextClip, CompositeVideoClip, CompositeAudioClip
from moviepy.video.tools.subtitles import SubtitlesClip
from sql_queries import Sql_Query
import os
from mediagetter import downloader
import azure.cognitiveservices.speech as speechsdk
import PIL.Image
from PIL import ImageDraw, ImageFont
import savedfile

class Video_Editor(Sql_Query):
    def __init__(self,downloader = downloader()):
        super().__init__()
        self.downloader = downloader
        
    def video_edit(self,video_file,widthtobe,heighttobe):
        video_clip = VideoFileClip(f"{video_file}")
        width, height = video_clip.size
        if width > height:
            video_clip = crop(video_clip, x_center=width/2, y_center=height/2, width = 360, height = 640)
            video_clip = video_clip.resize((720,1280))
        else:
            video_clip = crop(video_clip, x_center=width/2, y_center=height/2, width = widthtobe, height = heighttobe)
        return video_clip

    def audio_edit(self,audio_file):
        audio_clip = AudioFileClip(f"{audio_file}")
        return audio_clip

    def merging_clip(self):
        try:
            os.remove("final_video.mp4")
            os.remove("quote.mp3")
        except:
            pass
        self.downloader.video_downloader(self.downloader.get_random_video())
        video_clip = self.video_edit("video_demo.mp4",720,1280)
        quote_audio_text = self.using_quote()
        self.quote_audio(quote_audio_text)
        final_audio = self.audio_edit("quote.mp3").volumex(1.0)
        video_clip = video_clip.set_duration(final_audio.duration + 2)
        video_clip = video_clip.set_audio(final_audio,)
        if video_clip.size[0] == 480:
            final_video = CompositeVideoClip([video_clip, self.caption(quote_audio_text,30,"yellow",('center','center'),video_clip)])
        else:
            final_video = CompositeVideoClip([video_clip, self.caption(quote_audio_text,100,"yellow",('center','center'),video_clip)])
        return final_video.write_videofile("final_video.mp4")

    def caption(self,caption,font,color,position,video_file):
        captions = TextClip(f"{caption}",method='caption',stroke_width= 4,font="bar.ttf", fontsize=font, color=f"{color}", size=video_file.size)
        captions = captions.set_duration(video_file.duration)
        captions = captions.set_position(position)
        return captions

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
    
    def video_maker(self,text,idofvideo):
        self.video_downloader(idofvideo)
        video_clip = self.video_edit("static_media/video_demo.mp4",720,1280)
        self.quote_audio(text)
        final_audio = self.audio_edit("saved_media/quote.mp3").volumex(1.0)
        video_clip = video_clip.set_duration(final_audio.duration + 2)
        video_clip = video_clip.set_audio(final_audio)
        final_video = CompositeVideoClip([video_clip, self.caption(text,60,"yellow",('center','center'),video_clip)])
        final_video.write_videofile("saved_media/final_video.mp4")
        return "final_video.mp4"
    
if __name__ == "__main__": 
   vid = Video_Editor()
   vid.video_maker("Hello World","16757506")

