from datetime import datetime

def getBreakdownByPeriod(self_,response, choice, dates_in_period, users, month_or_week):
    displayStartDate = self_.end_date
    all_total = 0


    for week in dates_in_period:
        start_date_, week_start_date, week_end_date = self_.period_details.getStartDate(week, month_or_week)
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
        if self_.period_details.period_type.lower() == 'month':
            if week_end_date_ > datetime.now().date():
                # disp = self_.end_date
                # if disp > datetime.now().date():
                disp = datetime.now().date()
            else:
                disp = week_end_date
        else:
            disp = start_date_


        curr_total = users.filter(
            created__date__gte=start_date_,
            created__date__lte=week_end_date
        ).count()
        all_total += curr_total
        response.append(
            {
                'start_date': disp,
                'total': curr_total,
            }
        )
    # response[0]['all_total'] = all_total
    try:
        response[0]['all_total'] = all_total
    except Exception as e:
        response.append({
            'start_date': displayStartDate,
            'total': 0,
            'all_total': 0
        })

    return response