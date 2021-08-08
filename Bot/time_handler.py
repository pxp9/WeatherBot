import datetime as dt
import main

today = dt.date.today()
weekday = today.weekday()





def hello_world():
    e = dt.datetime.now()
    print ("Today's date:  = %s/%s/%s" % (e.day, e.month, e.year))
    print ("The time is now: = %s:%s:%s" % (e.hour, e.minute, e.second))
    print("FUCK IT")

def days_for_next_friday():

    next_friday = today + dt.timedelta( (4- weekday) % 7 )
    diff = str(next_friday - today)[0:1]
    print("Today is: "+str(today) + " and next friday is: "+str(next_friday)+" and there is a difference of "+str(diff)+" days")
    return diff


def days_for_last_friday():

    last_friday =  today - dt.timedelta(days=weekday) + dt.timedelta(days=4, weeks=0)

    diff =  diff = str(today - last_friday)[0:1]
    print("Today is: "+str(today) + " and before friday is: "+str(last_friday)+" and there is a difference of "+str(diff)+" days")
    return diff

def time_handler():

    if( weekday == 5 or weekday == 6):
        diff = days_for_last_friday()
    else:
        diff = days_for_next_friday()
