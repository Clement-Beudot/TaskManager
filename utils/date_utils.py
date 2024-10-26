from datetime import datetime, timedelta

DATE_FORMAT = "%d-%m-%Y"

def to_date(date_input):
    """
    Try to converts an entry into a datetime object, regardless of the format supplied.
    - If the entry is already a datetime object, it is returned as is.
    - If the input is a string, it is converted to datetime (if possible) using the specified format.
    - If the entry is None, returns None.
    """
    if isinstance(date_input, datetime):
        return date_input
    elif isinstance(date_input, str):
        try:
            return datetime.strptime(date_input, DATE_FORMAT)
        except ValueError:
            return None
    return None

def to_string(date_input):
    """
    Converts an input into a character string in the specified format.
    - If the input is already a string, it is returned as is.
    - If the input is a datetime object, it is formatted as a string.
    - If the input is None, returns an empty string.
    """
    if isinstance(date_input, str):
        return date_input
    elif isinstance(date_input, datetime):
        return date_input.strftime(DATE_FORMAT)
    return ""

def today():
    """
    Return today's date in datetime format.
    """
    formatted_datetime = to_string(datetime.today())
    return to_date(formatted_datetime)

def max_at_risk_date():
    """
    Return the max date when consider a task as at risk.
    """
    return today() + timedelta(days=3)