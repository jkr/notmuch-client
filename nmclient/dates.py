# -*- python;  coding: utf-8  -*-
#########################################################################
# dates.py: for use with date-range substitution in notmuch-client      #
#                                                                       #
# Copyright © 2011 Jesse Rosenthal                                      #
#                                                                       #
# This program is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program.  If not, see http://www.gnu.org/licenses/ .  #
#                                                                       #
# Author: Jesse Rosenthal <jrosenthal@jhu.edu>                          #
#########################################################################

import time
from datetime import datetime, date, timedelta

relative_day_dict = {"monday": 0,
                     "tuesday": 1,
                     "wednesday": 2,
                     "thursday": 3,
                     "friday": 4,
                     "saturday": 5,
                     "sunday": 6,
                     "mon": 0,
                     "tue": 1,
                     "wed": 2,
                     "thu": 3,
                     "fri": 4,
                     "sat": 5,
                     "sun": 6}

def _dayname_to_datetime (dayname):
    dayname_lower = dayname.lower()
    today = date.today()
    today_day_num = today.weekday()

    if dayname_lower in ("today", "yesterday"):
        return today - timedelta(("today", "yesterday").index(dayname_lower))
    elif dayname_lower in relative_day_dict:
        return today - timedelta((today_day_num - 
                                  day_dict[dayname_lower]) % 7)
    else:
        raise NotmuchDateRangeError, \
            "Unknow date keyword: %s" % dayname

def _timestring_to_datetime (date_string, default_datetime = None):
    """
    Takes a timestring of the form:
       
    [[{YYYY}-]{M}-]{D}

    and converts it a datetime. The.
    """
    if not default_datetime:
        default_datetime = date.today()
    try:
        out = _dayname_to_datetime(date_string)
    except NotmuchDateRangeError:
        try:
            split_date = [int(elem) for elem in date_string.split('-')]
        except ValueError:
            raise NotmuchDateRangeError, \
                "Illegal date format: %s" % date_string
        
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
            start = _timestring_to_datetime(split_range[0])
            end = start
        elif len(split_range) == 2:
            if not split_range[0]:
                start = datetime.fromtimestamp(0)
                end = _timestring_to_datetime(split_range[0])
            elif not split_range[1]:
                start = _timestring_to_datetime(split_range[0])
                end = date.today()
            else:
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

        

            

        

        
        

        
    
