from datetime import datetime
from jarvis_sdk.utils import date_to_timestamp
from jarvis_sdk.utils.message_to_value import object_to_value
from google.type.latlng_pb2 import LatLng


class ObjectTest:
    def __init__(self, field_name, field_value):
        self.field_name = field_name
        self.field_value = field_value
        setattr(self, field_name, field_value)

    def HasField(self, field_name):
        return self.field_name == field_name


class ArrayTest:
    def __init__(self, values):
        self.values = values


class FieldsObjectTest:
    def __init__(self, object):
        self.fields = object


def test_null():
    # Prepare
    test_object = ObjectTest('null_value', 'NULL')

    # Act
    value = object_to_value(test_object)

    # Assert
    assert value == 'NULL'


def test_bool():
    # Prepare
    test_object = ObjectTest('bool_value', True)

    # Act
    value = object_to_value(test_object)

    # Assert
    assert value == True


def test_integer():
    # Prepare
    test_object = ObjectTest('integer_value', 42)

    # Act
    value = object_to_value(test_object)

    # Assert
    assert value == 42


def test_unsigned_integer():
    # Prepare
    test_object = ObjectTest('unsigned_integer_value', 42)

    # Act
    value = object_to_value(test_object)

    # Assert
    assert value == 42


def test_double():
    # Prepare
    test_object = ObjectTest('double_value', 16.0)

    # Act
    value = object_to_value(test_object)

    # Assert
    assert value == 16.0


def test_time():
    # Prepare
    time = datetime.now()
    timestamp = date_to_timestamp(time)
    test_object = ObjectTest('value_time', timestamp)

    # Act
    value = object_to_value(test_object)

    # Assert
    assert value == timestamp


def test_duration():
    # Prepare
    test_object = ObjectTest('duration_value', "4s")

    # Act
    value = object_to_value(test_object)

    # Assert
    assert value == "4s"


def test_identifier():
    # Prepare
    test_object = ObjectTest('identifier_value', "163a1167-28a4-4695-920c-be0f32891ee3")

    # Act
    value = object_to_value(test_object)

    # Assert
    assert value == "163a1167-28a4-4695-920c-be0f32891ee3"


def test_string():
    # Prepare
    test_object = ObjectTest('string_value', "abcd")

    # Act
    value = object_to_value(test_object)

    # Assert
    assert value == "abcd"


def test_bytes():
    # Prepare
    test_object = ObjectTest('bytes_value', bytes([1, 2, 3, 4]))

    # Act
    value = object_to_value(test_object)

    # Assert
    assert value == bytes([1, 2, 3, 4])


def test_geo_point():
    # Prepare
    test_object = ObjectTest('geo_point_value', LatLng(latitude = 18.9219927, longitude = 49.0651119))

    # Act
    value = object_to_value(test_object)

    # Assert
    assert value.latitude == 18.9219927
    assert value.longitude == 49.0651119


def test_array():
    # Prepare
    test_object = ObjectTest(
    'array_value',
    ArrayTest([
      ObjectTest('integer_value', 89),
      ObjectTest('string_value', "sdfsdf"),
    ])
    )

    # Act
    value = object_to_value(test_object)

    # Assert
    assert value[0] == 89
    assert value[1] == "sdfsdf"


def test_map():
    # Prepare
    test_object = ObjectTest(
    'map_value',
    FieldsObjectTest({
      "first": ObjectTest('duration_value', "1s"),
      "second": ObjectTest('double_value', 15.7),
    })
    )

    # Act
    value = object_to_value(test_object)

    # Assert
    assert value['first'] == "1s"
    assert value['second'] == 15.7


def test_unknown():
    # Prepare
    test_object = ObjectTest('unknown_value', 'UNKNOWN')

    # Act
    value = object_to_value(test_object)

    # Assert
    assert value == None
