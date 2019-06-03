# -*- coding:utf-8 -*-
# author: will
import sys
import importlib
importlib.reload(sys)
import logging
import os
import re
import time
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler

from utils.file_lock import FileLock


class Logging(object):

    # Manually specify a client
    # sentry_handler = SentryHandler(KeysConfig.get_sentry_dsn())  # 初始化Sentry客户端
    # sentry_handler.setLevel(logging.INFO)  # 设置Sentry客户端日志级别
    #
    # setup_logging(sentry_handler)  # 集成Sentry到log

    _default_format_template = "%(asctime)s [%(levelname)s] [API/%(funcName)s] [%(filename)s:%(lineno)d] %(message)s"

    # logging.config.dictConfig(
    #     setting.LOGGING
    # )
    logger = logging.getLogger(__name__)

    class ReadEasyFormatter(Formatter):
        """日志信息显示汉字而不是unicode"""

        def format(self, record):
            """
            Format the specified record as text.

            The record's attribute dictionary is used as the operand to a
            string formatting operation which yields the returned string.
            Before formatting the dictionary, a couple of preparatory steps
            are carried out. The message attribute of the record is computed
            using LogRecord.getMessage(). If the formatting string uses the
            time (as determined by a call to usesTime(), formatTime() is
            called to format the event time. If there is exception information,
            it is formatted using formatException() and appended to the message.
            """
            record.message = record.getMessage()
            if self.usesTime():
                record.asctime = self.formatTime(record, self.datefmt)
            try:
                s = self._fmt % record.__dict__
            except UnicodeDecodeError as e:
                # Issue 25664. The logger name may be Unicode. Try again ...
                try:
                    record.name = record.name.decode('utf-8')
                    s = self._fmt % record.__dict__
                except UnicodeDecodeError:
                    raise e
            if record.exc_info:
                # Cache the traceback text to avoid converting it multiple times
                # (it's constant anyway)
                if not record.exc_text:
                    record.exc_text = self.formatException(record.exc_info)
            if record.exc_text:
                if s[-1:] != "\n":
                    s = s + "\n"
                try:
                    s = s + record.exc_text
                except UnicodeError:
                    # Sometimes filenames have non-ASCII chars, which can lead
                    # to errors when s is Unicode and record.exc_text is str
                    # See issue 8924.
                    # We also use replace for when there are multiple
                    # encodings, e.g. UTF-8 for the filesystem and latin-1
                    # for a script. See issue 13232.
                    s = s + record.exc_text.decode(sys.path.getfilesystemencoding(),
                                                   'replace')
            if re.findall(r"u'\\u", s):
                s = s.encode('utf-8').decode('unicode_escape')

            return s

    class SafeTimedRotatingFileHandler(TimedRotatingFileHandler):
        """解决多进程日志切分的问题"""

        def doRollover(self):
            """
            do a rollover; in this case, a date/time stamp is appended to the filename
            when the rollover happens.  However, you want the file to be named for the
            start of the interval, not the current time.  If there is a backup count,
            then we have to get a list of matching filenames, sort them and remove
            the one with the oldest suffix.
            """
            if self.stream:
                self.stream.close()
                self.stream = None
            # get the time that this sequence started at and make it a TimeTuple
            currentTime = int(time.time())
            dstNow = time.localtime(currentTime)[-1]
            t = self.rolloverAt - self.interval
            if self.utc:
                timeTuple = time.gmtime(t)
            else:
                timeTuple = time.localtime(t)
                dstThen = timeTuple[-1]
                if dstNow != dstThen:
                    if dstNow:
                        addend = 3600
                    else:
                        addend = -3600
                    timeTuple = time.localtime(t + addend)
            dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
            # dfn = self.baseFilename + "." + str(datetime.datetime.now().date())
            if not os.path.exists(dfn) and os.path.exists(self.baseFilename):
                with FileLock(self.baseFilename):
                    # 加锁后再判断一次,防止多进程中同时修改文件名
                    if not os.path.exists(dfn) and os.path.exists(self.baseFilename):
                        os.rename(self.baseFilename, dfn)

            # if os.path.exists(dfn):
            #     os.remove(dfn)
            # # Issue 18940: A file may not have been created if delay is True.
            # if os.path.exists(self.baseFilename):
            #     os.rename(self.baseFilename, dfn)

            if self.backupCount > 0:
                for s in self.getFilesToDelete():
                    os.remove(s)
            if not self.delay:
                self.stream = self._open()
            newRolloverAt = self.computeRollover(currentTime)
            while newRolloverAt <= currentTime:
                newRolloverAt = newRolloverAt + self.interval
            # If DST changes and midnight or weekly rollover, adjust for this.
            if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
                dstAtRollover = time.localtime(newRolloverAt)[-1]
                if dstNow != dstAtRollover:
                    if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                        addend = -3600
                    else:  # DST bows out before next rollover, so we need to add an hour
                        addend = 3600
                    newRolloverAt += addend
            self.rolloverAt = newRolloverAt

    @classmethod
    def addTimedRotatingFileHandler(cls, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False,
                                    utc=False, fmt=None):
        handler = cls.SafeTimedRotatingFileHandler(filename, when, interval, backupCount, encoding, delay, utc)
        format_template = fmt or cls._default_format_template
        log_format = cls.ReadEasyFormatter(fmt=format_template)
        handler.setFormatter(log_format)
        cls.logger.addHandler(handler)
