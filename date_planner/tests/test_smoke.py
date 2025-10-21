from src.cli import pick_idea
from src.ideas import VIBES

def test_pick_idea():
    for v in VIBES:
        assert isinstance(pick_idea(v, "mid"), str)
