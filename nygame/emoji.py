import re

from emoji import EMOJI_ALIAS_UNICODE_ENGLISH


def emojize(s):
    pattern = re.compile(u'(:[A-zÀ-ÿ0-9\\-_&.’”“()!#*+?–]+:)')

    def replace(match):
        mg = match.group(1)
        emj = EMOJI_ALIAS_UNICODE_ENGLISH.get(mg.replace("-", "_"), mg)
        return emj
    return pattern.sub(replace, s)
