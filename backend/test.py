import pysubs2
from translator import translateString
from formats.ass import AssParser

with open('subs.ass') as f:
    file_text = f.read()
parser = AssParser()
parsed_strings = parser.parse(file_text, 'ass')
parsed_strings = translateString(parsed_strings, 'en', 'cs')
result_ass = parser.compose(parsed_strings, 'ass')
with open('output.srt', 'w+') as f:
    f.write(result_ass)
