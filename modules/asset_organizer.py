import os
import shutil

class AssetOrganizer:
    def __init__(self, base_dir: str = "D:/MR/Mojart_Production_System"):
        self.base_dir = base_dir
        self.project_structure = {
            "raw_assets": os.path.join(base_dir, "assets"),
            "video_tracks": os.path.join(base_dir, "production/video"),
            "audio_tracks": os.path.join(base_dir, "production/audio"),
            "exports": os.path.join(base_dir, "production/exports")
        }
        self._init_structure()

    def _init_structure(self):
        for path in self.project_structure.values():
            if not os.path.exists(path):
                os.makedirs(path)

    def organize_downloaded_assets(self) -> int:
        moved_count = 0
        raw_dir = self.project_structure["raw_assets"]
        target_video_dir = self.project_structure["video_tracks"]

        if not os.path.exists(raw_dir):
            return 0

        for root, dirs, files in os.walk(raw_dir):
            for file in files:
                if file.endswith(".mp4"):
                    src_file = os.path.join(root, file)
                    dest_file = os.path.join(target_video_dir, file)
                    
                    if os.path.getsize(src_file) > 0:
                        if not os.path.exists(dest_file):
                            shutil.copy2(src_file, dest_file)
                            print(f"[ORGANIZER] Linked: {file} -> production/video/")
                            moved_count += 1
        return moved_count