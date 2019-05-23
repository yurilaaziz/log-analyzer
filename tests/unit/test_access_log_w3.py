import pytest

from log_analyzer.calculator import Calculator
from log_analyzer.patterns import LineParser
from log_analyzer.patterns.access_log_w3 import AccessLogW3
from log_analyzer.persistence.memory import MemoryPersistence


@pytest.fixture
def parsed_line_data(w3_access_log_lines):
    w3_pattern = LineParser(AccessLogW3)
    results = []
    for line in w3_access_log_lines:
        results.append(w3_pattern.match(line))
    return results


def test_match_mapping(w3_access_log_lines):
    w3_pattern = LineParser(AccessLogW3)
    for line in w3_access_log_lines:
        result = w3_pattern.match(line)
        for key in w3_pattern.pattern_class.mapping.keys():
            assert result.get(key) is not None


def test_words_alteration(w3_access_log_lines):
    w3_pattern = LineParser(AccessLogW3)
    for line in w3_access_log_lines:
        result = w3_pattern.match(line)
        assert result.get('section', '') in result.get('resource', '')


def test_calculate_stats(parsed_line_data):
    persistence = MemoryPersistence()
    calculator = Calculator(AccessLogW3, persistence=persistence)

    stats = calculator.compute(parsed_line_data)

    assert 'bandwidth' in stats['api']
    assert stats['api']['bandwidth'] == 280
    assert stats['api']['GET'] == 1
    assert stats['api']['success'] == 2


def test_model_sum_static(parsed_line_data):
    buffer = {}
    for data in parsed_line_data:
        AccessLogW3.sum(buffer, data, data['section'], item='bytes', key='bandwidth')
        AccessLogW3.sum(buffer, data, data['section'], item='verb', value=1)
        AccessLogW3.sum(buffer, data, data['section'], key='hits', value=1)

    assert 'bandwidth' in buffer['api']
    assert buffer['api']['bandwidth'] == 280
    assert buffer['api']['GET'] == 1
