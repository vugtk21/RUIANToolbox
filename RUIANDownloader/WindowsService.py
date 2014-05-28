# -*- coding: utf-8 -*-
"""To install RUIANDownloader you have to open the command line as administrator, change directory to where your python
interpreter is located and run command "python.exe [path to RUIANDownloader]/RUIANDownloader.py install". After that
you can run the service by command "NET START DldSvc". Running service can be stopped by command "NET STOP DldSvc"."""

import win32service
import win32serviceutil
import win32event
import datetime
import time
import RUIANDownload

#i = 40

class RUIANDld(win32serviceutil.ServiceFramework):
    # you can NET START/STOP the service by the following name
    _svc_name_ = "RUIANDld"
    # this text shows up as the service name in the Service
    # Control Manager (SCM)
    _svc_display_name_ = "RUIAN Downloader"
    # this text shows up as the description in the SCM
    _svc_description_ = "This service writes stuff to a file"

    def download(self):
        RUIANDownload.main(None)

    def getTimeToDownload(self):
        #global i
        now=datetime.datetime.now()
        time=now.replace(day=now.day + 1, hour=0, minute=0, second=0, microsecond=0)
        #time=now.replace(day=now.day, hour=13, minute=i, second=0, microsecond=0)
        #i=i+1
        return time

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.isAlive = True
        self.secondsToWait=60
        self.startTime = self.getTimeToDownload()

    def SvcStop(self):
        self.isAlive = False
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # fire the stop event
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        while(self.isAlive):
            now = datetime.datetime.now()
            if (now>self.startTime):
                self.download()
                self.startTime = self.getTimeToDownload()
            time.sleep(self.secondsToWait)

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(RUIANDld)