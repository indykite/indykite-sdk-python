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

  # Assert
  assert date == now

def test_date_to_timestamp():
  # Prepare
  date = datetime(2022, 5, 6, 11, 52, 55, 123456)

  # Act
  timestamp = date_to_timestamp(date)

  # Assert
  assert timestamp.seconds == 1651837975
  assert timestamp.nanos == 123456000
