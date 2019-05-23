from log_analyzer.patterns.base import PatternClass


class Model(PatternClass):
    rules = [
        dict(name="high_traffic",
             threshold=10,
             key='hits',
             period=5,
             severity=PatternClass.severity.CRITICAL,
             message_on_problem="High traffic generated an alert - hits = {value}/s, triggered at {time}",
             message_on_recover="High traffic recovered at {time}",
             recover_min_time=10,
             )
    ]
