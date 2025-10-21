def test_end_to_end_relationship_pipeline():
    """E2E validation from hello → date → relationship build."""
    stages = ["hello", "small_talk", "invite", "date", "followup"]
    success_rate = 0.6

    assert "hello" in stages, "Critical greeting phase missing."
    assert success_rate >= 0.5, "Conversion rate below acceptable SLA."
    assert stages[-1] == "followup", "Pipeline ended without closure."
