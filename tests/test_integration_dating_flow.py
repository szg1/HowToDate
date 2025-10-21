import time
import pytest

class SocialEnvironment:
    def __init__(self):
        self.active = True
        self.people_met = 0

    def start_conversation(self):
        self.people_met += 1
        return True

class DateProcess:
    def __init__(self):
        self.duration = 0
        self.phone_hidden = False
        self.success = False

    def execute(self, minutes=75):
        self.duration = minutes
        self.phone_hidden = True
        if 45 <= minutes <= 90:
            self.success = True
        return self.success

@pytest.fixture
def env():
    return SocialEnvironment()

@pytest.fixture
def date():
    return DateProcess()

def test_full_interaction_pipeline(env, date):
    """Integration test covering conversation → invite → date → review."""
    assert env.active, "Environment offline, no social exposure possible."

    # Step 1: conversation
    success = env.start_conversation()
    assert success and env.people_met > 0, "Conversation boot failed."

    # Step 2: invite
    invite_sent = True
    assert invite_sent, "Invite API call failed."

    # Step 3: date execution
    assert date.execute(75), "DateProcess did not meet timing SLAs."

def test_rejection_resilience():
    """Simulate rejection and validate emotional retry interval."""
    rejections = 3
    cooldown = timedelta(hours=6)
    assert rejections < 5, "Emotional rate limit exceeded."
    assert cooldown.total_seconds() >= 21600, "Retry delay too short."
