from datetime import timedelta, time


class AppSettings:
    def __init__(self, interval_hours: int, period: timedelta, start_time: time):
        self.INTERVAL_HOURS = interval_hours
        self.PERIOD = period
        self.START_TIME = start_time
