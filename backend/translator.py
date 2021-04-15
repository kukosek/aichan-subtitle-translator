import requests


apiurl = 'https://lindat.mff.cuni.cz/services/translation/api/v2/languages/'
def translateString(en_str, src_lang_code, tgt_lang_code):
    r = requests.post(apiurl, data={'src':src_lang_code, 'tgt':tgt_lang_code, 'input_text':en_str})
    r.encoding = r.apparent_encoding
    return r.text
