
def test_pages_deployment_gate_demo():
    """
    Intentionally fail CI to verify that GitHub
    Pages deployment is skipped when tests fail.
    """

    assert False, (
        "Intentional CI failure: "
        "GitHub Pages deployment must be skipped."
    )
