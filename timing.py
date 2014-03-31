import datetime as dt

def time_elapsed(func_name, start_time):
    end_time = dt.datetime.now()
    print func_name, ':', end_time - start_time
    return end_time 