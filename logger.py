import os
import sys
import traceback
import logging
import logging.handlers

from queue import SimpleQueue as Queue
from qtCore import *


# LoggingHandler based on KlipperScreen's LoggingHandler setup
# Rotating file handler based on Klipper and Moonraker's implementation
class MixLoggingHandler(logging.handlers.RotatingFileHandler):
    def __init__(self, software_version, filename, **kwargs):
        super(MixLoggingHandler, self).__init__(filename, **kwargs)
        self.rollover_info = None

    def set_rollover_info(self, name, item):
        self.rollover_info[name] = item

    def doRollover(self):
        super(MixLoggingHandler, self).doRollover()
        lines = [line for line in self.rollover_info.values() if line]
        if self.stream is not None:
            self.stream.write("\n".join(lines) + "\n")


# Logging based on Arksine's logging setup
class MixLogger(QObject):
    def __int__(self, log_file, software_version):
        # super(MixwareScreenLogger, self).__int__(log_file, software_version)
        self.log_file = log_file
        self.software_version = software_version

    def setup_logging(self):
        root_logger = logging.getLogger()
        queue = Queue()
        queue_handler = logging.handlers.QueueHandler(queue)
        root_logger.addHandler(queue_handler)
        root_logger.setLevel(logging.DEBUG)

        stdout_hdlr = logging.StreamHandler(sys.stdout)
        stdout_fmt = logging.Formatter('%(asctime)s [%(filename)s:%(funcName)s()] - %(message)s')
        stdout_hdlr.setFormatter(stdout_fmt)

        fh = listener = None

        try:
            fh = MixLoggingHandler(self.software_version, self.log_file, maxBytes=4194304, backupCount=1)
            formatter = logging.Formatter('%(asctime)s [%(filename)s:%(funcName)s()] - %(message)s')
            fh.setFormatter(formatter)
            listener = logging.handlers.QueueListener(queue, fh, stdout_hdlr)
        except Exception as e:
            print(
                f"Unable to create log file at '{os.path.normpath(self.log_file)}'.\n"
                f"Make sure that the folder '{os.path.dirname(self.log_file)}' exists\n"
                f"and KlipperScreen has Read/Write access to the folder.\n"
                f"{e}\n"
            )
        if listener is None:
            listener = logging.handlers.QueueListener(queue, stdout_hdlr)
        listener.start()

        def logging_exception_handler(ex_type, value, tb, thread_identifier=None):
            logging.exception(
                f'Uncaught exception {ex_type}: {value}\n'
                + '\n'.join([str(x) for x in [*traceback.format_tb(tb)]])
            )

        sys.excepthook = logging_exception_handler
        logging.captureWarnings(True)

        return listener, fh

