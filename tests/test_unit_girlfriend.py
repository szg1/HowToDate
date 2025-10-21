import pytest
from datetime import timedelta

# Mock user state
class User:
    def __init__(self):
        self.showered = False
        self.confidence = 0
        self.eye_contact = 0
        self.conversations = 0
        self.invites = 0
        self.rejections = 0

@pytest.fixture
def user():
    return User()

def test_hygiene_pipeline(user):
    """Ensure user meets baseline cleanliness spec."""
    user.showered = True
    assert user.showered, "User failed basic deployment: hygiene check."

def test_confidence_bootstrap(user):
    """Confidence should increment after one successful conversation."""
    user.confidence += 1
    assert user.confidence > 0, "Confidence initialization failed."

def test_eye_contact_bounds(user):
    """Validate human eye contact duration compliance."""
    user.eye_contact = 2.5
    assert 1.5 <= user.eye_contact <= 3.5, "Eye contact out of spec, fix gaze calibration."

def test_conversation_increment(user):
    """Conversations should increase counter and not throw exceptions."""
    user.conversations += 1
    assert user.conversations == 1, "Conversation counter desynchronized."

def test_invite_logic(user):
    """User should not invite before confidence threshold."""
    user.confidence = 1
    if user.confidence > 0:
        user.invites += 1
    assert user.invites == 1, "Invite logic failed to trigger."
