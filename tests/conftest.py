import pytest


@pytest.fixture
def w3_access_log_content(access_log_file):
    with open(access_log_file, 'r', encoding="utf-8") as f:
        content = f.read()
    return content


@pytest.fixture
def access_log_file(cwd):
    return cwd + '/files/w3_access.log'


@pytest.fixture
def w3_access_log_lines(w3_access_log_content):
    return w3_access_log_content.split('\n')


@pytest.fixture
def project_working_dir(cwd):
    return cwd + "/.."


@pytest.fixture
def pwd(project_working_dir):
    return project_working_dir


@pytest.fixture
def cwd():
    from os.path import dirname, realpath
    cwd = dirname(realpath(__file__))
    return cwd
