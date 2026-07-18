import sys
import os

# إضافة جذر المشروع لتفادي أخطاء الـ Import عند التشغيل من داخل المجلد الفرعي
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.blueprint_parser import parse_blueprint

def test_blueprint_parsing():
    print("[TEST] Running isolated Blueprint Parser check...")
    # تحديث المسار إلى المجلد الجديد المرفوع للجذر
    blueprint_path = "blueprints/sample_blueprint.json"
    
    try:
        blueprint = parse_blueprint(blueprint_path)
        print(f"[TEST SUCCESS] Form dimension type detected: {blueprint.ata.ty}")
        print(f"[TEST SUCCESS] Total script target lines: {len(blueprint.script)}")
        return True
    except Exception as e:
        print(f"[TEST FAILED] Parser crashed: {e}")
        return False

if __name__ == "__main__":
    test_blueprint_parsing()