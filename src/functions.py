from datetime import datetime


async def is_valid_datetime(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False
