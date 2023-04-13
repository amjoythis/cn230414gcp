window.onload = boot;

const ID_TEXT_SEARCH_EXP = "id_text_search_exp",
    ID_BTN_SEARCH = "id_btn_search",
    ID_SECTION_SEARCH_FEEDBACK = "id_section_search_feedback",
    ID_FORM_SEARCH="id_form_search",
    ID_CHECK_RESULTS_IN_SAME_PAGE="id_check_results_in_same_page";

var oTextSearchExp, oBtnSearch, oSectionSearchFeedback, oCheckResultsInSamePage;

function id(pId){return document.getElementById(pId);}

function boot(){
    oTextSearchExp = id(ID_TEXT_SEARCH_EXP);
    oBtnSearch = id(ID_BTN_SEARCH);
    oSectionSearchFeedback = id(ID_SECTION_SEARCH_FEEDBACK);
    oFormSearch = id(ID_FORM_SEARCH);
    oCheckResultsInSamePage = id(ID_CHECK_RESULTS_IN_SAME_PAGE)

    relevant = [oTextSearchExp, oBtnSearch, oSectionSearchFeedback]

    for (r of relevant){
        if (r==null){
            window.alert("Relevant object not available. Aborting.");
            return;
        }
    }//for
    window.alert("All relevant objects available. Proceeding.");

    oFormSearch.onsubmit = oBtnSearch.onclick = go_search;
}//boot

function go_search(){
    var search_for_this = oTextSearchExp.value;
    var search_with_google = "https://www.google.com/search?q="+search_for_this
    document.location.href = search_with_google;
}

