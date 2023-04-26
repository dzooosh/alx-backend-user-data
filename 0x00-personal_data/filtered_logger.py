#!/usr/bin/env python3
""" Filtered logger - logs obfuscated message inputed """
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message, separator: str):
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
    pattern = r"({}=)[^{}]+".format('|'.join(fields), separator)
    return re.sub(pattern, r'\1' + redaction, message)
