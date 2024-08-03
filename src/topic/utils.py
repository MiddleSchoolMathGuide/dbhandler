'''
Utils for topics
'''

import re


def normalize_title(title: str) -> re.Pattern[str]:
    '''
    Normalize the title to be case-insensitive and allow hyphen/space interchangeability.
    '''

    pattern = re.escape(title).replace(r'\-', r'[- ]').replace(r'\ ', r'[- ]')
    return re.compile(rf'^{pattern}$', re.IGNORECASE)
