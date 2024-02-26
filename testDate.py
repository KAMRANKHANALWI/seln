from datetime import datetime

def format_date_string(date_string):
    # Split the date string into day, month, and year
    day, month, year = date_string.split()

    # Remove the suffix (e.g., 'th', 'st', 'nd', 'rd') from the day
    day = day[:-2] if day[-2:] in ['th', 'st', 'nd', 'rd'] else day

    # Convert month name to its respective integer value
    month = datetime.strptime(month, '%B').month

    # Format the date string as DD-MM-YYYY
    formatted_date = "{:02d}-{:02d}-{}".format(int(day), month, year)

    return formatted_date


from datetime import datetime

def format_date(date_string):
    # Split the date string into day, month, and year
    day, month, year = date_string.split()

    # Remove the suffix (e.g., 'th', 'st', 'nd', 'rd') from the day
    day = day[:-2] if day[-2:] in ['th', 'st', 'nd', 'rd'] else day

    # Convert month name to its respective integer value
    month = datetime.strptime(month, '%B').month

    # Convert day, month, and year to integers
    day = int(day)
    month = int(month)
    year = int(year)

    # Format the day and month with leading zeros if necessary
    formatted_day = "{:02d}".format(day)
    formatted_month = "{:02d}".format(month)

    return formatted_day, formatted_month, year

# Test the function
firstDate = "24 February 2011"
day, month, year = format_date(firstDate)
print(day)
print(month)
print(year)
print(format_date(firstDate))


# # Test the function
# firstDate = "10th March 2011"
# formatted_date = format_date_string(firstDate)
# print(formatted_date)  # Output: 10-03-2011
