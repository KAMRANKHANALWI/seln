from datetime import datetime

def parse_date_string(date_string):
    # Parse the date string into a datetime object
    date_object = datetime.strptime(date_string, '%d-%m-%Y')

    # Extract day, month, and year from the datetime object
    day = date_object.day
    month = date_object.month
    year = date_object.year

    # Format the day and month with leading zeros if necessary
    formatted_day = "{:02d}".format(day)
    formatted_month = "{:02d}".format(month)

    return formatted_day, formatted_month, year

# Test the function
date_string = "13-07-1995"
day, month, year = parse_date_string(date_string)
print(day)
print(month)
print(year)
