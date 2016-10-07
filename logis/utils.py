import datetime


def serialize_datetime_obj(datetime_obj):
    retdict = dict(
        year=datetime_obj.year,
        month=datetime_obj.month,
        day=datetime_obj.day,
        hour=datetime_obj.hour,
        minute=datetime_obj.minute
    )
    return retdict


def decode_datetime_obj(datetime_dict):
    ret_datetime = datetime.datetime(
        year=datetime_dict['year'],
        month=datetime_dict['month'],
        day=datetime_dict['day'],
        hour=datetime_dict['hour'],
        minute=datetime_dict['minute']
    )
    return ret_datetime

