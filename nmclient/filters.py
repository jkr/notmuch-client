# -*- python;  coding: utf-8  -*-
#########################################################################
# filters.py: interface for filtering search terms in notmuch-client    #
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

from nmclient.dates import DateRange

def date_filter(token, stack, config):
    if token[:5] == "date:":
        d = DateRange.from_string_range(token[5:])
        stack.push(d.as_timestamp_range())
        return True

    stack.push(token)
    return False

def alias_filter(token, stack, config):
    if token[:6] == "alias:":
        try:
            value = config.aliases[token[6:]]
            stack.push(value)
            return True
        except KeyError:
            pass

    stack.push(token)
    return False
        

class SearchTermStack(object):

    def __init__(self, term_lst, nmconfig):
        self.stack = term_lst
        self.filters = []
        self.config = nmconfig

    def __repr__(self):
        return "Stack%r" % self.stack

    def add_filter(self, arg_filter):
        self.filters.append(arg_filter)

    def add_filters(self, filter_list):
        self.filters += filter_list

    def pop(self):
        tok = self.stack.pop(0)
        tok_list = tok.split()
        out = tok_list.pop(0)
        self.stack = tok_list + self.stack
        return out

    def push(self, string):
        self.stack.insert(0, string)

    def __iter__(self):
        return self

    def next(self):
        i = 0
        while True:
            try:
                fltr = self.filters[i]
                if fltr(self.pop(), self, self.config):
                    i = 0
                else:
                    i += 1
            except IndexError:
                try:
                    return "\"%s\"" % self.pop()
                except IndexError:
                    raise StopIteration
            

            
            
        


            

    

        

    

