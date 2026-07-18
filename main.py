import os
from modules.blueprint_parser import parse_blueprint
from modules.asset_collector import AssetCollector
from modules.asset_downloader import AssetDownloader
from modules.asset_organizer import AssetOrganizer
from modules.audio_processor import AudioProcessor
from modules.sequence_builder import SequenceBuilder

# 1. تحديد مسار المجلد الحالي ديناميكياً ليعمل على أي جهاز
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 2. حماية مفتاح الـ API عبر قراءته من بيئة التشغيل مع الاحتفاظ بـ الـ Key الحالي كبديل محلي لحمايته من الحظر
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "Xlddd6zhVaf9a8vTOSB33LxRgrgbsZzVAOWfjdJZyy0lSpd8sJETuBso")

def main():
    try:
        # 3. تعديل مسار الـ Blueprint ليعتمد على المسار الديناميكي
        blueprint_path = os.path.join(PROJECT_ROOT, "blueprints", "sample_blueprint.json")
        blueprint = parse_blueprint(blueprint_path)
        print("[SUCCESS] Blueprint file read and parsed successfully!")
        
        target_dimension = blueprint.ata.ty
        
        # 2. Initialize System Modules
        collector = AssetCollector(pexels_api_key=PEXELS_API_KEY)
        downloader = AssetDownloader(output_dir="assets")
        
        # 4. استبدال المسار الثابت "D:/MR/..." بالمتغير الديناميكي PROJECT_ROOT
        organizer = AssetOrganizer(base_dir=PROJECT_ROOT)
        audio_proc = AudioProcessor(base_dir=PROJECT_ROOT)
        seq_builder = SequenceBuilder(base_dir=PROJECT_ROOT)
        
        # 3. Extract search queries
        queries = collector.collect_queries(blueprint)
        print(f"[INFO] Extracted Queries: {queries}")
        
        # 4. Search, Evaluate, and Download assets
        print("\n[START] Beginning automated asset evaluation and download process...")
        for query in queries:
            print(f"\n--- Processing Query: [{query}] ---")
            search_results = collector.search_videos(query, per_page=2)
            
            if not search_results:
                print(f"[WARNING] No results found for query: {query}")
                continue
                
            for video_data in search_results:
                video_id = video_data.get("id")
                video_files = video_data.get("files", [])
                
                best_link = downloader.evaluate_and_filter_sources(video_files, target_type=target_dimension)
                
                if best_link:
                    file_name = f"{query}_{video_id}.mp4"
                    downloader.download_file(url=best_link, folder_name=query, file_name=file_name)
                else:
                    print(f"[SKIP] Video {video_id}: Does not match requirements.")

        # 5. Execute Auto-Organization Session
        print("\n[START] Beginning asset organization and pipeline linking...")
        organizer.organize_downloaded_assets()

        # 6. Execute Audio Processing Session
        print("\n[START] Beginning audio asset verification...")
        audio_report = audio_proc.verify_blueprint_audio(blueprint)
        print(f"[STATUS] Audio System: {audio_report['status']}")

        # 7. Execute Sequence Assembly and Rendering Session
        bgm_path = audio_report["bgm_file"] if audio_report["has_bgm"] else ""
        print("\n[START] Beginning asset sequence assembly...")
        final_output = seq_builder.build_sequence(output_filename="mojart_final_video.mp4", audio_track_path=bgm_path)
        
        if final_output:
            print(f"\n[FINISHED] Pipeline processed everything successfully! Master file created.")
        else:
            print(f"\n[FATAL] Pipeline stopped at sequence rendering stage.")

    except Exception as e:
        print(f"[ERROR] An error occurred during execution: {e}")

if __name__ == "__main__":
    main()