import requests
from typing import List
from .blueprint_parser import Blueprint

class AssetCollector:
    def __init__(self, pexels_api_key: str):
        self.api_key = pexels_api_key
        self.base_url = "https://api.pexels.com/videos/search"
        self.headers = {"Authorization": self.api_key}

    def collect_queries(self, blueprint: Blueprint) -> List[str]:
        """استخراج الكلمات المفتاحية من البلوبرنت"""
        return blueprint._targeting.y_queries

    def search_videos(self, query: str, per_page: int = 3) -> List[dict]:
        """البحث عن فيديوهات وإعادة قائمة بملفات المقاطع وجوداتها لتقييمها"""
        params = {"query": query, "per_page": per_page}
        try:
            response = requests.get(self.base_url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                results = []
                for video in data.get("videos", []):
                    # نرسل ملفات الفيديو كاملة (الجودة، الأبعاد، الرابط) لتقييمها لاحقاً
                    results.append({
                        "id": video.get("id"),
                        "files": video.get("video_files", [])
                    })
                return results
            else:
                print(f"فشل البحث عن {query}: رمز الحالة {response.status_code}")
                return []
        except Exception as e:
            print(f"حدث خطأ أثناء الاتصال بـ API: {e}")
            return []