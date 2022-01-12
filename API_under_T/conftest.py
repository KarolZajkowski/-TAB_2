import shutil
import uuid
import json, yaml
# import tasks
import random
import pytest
import schemathesis
from pathlib import Path
# from tasks import Task
from dataclasses import dataclass


@pytest.fixture(scope='session')
def get_schema():
    """:return load API schema """
    schema = schemathesis.from_path('definicjaAPI.txt')
    return schema


# @pytest.fixture(scope='session')
# def get_schema_if_swagger():
#     """ load API schema """
#     yaml_file = yaml.dump(json.load(open('definicjaAPI.txt')), default_flow_style=False)
#     # yaml_file = yaml_file.encode()
#     return yaml_file


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """:return monkeypatch request - request under control """
    monkeypatch.delattr('requests.sessions.Session.request')


@pytest.fixture
def backend(tmpdir):
    """:return temp file for check test return """
    temp_file = tmpdir.join('post.txt')
    temp_file.write('')
    return temp_file


# @pytest.fixture(scope='module')
# def project_file(tmpdir_factory):
#     my_tmpdir = tmpdir_factory.mktemp("data")
#     path = Path(my_tmpdir).parent.absolute()
#     my_tmpdir.join("global_data.txt")
#     yield my_tmpdir
#     if my_tmpdir.isfile():
#         with pytest.raises(PermissionError):
#             shutil.rmtree(path)


@pytest.fixture(scope='module')
def project_file(tmpdir_factory):
    """:return file for transport data in functions """
    my_tmpdir = tmpdir_factory.mktemp("data").join("global_data.json")
    my_tmpdir.dump('')
    return my_tmpdir


def get_random():
    return {
        "id": str(uuid.uuid4()),
        "userId": str(uuid.uuid4()),
        "typeId": str(uuid.uuid4()),
        "distributionModelId": str(uuid.uuid4()),
        "amount": str(random.randint(1, 999)),  # 1-1000
        "semester": str(random.randint(1, 4))  # 1-5
    }


@pytest.fixture(params=[get_random(), get_random(), get_random()])
def valid_data(request):
    """:return generate data for validated params """
    # return str(uuid.uuid4())
    # return {
    #     "id": str(uuid.uuid4()),
    #     "userId": str(uuid.uuid4()),
    #     "typeId": str(uuid.uuid4()),
    #     "distributionModelId": str(uuid.uuid4()),
    #     "amount": str(random.randint(1, 999)),  # 1-1000
    #     "semester": str(random.randint(1, 4))  # 1-5
    #         }
    return request.param
