import requests
import json
#--- FIND NAME --
import itertools
import operator
from nltk.tag.stanford import StanfordNERTagger
#--- FIND EMAIL --
import re
#--- TO TXT FILE --
import sys


# ---------- FROM PDF TO TEXT ----------
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

# ---------- END (PDF TO TEXT) ----------

# ----- splitlines the data -----
recj = rec_json['ParsedResults'][0]['ParsedText']
recj = recj.splitlines()
resumej = resume_json['ParsedResults'][0]['ParsedText']
resumej = resumej.splitlines()
# ----- end (splitlines the data) -----

# ---------- FIND NAME OF APPLICANT ----------
st = StanfordNERTagger('stanford-ner/english.all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')

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

# ---------- END (FIND NAME OF APPLIANT) ----------


# ---------- FIND APPLICANT EMAIL ----------
regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

def findEmail(splitline):
    ret = []
    realRet = []
    for str in splitline:
        match = re.findall(r'[\w\.-]+@[\w\.-]+', str)
        ret.append(match)
    for item in ret:
        if item != []:
            realRet.append(item[0])
    if len(realRet) == 1:
        return realRet[0]
    else:
        return realRet

# print(findEmail(resumej))
# print(findEmail(recj))
# ---------- END (FIND APPLICANT EMAIL) ----------


# ---------- FIND APPLICANT PHONE NUMBER ----------
regex = re.compile("\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b")

def findPhone(splitline):
    ret = []
    realRet = []
    for str in splitline:
        match = re.findall(r"\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b", str)
        ret.append(match)
    for item in ret:
        if item != []:
            realRet.append(item[0])
    if len(realRet) == 1:
        return realRet[0]
    else:
        return realRet

# ---------- END (APPLICANT PHONE NUMBER) ----------


# ---------- IDENTIFY GENDER WORDS ----------
genderID = {"they":["he","she"],
            "them":["him","her"],
            "their":["his","hers"],
            "themself":["himself","herself"],
            "person":["woman","man","boy","girl"],
            "people":["women","men","boys","girls"],
            "business executive":["businessman","businesswoman", "business man", "business woman"],
            "cleaner":["cleaning lady"],
            "courier":["delivery boy", "delivery man", "delivery woman"],
            "supervisor":["foreman"],
            "insurance agent":["insurance man"],
            "proprietor":["landlady","landlord"],
            "mail carrier":["mailman"],
            "journalist":["newsman"],
            "police officer":["policeman"],
            "technician":["repairman"],
            "sales agent":["saleslady","salesman"],
            "service representative":["serviceman"],
            "flight attendant":["steward","stewardess"],
            "server":["waiter","waitress"],
            "worker":["workman"],
            "chairperson":["chairman","chairwoman"],
            "committee member":["committee man","committee woman"],
            "first-year student":["freshman"],
            "figurehead":["front man"],
            "host":["hostess"],
            "homemaker":["housewife","househusband"],
            "go-between":["middleman"],
            "troubleshooter":["ombudsman"],
            "entrepreneur":["self-made man"],
            "spokesperson":["spokesman"],
            "wage earner":["working man","working woman"],
            "gigantic":["king-size"],
            "courteous":["ladylike"],
            "birth name":["maiden name"],
            "human resources":["manpower"],
            "host":["master of ceremonies"],
            "synthetic":["man made","man-made"],
            "dynamo":["man of action"],
            "staff horus":["man-hour"],
            "nurturing":["motherly"],
            "upstaging":["one-up-manship"],
            "diplomat":["statesman"],
            "expertise":["workmanship"],
            "best person for the job":["best man for the job","best woman for the job"],
            "principal":["headmaster","headmistress"],
            "layperson":["layman"],
            "staffed":["manned"]
            }
# ---------- END (IDENTIFY GENDER WORDS) ---------

# ---------- FINAL THINGS -----------
# def doNA(string):
#     if string is None:
#         return "N/A"

def writeToFile():
    print("Writing to results.txt . . .")
    rfile = open('results.txt','w')
    rfile.write("REC\n")
    rfile.write("Name: " + oneName(listNames(recj)) + "\n")
    rfile.write("Email: " + str(findEmail(recj)) + "\n")
    rfile.write("Phone: " + str(findPhone(recj)) + "\n")
    rfile.write(" \n")
    rfile.write("RESUME\n")
    rfile.write("Name: " + oneName(listNames(resumej)) + "\n")
    rfile.write("Email: " + str(findEmail(resumej)) + "\n")
    rfile.write("Phone: " + str(findPhone(resumej)) + "\n")
    rfile.close()
    print("Done!")

# ----------- RUN -----------
writeToFile()
