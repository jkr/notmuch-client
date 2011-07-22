import time
from datetime import datetime, date, timedelta

def _timestring_to_datetime (date_string, default_datetime = None):
    """
    Takes a timestring of the form:
       
    [[{YYYY}-]{M}-]{D}

    and converts it a datetime. The.
    """
    if not default_datetime:
        default_datetime = datetime.now()
    try:
        split_date = [int(elem) for elem in date_string.split('-')]
    except ValueError:
        raise NotmuchDateRangeError, \
            "Illegal date format: %s" % split_date

    # Now, we go through the date, and fill in missing parts with our
    # default

    if len(split_date) == 1:
        modified_date = (default_datetime.year,
                         default_datetime.month,
                         split_date[0])
    elif len(split_date) == 2:
        modified_date = (default_datetime.year,
                         split_date[0],
                         split_date[1])
    elif len(split_date) == 3:
        modified_date = split_date
    else:
        raise NotmuchDateRangeError, \
            "Illegal date format: %s" % split_date

    out = datetime(*modified_date)
    return out

class NotmuchDateRangeError (Exception):
    pass

class DateRange (object):

    def __init__ (self, startstamp, endstamp):
        self.start = startstamp
        self.end = endstamp

    @classmethod
    def from_string_range(cls, range_string):
        split_range = range_string.split("--")
        if len(split_range) == 1:
            if range_string[:2] == "--":
                start = datetime.fromtimestamp(0)
                end = _timestring_to_datetime(split_range[0])
            elif range_string[-2:] == "--":
                start = _timestring_to_datetime(split_range[0])
                end = date.now()
        elif len(split_range) == 2:
            start = _timestring_to_datetime(split_range[0])
            end = _timestring_to_datetime(split_range[1])
        else:
            raise NotmuchDateRangeError, \
                "Not a valid range string: %s" % range_string

        end += timedelta(1)

        startstamp = time.mktime(start.timetuple())
        endstamp = time.mktime(end.timetuple())
        return cls(startstamp, endstamp)

    def as_timestamp_range(self):
        return "%d..%d" % (self.start, self.end)

        

            

        

        
        

        
    
