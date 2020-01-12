import logging

INFO = logging.INFO
DEBUG = logging.DEBUG
ERROR = logging.ERROR
WARNING = logging.WARNING


def warning(msg, name = None, *args, **kwargs):
	if name is not None:
		logger = logging.getLogger(name)
	else:
		logger = logging.getLogger()
	logger.warning(msg)


def info(msg, name = None, *args, **kwargs):
	if name is not None:
		logger = logging.getLogger(name)
	else:
		logger = logging.getLogger()
	logger.info(msg)


def error(msg, name = None, *args, **kwargs):
	if name is not None:
		logger = logging.getLogger(name)
	else:
		logger = logging.getLogger()
	logger.error(msg)


def critical(msg, name = None, *args, **kwargs):
	if name is not None:
		logger = logging.getLogger(name)
	else:
		logger = logging.getLogger()
	logger.critical(msg)


def basicConfig(*args, **kwargs):
	logging.basicConfig(*args, **kwargs)
