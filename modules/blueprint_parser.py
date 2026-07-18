import json
from typing import List
from dataclasses import dataclass, field

@dataclass
class CoreData:
    _segment: str = ""
    ted_duration_seconds: float = 5.0
    ty: str = "medium"

@dataclass
class chTargeting:
    _description: str = ""
    type: str = "video"
    y_queries: List[str] = field(default_factory=list)
    ck_queries: List[str] = field(default_factory=list)
    elements: List[str] = field(default_factory=list)

@dataclass
class tStrategy:
    red_sources: List[str] = field(default_factory=list)
    ck_asset_types: List[str] = field(default_factory=list)

@dataclass
class EditingGuide:
    _mood: str = ""
    pace: str = "normal"
    een_text: str = ""
    ted_effects: str = ""
    _notes: str = ""

@dataclass
class Blueprint:
    d: str
    ata: CoreData = field(default_factory=CoreData)
    _targeting: chTargeting = field(default_factory=chTargeting)
    _strategy: tStrategy = field(default_factory=tStrategy)

def parse_blueprint(file_path: str) -> Blueprint:
    with open(file_path, 'r', encoding='utf-8') as f:
        data_dict = json.load(f)
    
    # تحويل البيانات المقروءة إلى كائنات Dataclasses
    core_data = CoreData(**data_dict.get('ata', {}))
    targeting = chTargeting(**data_dict.get('_targeting', {}))
    strategy = tStrategy(**data_dict.get('_strategy', {}))
    
    return Blueprint(
        d=data_dict.get('d', ''),
        ata=core_data,
        _targeting=targeting,
        _strategy=strategy
    )