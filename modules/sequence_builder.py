import os
from typing import List
from moviepy import VideoFileClip, concatenate_videoclips, AudioFileClip

class SequenceBuilder:
    def __init__(self, base_dir: str = "D:/MR/Mojart_Production_System"):
        self.base_dir = base_dir
        self.video_dir = os.path.join(base_dir, "production/video")
        self.export_dir = os.path.join(base_dir, "production/exports")
        
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def build_sequence(self, output_filename: str = "final_output.mp4", audio_track_path: str = "") -> str:
        print("\n[SEQUENCE] Initializing video sequence compilation...")
        
        if not os.path.exists(self.video_dir):
            print("[SEQUENCE] [ERROR] Production video directory does not exist.")
            return ""
            
        video_files = [os.path.join(self.video_dir, f) for f in os.listdir(self.video_dir) if f.endswith(".mp4")]
        
        if not video_files:
            print("[SEQUENCE] [ERROR] No video assets found in production/video/ to assemble.")
            return ""
            
        print(f"[SEQUENCE] Found {len(video_files)} video segment(s) for compilation.")
        
        clips: List[VideoFileClip] = []
        try:
            for path in video_files:
                print(f"[SEQUENCE] Loading clip: {os.path.basename(path)}")
                clip = VideoFileClip(path)
                
                # تعديل الدالة لتتوافق مع إصدار MoviePy الحديث
                if clip.duration > 5:
                    clip = clip.subclipped(0, 5)
                clips.append(clip)
            
            print("[SEQUENCE] Concatenating tracks into a single timeline...")
            final_video = concatenate_videoclips(clips, method="compose")
            
            if audio_track_path and os.path.exists(audio_track_path):
                print(f"[SEQUENCE] Linking external audio track: {os.path.basename(audio_track_path)}")
                audio_clip = AudioFileClip(audio_track_path)
                if audio_clip.duration > final_video.duration:
                    audio_clip = audio_clip.subclipped(0, final_video.duration)
                final_video = final_video.with_audio(audio_clip) # استخدام with_audio بدلاً من set_audio في الإصدار الجديد
            
            output_path = os.path.join(self.export_dir, output_filename)
            print(f"[SEQUENCE] Rendering final production master to: {output_path}")
            
            final_video.write_videofile(
                output_path,
                fps=24,
                codec="libx264",
                audio_codec="aac",
                logger=None
            )
            
            for c in clips:
                c.close()
            final_video.close()
            
            print(f"[SUCCESS] Video rendered successfully inside production/exports/!")
            return output_path
            
        except Exception as e:
            print(f"[SEQUENCE] [FATAL] Rendering pipeline collapsed: {e}")
            for c in clips:
                try: c.close()
                except: pass
            return ""