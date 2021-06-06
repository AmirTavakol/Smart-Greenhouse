import schedule
import time
import ET0
import ETc
import trigger

schedule.every().day.at("16:30").do(ET0.ET0_2_db)
schedule.every().day.at("16:35").do(ETc.saveETc)
schedule.every().day.at("16:40").do(trigger.trigger)


while True:
    schedule.run_pending()
    time.sleep(58) #check almost every minute