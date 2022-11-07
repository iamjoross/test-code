
from random import randint
from pytest_cases import fixture


def pytest_addoption(parser):
    # If you add a breakpoint() here it'll never be hit.
    parser.addoption("--seed", action="store", default=randint(0, 100))

@fixture(scope="session")
def seed(pytestconfig):
    # This line throws an exception since seed was never added.
    return pytestconfig.getoption("seed")