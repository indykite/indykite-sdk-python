from utils import timestamp_to_date, date_to_timestamp
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime

def test_timestamp_to_date():
  # Prepare
  now = datetime.now()
  timestamp = Timestamp()
  timestamp.FromDatetime(now)

  # Act
  date = timestamp_to_date(timestamp)
  date_none = timestamp_to_date(None)

  # Assert
  assert date == now
  assert date_none == None

def test_date_to_timestamp():
  # Prepare
  date = datetime(2022, 5, 6, 11, 52, 55, 123456)

  # Act
  timestamp = date_to_timestamp(date)
  timestamp_none = date_to_timestamp(None)

  # Assert
  assert timestamp.seconds == 1651837975
  assert timestamp.nanos == 123456000
  assert timestamp_none == None
