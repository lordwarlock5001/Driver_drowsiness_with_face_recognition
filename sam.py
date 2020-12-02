import datetime
date = str(datetime.datetime.now().time().hour) + ":" + str(datetime.datetime.now().time().minute) + ":" + str(datetime.datetime.now().time().second)
print(date)