import sys
import logging
import traceback


def handle_excepthook(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error("An uncaught exception occurred:")
    logging.error("Type: %s", exc_type)
    logging.error("Value: %s", exc_value)

    if exc_traceback:
        format_exception = traceback.format_tb(exc_traceback)
        for line in format_exception:
            logging.error(repr(line))
    raise exc_type(exc_value)


def logger_error(e):

    logger = logging.getLogger()
    log_format = logging.Formatter('%(asctime)-15s %(levelname)-2s %(message)s')
    sh = logging.StreamHandler()
    sh.setFormatter(log_format)
    logger.addHandler(sh)
    logger.setLevel(logging.ERROR)
    logger.error(e, stack_info=True, exc_info=True)
    return logger
