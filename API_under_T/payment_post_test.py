import json
import pytest
import requests
# import schemathesis  # valid for openapi 3+
from uuid import UUID
from unittest.mock import patch, Mock, MagicMock
# from swagger_tester import swagger_test  # valid just swagger2.0

from API_under_T.api_payment import Payment, schema


@schema.parametrize()
@patch('requests.post')
def test_schema_mocked(mocked_post, case):
    mocked_post.return_value = Mock(status_code="400",
                                    json=lambda: {"message": "Parameter should be an string"})
    case = requests.post('/v1/payment')  # temp <- object mocked
    case.call_and_validate()


@pytest.fixture(params=['list', 'backend'], name='payment', scope='function')
def fixture_payment(project_file, backend, request):
    """:return class with and without - shared folder for getting resolve rest of the api task"""
    if request.param == 'list':
        payment = Payment()
    elif request.param == 'backend':
        payment = Payment(backend=project_file)
    return payment


def test_payment_initialization(payment):
    """short check for helped func"""
    assert payment


def test_schema_initialization(get_schema):
    """:return check is api schema is available """
    assert str(get_schema) == 'OpenApi30 for Payments (1.0)'


class ResponseGetMock(object):
    """:return mocked data"""

    def json(self):
        return {"data": {
            "id": "1e0b3cac-1614-4af4-8284-c03b9b29340c",
            "userId": "9165a4d8-f0c4-4f19-b70d-887345ffe03e",
            "typeId": "323b9b87-2259-4a91-8cf5-2840a752e0f3",
            "distributionModelId": "c322c68e-8880-4ec3-aae4-40e29654f297",
            "title": "Rata za studia",
            "amount": "485.00",
            "deadline": "2020-06-01",
            "academicYear": "2019/2020",
            "semester": 3,
            "createdAt": "2020-05-28 15:15:00",
            "updatedAt": "2020-05-28 15:15:00"
        }}

    def status_code(self): return 200  # type: int


@pytest.fixture()
def body_payment():
    """:return request body for POST method - reused <function> """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "userId": "9165a4d8-f0c4-4f19-b70d-887345ffe03e",
        "typeId": "8c8758ca-beb5-4f2d-ad50-ed976e6fe5c5",  # valid_uuid
        "distributionModelId": "24cf73e3-3391-4974-b2b7-95b3344f1c6c",
        "title": "Rata za studia",
        "amount": "485.00",
        "deadline": "2020-06-01",
        "academicYear": "2019/2020",
        "semester": 3
    }
    return headers, data


@pytest.fixture(params=({"code": 200, "data": {
    "id": "1e0b3cac-1614-4af4-8284-c03b9b29340c",
    "userId": "9165a4d8-f0c4-4f19-b70d-887345ffe03e",
    "typeId": "323b9b87-2259-4a91-8cf5-2840a752e0f3",
    "distributionModelId": "c322c68e-8880-4ec3-aae4-40e29654f297",
    "title": "Rata za studia",
    "amount": "485.00",
    "deadline": "2020-06-01",
    "academicYear": "2019/2020",
    "semester": 3,
    "createdAt": "2020-05-28 15:15:00",
    "updatedAt": "2020-05-28 15:15:00"
}
                         },
                        {
                            "code": "400",
                            "message": "Parameter should be an string"
                        }, {
                            "code": "500",
                            "message": "Internal server error"
                        }))
def test_post_param(request):
    """:return Parametrize POST response """
    return request.param


