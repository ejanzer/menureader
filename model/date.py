import datetime

def get_date():
    return datetime.datetime.utcnow()


def format_date(date):
    return datetime.datetime.strftime(date, '%D')