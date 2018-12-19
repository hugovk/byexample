from __future__ import unicode_literals
import re
from byexample.finder import ZoneDelimiter
from byexample.common import constant

stability = 'experimental'

class MarkdownFencedCodeDelimiter(ZoneDelimiter):
    target = {'.md'}

    @constant
    def zone_regex(self):
        return re.compile(r'''
            # Begin with a markdown fenced-code marker or a html comment marker
            ^[ ]*
                (?:
                    (?P<marker>```(?:``)*(?=[^`]))  # fenced-code marker (backticks)
                    | (?:<!--)              # or the html comment marker
                )

            # then, grab everything until the first end marker
            (?P<zone>.*?)

            # finally, the end marker
            (?(marker)    # if we matched a fenced-code maker previously
                  ^[ ]*(?P=marker) # then we must match the same amount of backticks
                  |(?:-->)    # otherwise, we must match the close of the html comment
            )
            ''', re.DOTALL | re.MULTILINE | re.VERBOSE)

    def __repr__(self):
        return "Markdown Fenced-Code Delimiter"
