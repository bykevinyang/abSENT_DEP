from datetime import datetime

def dateConvert (date):
    """
    Convert date from string to datetime object
    """
    split = date.split(' ')
     
     # Convert month to number
    months = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }

    day = split[1]
    month = months[split[2]]
    year = split[3]
    time = split[4]

    
    return f'{year}-{month}-{day}T{time}'
