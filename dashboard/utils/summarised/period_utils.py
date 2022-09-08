import pytz
import calendar
from datetime import datetime, date, timedelta


class PeriodUtils:
    def __init__(
            self, period_type, start_date, end_date
    ):
        self.period_type = period_type
        self.start_date = start_date
        self.end_date = end_date

    def weeks_dates_in_period(self):
        start_date = datetime.strptime(self.start_date,"%Y-%m-%d")
        end_date = datetime.strptime(self.end_date, "%Y-%m-%d")

        weeks = []
        days_diff = (end_date - start_date).days
        curr_date = start_date
        for k in range(0, days_diff + 1):
            curr_date = curr_date + timedelta(days=1)
            if curr_date.weekday() == 0:
                weeks.append(
                    {
                        'start_date': curr_date,
                        'end_date': curr_date + timedelta(days=6)
                    }
                )
        self.weeks_dates_in_period = weeks


    def month_dates_in_period(self):
        start_date = datetime.strptime(self.start_date,"%Y-%m-%d")
        end_date = datetime.strptime(self.end_date, "%Y-%m-%d")


        num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

        months = []
        curr_date = start_date
        for k in range(0, num_months + 1):
            days_in_curr_month = calendar.monthrange(
                curr_date.year, curr_date.month
            )[1]

            curr_date_end_date = curr_date + timedelta(days=days_in_curr_month)


            months.append(
                {
                    'start_date': date(curr_date.year, curr_date.month, 1),
                    # 'end_date': curr_date_end_date, #curr_date + timedelta(days=days_in_curr_month-1)
                    'month_date': curr_date_end_date - timedelta(days=1),
                    'end_date': curr_date_end_date - timedelta(days=1),
                }
            )
            curr_date = curr_date_end_date
        self.month_dates_in_period = months

    def getSubPeriodDates(self, week, month_or_week):
        """
        Given a start and end date, get the
        """
        start_date = None
        try:
            start_date_ = week['start_date'].date()
        except Exception as e:
            start_date_ = week['start_date']
        try:
            month_date = week['month_date'].date()
        except Exception as e:
            pass
        start_date = start_date_
        start_date_ = start_date_ if month_or_week.upper() \
                                     != 'month'.upper() else month_date

        return start_date, start_date_, week['end_date']

    def getPeriodDispalyDate(
            self, week_start_date, week_end_date,
            start_date_, end_date,
    ):
        try:
            week_start_date = str(week_start_date.date())
        except Exception as e:
            week_start_date = str(week_start_date)
        try:
            week_end_date_ = week_end_date.date()
            week_end_date = str(week_end_date.date())

        except Exception as e:
            week_end_date_ = week_end_date
            week_end_date = str(week_end_date)
        if self.period_type.upper() == 'month'.upper():
            if week_end_date_ > datetime.now().date():
                disp = end_date
            else:
                disp = week_end_date
        else:
            disp = start_date_

        return disp

    def getStartDate(self, week, month_or_week):
        start_date = None
        try:
            start_date_ = week['start_date'].date()
        except Exception as e:
            start_date_ = week['start_date']
        try:
            month_date = week['month_date'].date()
        except Exception as e:
            pass
        start_date = start_date_
        start_date_ = start_date_ if month_or_week != 'month' else month_date

        return start_date, start_date_, week['end_date']

    def time_to_eat(self, start_time, timezone="Africa/Nairobi"):
        timezone = "Africa/Nairobi"
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f %z')
        utcmoment = start_time.replace(tzinfo=pytz.utc)
        localDatetime = utcmoment.astimezone(pytz.timezone(timezone))
        start_time = localDatetime.strftime("%Y-%m-%d %H:%M:%S")
        return datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

