#!/usr/bin/env python3
""" Filtered logger - logs obfuscated message inputed """
import re
from typing import List
import logging


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    fiter_datum - obfuscate messages
    Args:
    fields - list of strings reping all fields to obfuscate
    redaction - a string reping by what the field will be obfuscated
    message -a string reping the log line
    separator - a string reping by which character is
                seperating all fields in the log line (message)

    Returns: the log message obfuscated
    """
    for field in fields:
        pattern = field + "=.*?" + separator
        message = re.sub(pattern, field + "=" + redaction + separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        format - filter values in incoming log records using
                    filter_datum
        Args:
        @record - loggings LogRecord
        """
        message = super(RedactingFormatter, self).format(record)
        filtered_message = filter_datum(self.fields, self.REDACTION,
                                        message, self.SEPARATOR)
        return filtered_message

    def get_logger() -> logging.Logger:
        """
        get_logger - returns logging.Logger object
        """
        logger = logging.getLogger("user_data")
        logger.setLevel(logging.INFO)
        logger.propagate = False

        stream_handler = logging.StreamHandler()
        formatter = RedactingFormatter(PII_FIELDS)

        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        return logger
