import pysubs2
from math import ceil
from ass_tag_parser import parse_ass, compose_ass, errors
from ass_tag_parser.ass_struct import AssText

def autoLineBreaks(long_string, break_char):
    words = long_string.split(' ')

    try:
        max_chars = ceil(len(long_string) / ceil(len(long_string) / 42))
    except ZeroDivisionError:
        max_chars = 500


    char_counter = 0
    for i, word in enumerate(words):
        char_counter += len(word)
        if char_counter > max_chars:
            if i > 0:
                words[i-1] += break_char
                char_counter = 0
    #join words, split them by break char, remove trailing/leading spaces from everything, and join it back with break_char
    return break_char.join(map(str.strip, (" ".join(words).split(break_char))))

def readTagText(tag, stringHolder):
    returnable = None
    if isinstance(tag, AssText):
        returnable = tag
        if stringHolder is not None:
            stringHolder.string += tag.text.replace('\\N', '\n').replace('\r', '\n').replace('\n', '')
        tag.text = '⠀'
    try:
        for sub_tag in tag.tags:
            if readTagText(sub_tag, stringHolder):
                returnable = sub_tag
    except AttributeError:
        pass
    return returnable

class StringHolder:
    def __init__(self):
        self.string = ""
translation_delimeter ='\n'

class AssParser:
    def parse(self, ass_string, sub_format="ass"):
        self.format = sub_format
        subs = pysubs2.SSAFile.from_string(ass_string, sub_format)
        self.subs = subs
        input_hold = StringHolder()
        for line in subs:
            try:
                subdoc = parse_ass(line.text)
            except errors.ParseError:
                input_hold.string += translation_delimeter
            foundTextTag = False
            for tag in subdoc:
                found_tag = readTagText(tag, input_hold)
                if found_tag is not None:
                    foundTextTag = found_tag
            if foundTextTag is not None:
                #if input_hold.string[-1] != '\n':
                    #input_hold.string += '\n'
                input_hold.string += translation_delimeter

            line.text = compose_ass(subdoc)
        return input_hold.string

    def compose(self, translatedString, sub_format="ass"):
        subs = self.subs
        translatedLines = translatedString.split(translation_delimeter)
#print(translatedString)

        line_i = 0
        for sub in subs:
            translated_string = translatedLines[line_i]
            if self.format == "ass":
                translated_string = autoLineBreaks(translated_string, '\\N')
            elif self.format == "srt":
                translated_string = autoLineBreaks(translated_string, '\n')

            subdoc = parse_ass(sub.text)
            for tag in subdoc:
                x = readTagText(tag, None)
                if x is not None:
                    x.text = translated_string
                    line_i += 1
                    break
            sub.text = compose_ass(subdoc)
        subs.info["Original Translation"] = "Líný překlad z dulik.net/aichan"
        return subs.to_string(format_=sub_format)
