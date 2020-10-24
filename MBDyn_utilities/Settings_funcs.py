def string_to_list(string_list, sep):
    if string_list:
        #remove first and last blanc
        return string_list.split(sep)
    else:
        return []

def list_to_string(mlist, sep):
    if len(mlist)>0:
        string_list = mlist[0]
        if len(mlist) > 1:
            for item in mlist[1::]:
                string_list += sep + item
    else:
        string_list=""
    return string_list