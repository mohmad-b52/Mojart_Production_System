import os
from typing import Optional

class AudioProcessor:
    def __init__(self, base_dir: str = "D:/MR/Mojart_Production_System"):
        self.base_dir = base_dir
        self.audio_dir = os.path.join(base_dir, "production/audio")
        
        if not os.path.exists(self.audio_dir):
            os.makedirs(self.audio_dir)

    def verify_blueprint_audio(self, blueprint_data) -> dict:
        """Scan blueprint for audio configurations and check local file status"""
        audio_status = {
            "has_bgm": False,
            "bgm_file": "",
            "status": "No audio specified in blueprint"
        }

        # Check if audio or background music properties exist in blueprint data structure
        # (Assuming 'metadata' or 'audio' section maps to the layout)
        if hasattr(blueprint_data, 'metadata') and blueprint_data.metadata:
            # Placeholder check for specific background music configs inside Blueprint asset mapping
            pass
            
        print(f"[AUDIO] Scanning production directory for source assets...")
        available_files = [f for f in os.listdir(self.audio_dir) if f.endswith(('.mp3', '.wav', '.m4a'))]
        
        if available_files:
            audio_status["has_bgm"] = True
            audio_status["bgm_file"] = os.path.join(self.audio_dir, available_files[0])
            audio_status["status"] = f"Found {len(available_files)} local audio asset(s) ready for production."
            print(f"[AUDIO] Active Track Linked: {available_files[0]}")
        else:
            audio_status["status"] = "No local audio assets found in production/audio/. System will proceed with video execution only."
            print(f"[AUDIO] [WARNING] Production audio path is empty.")

        return audio_status