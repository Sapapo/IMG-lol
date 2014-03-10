__author__ = 'samip_000'


def xstr(s):
    try:
        if s is None:
            return ''
        elif type(s) == 'str':
            return s
        else:
            return str(s)
    except:
        try:
            return s.decode('utf-8', 'ignore')
        except:
            return s


def appif(pre, s, pos):
    if s is None:
        return ''
    if s == '':
        return ''
    s = xstr(s)
    ret = " ".join(s.split())
    return xstr(pre) + ret + xstr(pos)


def u_(s):

    u=xstr(s);
    return u.replace(' ','_').strip(" \r\n\t")


def a_(s,leni=255):

   s= filter(filter_func, s)
   return s[:leni]


def force_numeric(s,default,l=1):

    try:

        si = int(s)
        if (si<00):
            return default
        if (si>2300):
            return default
        return xstr(si).zfill(l)

    except:
        return default


def filter_func(char):
    #print ord(char)
    return 32 <= ord(char) <= 126