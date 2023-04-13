from flask import Flask, request, render_template, redirect

# https://stackoverflow.com/questions/5607551/how-to-urlencode-a-querystring-in-python
import urllib.parse # for proper encoding of user data in passing it from client to server

from db import memorize

application = Flask (__name__)

NAME_CHECK_RESULTS_IN_SAME_PAGE = "name_check_results_in_same_page"

@application.route("/", methods=['GET', 'POST'])
def root():
    return render_template(
        "search_via_app_with_js_and_db.html"
    )
# def root

@application.route("/search", methods=['GET', 'POST'])
def search():
    bGET:bool = request.method=='GET'
    bPOST:bool = request.method=='POST'

    theUserData:dict = request.args if bGET else request.form

    bGotQuery = 'q' in theUserData.keys()
    bGotCheckResultsInSamePage = NAME_CHECK_RESULTS_IN_SAME_PAGE in theUserData.keys()

    if(bGotQuery):
        q = theUserData['q']
        encoded_q = urllib.parse.quote_plus(
            q
        )
        #search_with_google = "https://www.google.com/search?q="+q
        search_with_google = "https://www.google.com/search?q=" + encoded_q

        # list_all_results = memorize(q, [search_with_google]) # this works on AWS EBS, because it supports FS IO

        # dummy
        list_all_results = [
            {
                'anchor':'App Engine does not allow direct file system IO ops.',
                'href':''
            }
        ]

        if(not bGotCheckResultsInSamePage):
            return redirect(search_with_google)
        else:
            return render_template(
                "search_via_app_with_js_and_db.html",
                r=list_all_results
            )
    else:
        return "<h1>No query received!</h1>"
    # if-else
# def

bCLI = __name__ == '__main__'

if(bCLI):
    application.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
# if