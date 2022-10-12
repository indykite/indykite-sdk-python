import pytest
import sys

from jarvis_sdk.cmdconfig import ConfigClient
from jarvis_sdk.indykite.config.v1beta1 import config_management_api_pb2 as pb2
from jarvis_sdk.model.app_space import ApplicationSpace
from tests.helpers import data


def test_get_app_space_by_id_short_id(capsys):
    app_space_id = "aaaaaaaaaaaaaaa"

    client = ConfigClient()
    assert client is not None

    response = client.get_app_space_by_id(app_space_id)
    captured = capsys.readouterr()
    print(captured)
    assert("invalid ReadApplicationSpaceRequest.Id: value length must be between 22 and 254 runes, inclusive" in captured.out)
    assert response is None


def test_get_app_space_by_id_wrong_id(capsys):
    app_space_id = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    client = ConfigClient()
    assert client is not None

    response = client.get_app_space_by_id(app_space_id)
    captured = capsys.readouterr()
    print(captured)
    assert("invalid id value was provided for id" in captured.out)
    assert response is None


def test_get_app_space_id_success(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_id = "gid:AAAAAmluZHlraURlgAABDwAAAAA"
    app_space = client.get_app_space_by_id(app_space_id)
    captured = capsys.readouterr()

    assert app_space is not None
    assert "invalid or expired access_token" not in captured.out


def test_get_app_space_by_name_wrong_name(capsys):
    app_space_name = "aaaaaaaaaaaaaaaaaaaaaaaaa"

    client = ConfigClient()
    assert client is not None

    customer_id = data.get_customer_id()

    response = client.get_app_space_by_name(customer_id, app_space_name)
    captured = capsys.readouterr()
    assert("not found" in captured.out)
    assert response is None


def test_get_app_space_by_name_short_customer(capsys):
    app_space_name = data.get_app_space_name()

    client = ConfigClient()
    assert client is not None

    customer_id = "bbbbbbbbbbbbbb"

    response = client.get_app_space_by_name(customer_id, app_space_name)
    captured = capsys.readouterr()
    assert "UniqueNameIdentifier.Location: value length must be between 22 and 254 runes" in captured.out
    assert response is None


def test_get_app_space_by_name_wrong_customer(capsys):
    app_space_name = data.get_app_space_name()

    client = ConfigClient()
    assert client is not None

    customer_id = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"

    response = client.get_app_space_by_name(customer_id, app_space_name)
    captured = capsys.readouterr()
    assert "invalid id value was provided for name.location" in captured.out
    assert response is None


def test_get_app_space_name_success(capsys):
    client = ConfigClient()
    assert client is not None

    app_space_name = data.get_app_space_name()
    customer_id = data.get_customer_id()

    app_space = client.get_app_space_by_name(customer_id, app_space_name)
    captured = capsys.readouterr()

    assert app_space is not None
    assert "invalid or expired access_token" not in captured.out
    assert isinstance(app_space, ApplicationSpace)
