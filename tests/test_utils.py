from unittest import TestCase
import datetime
import random

from logis import utils


class TestDatetime(TestCase):
    """Test the datetime serialization/decoding functions"""

    def setUp(self):
        self.real_dates = [datetime.datetime(
            year=random.randint(2010, 2016),
            month=random.randint(1, 12),
            day=random.randint(1, 27),
            hour=random.randint(1, 12),
            minute=random.randint(0, 59)
        ) for _ in range(100)]

        self.true_serialized = [dict(
            year=date.year,
            month=date.month,
            day=date.day,
            hour=date.hour,
            minute=date.minute
        ) for date in self.real_dates]

    def test_encoding(self):
        encoded_list = [utils.serialize_datetime_obj(date) for date in self.real_dates]
        [self.assertDictEqual(true_dict, encoded_dict) for true_dict, encoded_dict in
         zip(self.true_serialized, encoded_list)]

    def test_decoding(self):
        decoded_list = [utils.decode_datetime_obj(date_dict) for date_dict in self.true_serialized]
        self.assertListEqual(decoded_list, self.real_dates)
