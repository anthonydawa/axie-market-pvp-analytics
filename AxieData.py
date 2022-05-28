from filter import marketplace_query

import time

class AxieData:

    def __init__(self):
        self.rateLimitMin = 300
        self.rateLimitHour = 1000
        self.currentLimitMin = 300
        self.currentLimitHour = 1000

    def manageRateLimit(self):

        # get request header then before runnin make sure 
        current_unix = int(time.time())
        minute = current_unix % 60
        return minute


    def queryAxie(self):

        return marketplace_query


x = AxieData()
print(x.manageRateLimit())
