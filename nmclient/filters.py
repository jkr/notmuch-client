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
                    return self.pop()
                except IndexError:
                    raise StopIteration
            

            
            
        


            

    

        

    

