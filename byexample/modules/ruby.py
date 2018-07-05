"""
Example:
  >> def hello
  >>     'hello bla world'
  >> end;

  >> hello
  => "hello<...>world"

  ```ruby

  j = 2;
  (0..3).each do |i|
    j += i;
  end;

  j + 3

  out:
  => 11

  >> { 1 => 2, 3=>{4=>"aaaaaaaa", 5=>Array(0..20)}}
  => {1=>2,
   3=>
    {4=>"aaaaaaaa",
     5=>
      [0,
       1,
       <...>
       19,
       20]}}

  ```
"""

import re, pexpect, sys, time
from byexample.common import constant
from byexample.parser import ExampleParser
from byexample.finder import ExampleFinder
from byexample.runner import ExampleRunner, PexepctMixin

class RubyPromptFinder(ExampleFinder):
    target = 'ruby-prompt'

    @constant
    def example_regex(self):
        return re.compile(r'''
            # Snippet consists of one or more PS1 lines >>
            (?P<snippet>
                (?:^(?P<indent> [ ]*) >>[ ]     .*)    # PS1 line
                (?:\n           [ ]*  >>      .*)*)    # and more PS1 lines
            \n?
            # Want consists of any non-blank lines that do not start with PS1
            # The '=>' indicator is included (implicitly)
            (?P<expected> (?:(?![ ]*$)     # Not a blank line
                          (?![ ]*>>)       # Not a line starting with PS1
                         .+$\n?            # But any other line
                      )*)
            ''', re.MULTILINE | re.VERBOSE)

    def get_language_of(self, *args, **kargs):
        return 'ruby'

    def get_snippet_and_expected(self, match, where):
        snippet, expected = ExampleFinder.get_snippet_and_expected(self, match, where)

        snippet = self._remove_prompts(snippet)
        return snippet, expected

    def _remove_prompts(self, snippet):
        lines = snippet.split("\n")
        return '\n'.join(line[3:] for line in lines)

class RubyParser(ExampleParser):
    language = 'ruby'

    @constant
    def example_options_string_regex(self):
        return re.compile(r'#\s*byexample:\s*([^\n\'"]*)$',
                                                    re.MULTILINE)

    def extend_option_parser(self, parser):
        parser.add_flag("ruby-pretty-print", help="enable the pretty print enhancement.")
        return parser

class RubyInterpreter(ExampleRunner, PexepctMixin):
    language = 'ruby'

    def __init__(self, verbosity, encoding, **unused):
        PexepctMixin.__init__(self,
                                cmd=None,
                                PS1_re = r'irb[^:]*:\d+:0(>|\*) ',
                                any_PS_re = r'irb[^:]*:\d+:\d+(>|\*) ')

        self.encoding = encoding

    def run(self, example, flags):
        return self._exec_and_wait(example.source,
                                    timeout=int(flags['timeout']))

    def interact(self, example, options):
        PexepctMixin.interact(self)

    def initialize(self, examples, options):
        ruby_pretty_print = options.get('ruby_pretty_print', True)

        # set the final command
        self.cmd = '/usr/bin/env irb'

        # run!
        self._spawn_interpreter(delaybeforesend=options['delaybeforesend'])

        # set the pretty print inspector
        if ruby_pretty_print:
            self._exec_and_wait('IRB.CurrentContext.inspect_mode = :pp\n',
                                    timeout=2)

    def shutdown(self):
        self._shutdown_interpreter()
