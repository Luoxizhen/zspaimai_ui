# -*- coding: utf-8 -*-
"""
@author: 'xiazeng'
@created: 2016/12/2 
"""
import re
import time
import datetime
import threading

try:
    import Queue
except ImportError:
    from queue import Queue
import logging


logger = logging.getLogger()


class LogRecord(object):
    reg_str = (
        r"(?P<time>(\d{4}-)?\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d+)\s+"
        r"(?P<level>[VDIWEFS])\/"
        r"(?P<tag>.*(?=\(\s*\d+\s*\)))\(\s*"
        r"(?P<pid>\d+)\s*\)\s*:\s+"
        r"(?P<msg>.*)"
    )
    reg = re.compile(reg_str, flags=re.VERBOSE | re.MULTILINE)

    def __init__(self, line):
        self.raw_line = line
        m = LogRecord.reg.match(line)
        if m is None:
            raise RuntimeError("invalided line:" + line)
        self.time = m.group("time")
        self.level = m.group("level")
        self.tag = m.group("tag")
        self.pid = m.group("pid")
        self.msg = m.group("msg")

    @property
    def ts(self):
        t = self.time.split(".")
        if len(self.time.split("-")) != 3:
            time_str = "%s-%s" % (datetime.datetime.now().year, t[0])
        else:
            time_str = int(t[0])
        timetuple = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        ts = time.mktime(timetuple) * 1000 + int(t[1])
        return ts

    @classmethod
    def is_valid_line(cls, line):
        m = cls.reg.match(line)
        if not m:
            logger.warn(line)
        return m is not None

    def __repr__(self):
        return "%s %s %s %s" % (self.time, self.level, self.tag, self.msg)


class AsynchronousFileReader(threading.Thread):
    """
    Helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    """

    def __init__(self, fd, queue):
        assert isinstance(queue, Queue)
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queue
        self._reader_stop = False

    def run(self):
        """The body of the tread: read lines and put them on the queue."""
        for line in iter(self._fd.readline, ""):
            self._queue.put(line)
            if self._reader_stop:
                break

    def eof(self):
        """Check whether there is no more content to expect."""
        return not self.is_alive()

    def stop(self):
        self._reader_stop = True
        self.join()


class JLogCat(threading.Thread):
    def __init__(self, adb):
        threading.Thread.__init__(self)
        self._is_stop = False
        adb.run_adb("logcat -c")
        self.process = adb.run_adb("logcat -v time", False)

        # Launch the asynchronous readers of the process' stdout.
        self.stdout_queue = Queue()
        stdout_reader = AsynchronousFileReader(self.process.stdout, self.stdout_queue)
        stdout_reader.start()
        self.stdout_reader = stdout_reader
        self.mutex = threading.Lock()
        self.filter_map = {}
        self.names = []

    def run(self):

        # Check the queues if we received some output (until there is nothing more to get).
        retype = type(re.compile("hello, world"))
        while not self.stdout_reader.eof() and not self._is_stop:
            while not self.stdout_queue.empty() and not self._is_stop:
                line = None
                try:
                    line = self.stdout_queue.get(timeout=0.1)
                    line = line.decode("utf8","ignore")
                except Queue.Empty:
                    print("empty")
                    pass
                if line:
                    for fm in self.filter_map.values():
                        records = fm["records"]
                        for keyword in fm["keywords"]:
                            if isinstance(keyword, str):
                                if keyword in line:
                                    # logger.debug("+logcat, %s", line.strip())
                                    records.append(line.strip())
                            elif isinstance(keyword, retype):
                                if keyword.match(line):
                                    # logger.debug("+logcat, %s", line.strip())
                                    records.append(line.strip())

    def start_record(self, name, *args):
        """
        ????????????
        :param name:????????????
        :param java_regex: java??????????????????
        :return:
        """
        self.mutex.acquire()
        self.filter_map[name] = {"keywords": args, "records": []}
        self.mutex.release()

    def _get_records(self, name):
        self.mutex.acquire()
        lines = self.filter_map[name]["records"]
        records = []
        for l in lines:
            # l = bytes.decode(l)
            if LogRecord.is_valid_line(l):
                records.append(LogRecord(l))
        self.mutex.release()
        return records

    def get_lines(self, name):
        return self._get_records(name)

    def wait_records(self, name, count=1, timeout=10):
        s = time.time()
        while time.time() - s < timeout:
            records = self._get_records(name)
            if len(records) >= count:
                return records
            time.sleep(0.1)
        return []

    def stop_record(self, name):
        records = self._get_records(name)
        self.mutex.acquire()
        del self.filter_map[name]
        self.mutex.release()
        # self.process.kill()
        self.stdout_reader.stop()
        return records

    def stop(self):
        self._is_stop = True
        self.join()
        self.process.kill()
        self.stdout_reader.stop()
        logger.info("logcat finish")
