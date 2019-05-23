import logging

from .base import PatternClass

LOGGER = logging.getLogger(__file__)


class AccessLogW3(PatternClass):
    mapping = {
        'remotehost': 1,
        'rfc931': 2,
        'authuser': 3,
        'date': 4,
        'verb': 5,
        'resource': 6,
        'http_version': 7,
        'status': 8,
        'bytes': 9,
    }

    pattern = '^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+)\s?(\S+)?\s?(\S+)?" ' \
              '(\d{3}|-) (\d+|-)\s?"?([^"]*)"?\s?"?([^"]*)?"?$'

    alterations = {
        'section': lambda words: words.get('resource', '/').split('/')[1],
        'error': lambda words: 1 if words.get('status', '100')[0] == '5' else 0,
        'bad_request': lambda words: 1 if words.get('status', '100')[0] == '4' else 0,
        'success': lambda words: 1 if words.get('status', '100')[0] == '2' else 0,
    }

    stats = {
        'bandwidth': lambda buffer, data: AccessLogW3.sum(buffer, data, index=data['section'], item='bytes',
                                                          key='bandwidth'),
        'verb': lambda buffer, data: AccessLogW3.sum(buffer, data, index=data['section'], item='verb', value=1),
        'success': lambda buffer, data: AccessLogW3.sum(buffer, data, index=data['section'], item='success',
                                                        key='success'),
        'bad_request': lambda buffer, data: AccessLogW3.sum(buffer, data, index=data['section'], item='bad_request',
                                                            key='bad_request'),
        'error': lambda buffer, data: AccessLogW3.sum(buffer, data, index=data['section'], item='error', key='error'),
        'hits': lambda buffer, data: AccessLogW3.sum(buffer, data, index=data['section'], key='hits', value=1),

    }

    @staticmethod
    def ensure_section(sections, key):
        if key not in sections:
            sections[key] = dict()

    @staticmethod
    def sum(buffer, data, index, item=None, key=None, value=None):
        if key is None:
            try:
                key = str(data[item])
            except KeyError:
                LOGGER.error("item {} is not located in parsed line")
                return None

        if value is None:
            try:
                value = int(data[item])
            except (ValueError, KeyError):
                value = 0

        AccessLogW3.ensure_section(buffer, index)
        buffer[index][key] = buffer[index].get(key, 0) + value
