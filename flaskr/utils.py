import datetime

def date2Season(date: datetime.date):
    month_number = date.month
    if month_number >= 1 and month_number<=3:
        return 'winter'
    elif month_number >= 4 and month_number<=6:
        return 'spring'
    elif month_number >= 7 and month_number<=9:
        return 'summer'
    elif month_number >= 10 and month_number<=12:
        return 'fall'
    else:
        return 'fall'