@patch('requests.post')
def test_mocked_post(mocked_post, test_post_param, valid_data, payment, body_payment):
    """MOCKED post data with all status code for this method"""
    headers, data = body_payment

    status_code = test_post_param['code']
    if int(status_code) == 200:
        test_post_param["data"]["userId"] = valid_data["userId"]
        mocked_data = test_post_param["data"]
    elif int(status_code) == 400:
        data["userId"] = valid_data["userId"] + "no_valid_variable"  # no valid data to uuid
        mocked_data = test_post_param["message"]
    elif int(status_code) == 500:
        data["userId"] = None
        mocked_data = test_post_param["message"]

    mocked_post.return_value = Mock(status_code=status_code, json=lambda: mocked_data)
    # response = requests.post('/v1/payment', headers, data)  # temp <- object mocked
    response = payment.payment_post('/v1/payment', headers, data)  # temp <- object mocked

    assert response.status_code
    if status_code == 200:
        assert response.json()['userId'] == valid_data["userId"]
        assert UUID(response.json()['id'], version=4)
        assert UUID(response.json()['userId'], version=4)
        assert UUID(response.json()['typeId'], version=4)
        assert UUID(response.json()['distributionModelId'], version=4)

    elif status_code == 400:
        assert response.json()['message'] == "Parameter should be an string"

    elif status_code == 500:
        assert response.json()['message'] == "Internal server error"


@pytest.fixture()
def test_200_created(project_file):
    """ Created data from POST """
    data = Payment(backend=project_file)
    json_data = data.backend.read()
    json_data = json.loads(json_data)
    assert json_data  # type: json
    assert UUID(json_data['id'], version=4)
    assert UUID(json_data['userId'], version=4)
    assert UUID(json_data['typeId'], version=4)
    assert UUID(json_data['distributionModelId'], version=4)
    # return str(json_data['id'])
    return str(json_data['id'])


@pytest.fixture(params=({
                            "code": "200",
                            "message": "Resource updated"
                        }, {
                            "code": "400",
                            "message": "Parameter should be an string"
                        }, {
                            "code": "404",
                            "message": "Resource not found"},
                        {
                            "code": "500",
                            "message": "Internal server error"}))
def test_get_param(request):
    """:return Parametrize POST response """
    return request.param


# @patch.object(requests, 'get', return_value=ResponseGetMock())
@patch('requests.post')
def test_get_id(mocked_get, project_file, test_200_created, payment, test_get_param):
    id = test_200_created
    status_code = test_get_param['code']
    mocked_data = test_get_param["message"]

    # mocked_get.return_value = Mock()
    mocked_get.return_value = Mock(status_code=status_code, json=lambda: mocked_data)
    response = payment.payment_get(f"/v1/payment/{id}")  # temp <- object mocked
    # resp = requests.post(f"/v1/payment/{id}")  # no body in this step

    assert response.status_code
    if status_code == 200:
        assert response.json()['message'] == "Resource updated"
    elif status_code == 400:
        assert response.json()['message'] == "Parameter should be an string"
    elif status_code == 404:
        assert response.json()['message'] == "Resource not found"
    elif status_code == 500:
        assert response.json()['message'] == "Internal server error"


@pytest.fixture(params=({
                            "code": "200",
                            "message": "Resource deleted"
                        }, {
                            "code": "404",
                            "message": "Resource not found"
                        }, {
                            "code": "500",
                            "message": "Internal server error"}))
def test_delete_param(request):
    """:return Parametrize POST response """
    return request.param


@patch('requests.delete')
def test_delete_id(mocked_get, project_file, test_200_created, payment, test_delete_param):
    id = test_200_created
    status_code = test_delete_param['code']
    mocked_data = test_delete_param["message"]

    # mocked_get.return_value = Mock()
    mocked_get.return_value = Mock(status_code=status_code, json=lambda: mocked_data)
    response = payment.payment_delete(f"/v1/payment/{id}")  # temp <- object mocked

    assert response.status_code
    if status_code == 200:
        assert response.json()['message'] == "Resource deleted"
    elif status_code == 404:
        assert response.json()['message'] == "Resource not found"
    elif status_code == 500:
        assert response.json()['message'] == "Internal server error"


def test_close_project_file(project_file):
    with pytest.raises(AttributeError):
        project_file.close()
    assert project_file
