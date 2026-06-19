import datetime

def parse_date(date_val):
    """
    Parses a date from string (with optional time/timezone) or datetime object,
    returning a datetime.date object.
    """
    if not date_val:
        return None
    if isinstance(date_val, datetime.datetime):
        return date_val.date()
    if isinstance(date_val, datetime.date):
        return date_val
    try:
        # Remove any timestamp/timezone component
        date_str = str(date_val).replace('T', ' ').split(' ')[0]
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Formato de data inválido: {date_val}") from e
