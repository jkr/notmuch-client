from datetime import datetime

class NotmuchDateRangeError (Exception):
    pass

class DateRange (object):

    def __init__ (self, startstamp, endstamp):
        self.start = startstamp
        self.end = endstamp

    @classmethod
    def from_string_range(self, range_string):
        try:
            start, end = range_string.split("..")
        except ValueError:
            raise NotmuchDateRangeError, \
                "Not a valid range string: %s" % range_string

        
        

        
    
