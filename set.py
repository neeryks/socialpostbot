from moviepy.video.fx.all import crop
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import AudioFileClip
from moviepy.editor import TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
from quotegetter import Quote_Getter, Sql_Query

class Video_Editor(Quote_Getter):
    def __init__(self):
        pass
        
    def video_edit(self,video_file,width,height):
        video_clip = VideoFileClip(f"{video_file}")
        width, height = video_clip.size
        video_clip = crop(video_clip, x_center=width/2, y_center=height/2, width=width, height=height)
        return video_clip

    def audio_edit(self,audio_file):
        audio_clip = AudioFileClip(f"{audio_file}")
        return audio_clip

    def merging_clip(self):
        video_clip = self.video_edit()
        audio_clip = self.audio_edit()
        video_clip = video_clip.set_audio(audio_clip)
        final_video = CompositeVideoClip([video_clip, self.caption("Hello World")])
        return final_video.write_videofile("final_video.mp4")

    def caption(self,caption,font,color,position):
        captions = TextClip(f"{caption}", fontsize=f"{font}", color=f"{color}")
        captions = captions.set_duration(self.video_edit().duration)
        captions = captions.set_position(f"{position}")
        return captions
    

