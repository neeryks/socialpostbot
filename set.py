from moviepy.video.fx.all import crop
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import AudioFileClip
from moviepy.editor import TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
from quotegetter import Quote_Getter, Sql_Query

class Video_Editor(Sql_Query):
    def __init__(self):
        super().__init__()
        
    def video_edit(self,video_file,widthtobe,heighttobe):
        video_clip = VideoFileClip(f"{video_file}")
        width, height = video_clip.size
        video_clip = crop(video_clip, x_center=width/2, y_center=height/2, width = widthtobe, height = heighttobe)
        return video_clip

    def audio_edit(self,audio_file):
        audio_clip = AudioFileClip(f"{audio_file}")
        return audio_clip

    def merging_clip(self):
        video_clip = self.video_edit("video_demo.mp4",720,1280)
        audio_clip = self.audio_edit("epic.mp3").set_duration(video_clip.duration)
        video_clip = video_clip.set_audio(audio_clip)
        final_video = CompositeVideoClip([video_clip, self.caption(self.using_quote(),50,"white",('center','center'),video_clip)])
        return final_video.write_videofile("final_video.mp4")

    def caption(self,caption,font,color,position,video_file):
        captions = TextClip(f"{caption}", fontsize=font, color=f"{color}")
        captions = captions.set_duration(video_file.duration)
        captions = captions.set_position(position).margin(left=10,right=10, opacity=0)
        return captions
    
merger = Video_Editor()
merger.merging_clip()
