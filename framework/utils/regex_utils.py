import re


class RegexUtils:

    @staticmethod
    def get_part_string_by_regex(string, regex):
        return re.findall(pattern=regex, string=string)
