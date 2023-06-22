from moviepy.video.fx.all import crop
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import AudioFileClip
from moviepy.editor import TextClip, CompositeVideoClip, CompositeAudioClip
from moviepy.video.tools.subtitles import SubtitlesClip
from quotegetter import Sql_Query
import os
import boto3
from mediagetter import downloader

class Video_Editor(Sql_Query):
    def __init__(self,downloader = downloader()):
        super().__init__()
        self.downloader = downloader
        
    def video_edit(self,video_file,widthtobe,heighttobe):
        video_clip = VideoFileClip(f"{video_file}")
        width, height = video_clip.size
        if width > height:
            video_clip = crop(video_clip, x_center=width/2, y_center=height/2, width = 480, height = height)
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
        audio_clip1 = self.audio_edit("epic.mp3").set_duration(video_clip.duration).volumex(0.5)
        audio_clip2 = self.audio_edit("quote.mp3").volumex(1.0)
        final_audio = CompositeAudioClip([audio_clip1, audio_clip2])
        video_clip = video_clip.set_audio(final_audio)
        final_video = CompositeVideoClip([video_clip, self.caption(quote_audio_text,50,"white",('center','center'),video_clip)])
        return final_video.write_videofile("final_video.mp4")

    def caption(self,caption,font,color,position,video_file):
        captions = TextClip(f"{caption}", fontsize=font, color=f"{color}")
        captions = captions.set_duration(video_file.duration)
        captions = captions.set_position(position).margin(left=10,right=10, opacity=0)
        return captions
    
    def quote_audio(self,quote):
        polly_client = boto3.client('polly',region_name='us-east-1')
        output_format = 'mp3'
        voice_id = 'Matthew'
        response = polly_client.synthesize_speech(VoiceId=voice_id,OutputFormat=output_format,Text = quote,Engine='neural')
        audio_file = 'quote.mp3'
        with open(audio_file, 'wb') as file:
            file.write(response['AudioStream'].read())
            file.close()
    
merger = Video_Editor()
merger.merging_clip()

