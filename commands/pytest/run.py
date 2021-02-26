from web.settings import BASE_DIR
from pytest import main as test, ExitCode


def all_tests():
    test_status = test([BASE_DIR])
    if test_status and not test_status == ExitCode.NO_TESTS_COLLECTED:
        return False
    return True
