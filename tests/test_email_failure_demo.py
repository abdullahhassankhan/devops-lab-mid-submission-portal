
def test_email_failure_reporting():
    """
    Intentionally fail CI to verify that
    an automatic FAILED email is delivered.
    """

    assert False, (
        "Intentional CI failure: "
        "Automatic failure email reporting test."
    )
