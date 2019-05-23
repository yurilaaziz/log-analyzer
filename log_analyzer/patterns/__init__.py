import re


class LineParser:
    def __init__(self, pattern_class):
        self.pattern_class = pattern_class
        self.regex = re.compile(pattern_class.pattern)
        if self.regex is None:
            raise Exception("Regex pattern error")

    def match(self, string, values=None):
        match = self.regex.match(string)
        if match is None:
            return None

        result = dict()
        for item in values or self.pattern_class.mapping:
            result[item] = match.group(self.pattern_class.mapping[item])

        for key, func in self.pattern_class.alterations.items():
            result[key] = func(result)

        return result

    def parse(self, lines):
        results = list()
        for line in lines:
            result = self.match(line)
            if result:
                results.append(result)
        return results
