from datetime import datetime

def convert_date(iso_string: str) -> str:
    """
    Converts an ISO date and time string into human readable local time.

    Parameters
        iso_string (str): An ISO 8601 format date and time string

    Return
        (str) A human-readable date and time string.
    """
    timestamp = datetime.fromisoformat(iso_string).timestamp()
    local_time = datetime.fromtimestamp(timestamp)
    return local_time.strftime("%Y-%m-%d %H:%M")
