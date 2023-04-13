from datetime import datetime
import json

from am_consumer import findAnchorsAtUrl, get_google_organic_result_anchors

DB = "SEARCHES.DB"

def harvest(
    url
):
    pass

def memorize(
    pSearchExp:str,
    pListSearchQueries:list
):
    now = datetime.now()
    y = now.year
    m = now.month
    d = now.day
    h = now.hour
    mm = now.minute
    s = now.second

    str_now = f"{y}-{m}-{d} {h}:{mm}:{s}"

    all_results = list()
    iBytesWritten = 0
    for q in pListSearchQueries:
        anchors = findAnchorsAtUrl(q)
        list_results = get_google_organic_result_anchors(anchors)
        all_results+=list_results
        json_list_results = json.dumps(list_results)

        r = {
            'when':str_now,
            'what':pSearchExp,
            'how':q,
            'results':json_list_results
        }
        json_r = json.dumps(r)

        record = f"{json_r}\n"

        iBytesWritten += update(record)
    # for

    #return iBytesWritten
    return all_results
# memorize

def update(
    record:str
):
    try:
        fw = open(DB, 'a')
        if(fw):
            ibytes_written = fw.write(record)
            fw.close()
            return ibytes_written
        # if
    except Exception as e:
        return 0
    # try-except

    return 0
# def update

def select():
    try:
        fr = open(DB, 'r')
        if(fr):
            strAll = fr.read()
            fr.close()
            return strAll
        # if
    except Exception as e:
        return False
    # try-except

    return False
# def select
