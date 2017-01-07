import requests
import json
import itertools
import operator
from nltk.tag.stanford import StanfordNERTagger
st = StanfordNERTagger('stanford-ner/english.all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')

def ocr_space_file(filename, overlay=False, api_key='186247b66c88957', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()


def ocr_space_url(url, overlay=False, api_key='186247b66c88957', language='eng'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()

# Use examples:
test_file = ocr_space_file(filename='rec.png')
test_url = ocr_space_url(url='http://www.pages.drexel.edu/~et95/final/images/Resume2013To.jpg')

rec_json = json.loads(test_file)
resume_json = json.loads(test_url)

# print(rec_json['ParsedResults'][0]['ParsedText'])
# print(resume_json['ParsedResults'][0]['ParsedText'])



# look for name

#--- remove newlines
recj = rec_json['ParsedResults'][0]['ParsedText']
# recj = recj.replace("\r","")
# recj = recj.replace("\n","")
recj = recj.splitlines()
# print(recj)
resumej = resume_json['ParsedResults'][0]['ParsedText']
# ------
def most_common(list):
    sortedList = sorted((x,i) for i, x in enumerate(list))
    groups = itertools.groupby(sortedList, key=operator.itemgetter(0))
    def _auxfun(g):
        item, iterable = g
        count = 0
        min_index = len(list)
        for _, where in iterable:
            count += 1
            min_index = min(min_index, where)
        return count, -min_index
    return max(groups, key=_auxfun)[0]


def listNames(splitline):
    names = []
    for str in splitline:
        str = str[0:-1]
        data = st.tag(str.split())
        for tup in data:
            if tup[1] == 'PERSON':
                names.append(tup[0])
    return names

def oneName(list):
    combinedNames = [i+' '+j for i,j in zip(list[::2],list[1::2])]
    return most_common(combinedNames)

manyNames = listNames(recj)
print(manyNames)
print(oneName(manyNames))
