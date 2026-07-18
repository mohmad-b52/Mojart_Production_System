import os
import requests
import time
from typing import List

class AssetDownloader:
    def __init__(self, output_dir: str = "assets"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def evaluate_and_filter_sources(self, video_files: List[dict], target_type: str = "medium") -> str:
        best_link = ""
        max_width = 0

        for file_info in video_files:
            width = file_info.get("width", 0)
            height = file_info.get("height", 0)
            link = file_info.get("link", "")

            if not link:
                continue

            if target_type == "medium" and width < height:
                continue
            
            if width > max_width:
                max_width = width
                best_link = link

        return best_link

    def download_file(self, url: str, folder_name: str, file_name: str, max_retries: int = 5) -> str:
        target_folder = os.path.join(self.output_dir, folder_name)
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        file_path = os.path.join(target_folder, file_name)
        
        # --- آلية التخطي الذكية المضافة ---
        # إذا كان الملف موجوداً وحجمه أكبر من 0 بايت، نتخطى التحميل فوراً
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            print(f"[SKIP] {file_name} already exists locally. Skipping download.")
            return file_path
        # ---------------------------------

        for attempt in range(1, max_retries + 1):
            try:
                if attempt > 1:
                    print(f"\n[RETRY] Connection lost. Retrying execution (Attempt {attempt}/{max_retries}) in 3 seconds...")
                    time.sleep(3)

                print(f"[DOWNLOADING] {file_name} ...")
                response = requests.get(url, stream=True, timeout=15)
                
                if response.status_code == 200:
                    total_size = int(response.headers.get('content-length', 0))
                    downloaded = 0
                    
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=1024*1024):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                if total_size > 0:
                                    percent = int((downloaded / total_size) * 100)
                                    print(f"Progress: {percent}% ({downloaded // (1024*1024)}MB / {total_size // (1024*1024)}MB)", end='\r')
                    
                    if downloaded >= total_size:
                        print(f"\n[SUCCESS] Saved to: {file_path}")
                        return file_path
                
                print(f"\n[ERROR] Server responded with status code: {response.status_code}")
            
            except (requests.exceptions.RequestException, Exception) as e:
                print(f"\n[WARNING] Attempt {attempt} failed due to network instability.")
                
        print(f"\n[FATAL] Failed to download {file_name} after {max_retries} attempts.")
        return ""