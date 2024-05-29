from flask import Flask, render_template, request
from HoundSploit.searcher.engine.suggestions import get_custom_suggestions_list
from HoundSploit.searcher.entities.exploit import Exploit
from HoundSploit.searcher.entities.shellcode import Shellcode
from HoundSploit.searcher.utils.file import download_vulnerability_file
from HoundSploit.searcher.utils.constants import BASE_DIR, TEMPLATE_DIR, STATIC_DIR, N_RESULTS_FOR_PAGE, DEFAULT_SUGGESTIONS

from HoundSploit.server.requests.details import get_exploit_from_params, get_shellcode_from_params
from HoundSploit.server.requests.search_engine import get_search_filters, get_searched_text, is_previous_page_bookmarks, get_current_exploits_page,\
    get_current_shellcodes_page, get_current_results_view, get_sorting_type
from HoundSploit.server.requests.suggestions import get_searched_text_suggestion, get_search_suggestion, get_suggestion_autoreplacement_flag
from HoundSploit.server.requests.bookmarks import get_bookmarks_request_params
from HoundSploit.server.responses.details import render_vulnerability_details
from HoundSploit.server.responses.error_page import render_error_page
from HoundSploit.server.responses.settings import render_settings
from HoundSploit.server.responses.suggestions import render_suggestions
from HoundSploit.server.responses.bookmarks import render_bookmarks
from HoundSploit.server.responses.search_engine import render_advanced_home_page, render_home_page, render_search_results, render_advanced_search_results
from HoundSploit.searcher.engine.updates import install_updates, check_db_changes,check_software_changes, check_no_updates
from HoundSploit.searcher.engine.bookmarks import new_bookmark, is_bookmarked, remove_bookmark
from HoundSploit.searcher.engine.suggestions import new_suggestion, remove_suggestion


def request_search_results():
    searched_text = get_searched_text(request)
    if str(searched_text).isspace() or searched_text == "":
        return render_home_page()
    else:
        search_params = {
            'current_exploits_page': get_current_exploits_page(request),
            'current_shellcodes_page': get_current_shellcodes_page(request),
            'current_view': get_current_results_view(request),
            'sorting_type': get_sorting_type(request)
        }
        return render_search_results(searched_text, search_params)
        
    


def request_advanced_search_results():
    searched_text = get_searched_text(request)
    
    search_params = {
        'current_exploits_page': get_current_exploits_page(request),
        'current_shellcodes_page': get_current_shellcodes_page(request),
        'current_view': get_current_results_view(request),
        'sorting_type': get_sorting_type(request)
    }

    filters = get_search_filters(request)
        
    if str(searched_text).isspace() or searched_text == "":
        return render_advanced_home_page()

    return render_advanced_search_results(searched_text, search_params, filters)


def request_exploit_details():
    exploit = get_exploit_from_params(request)
    searched_text = get_searched_text(request)
    is_prev_page_bookmarks = is_previous_page_bookmarks(request)
    return render_vulnerability_details(exploit, is_prev_page_bookmarks, None)  


def request_shellcode_details():
    shellcode = get_shellcode_from_params(request)
    searched_text = get_searched_text(request)
    is_prev_page_bookmarks = is_previous_page_bookmarks(request)
    return render_vulnerability_details(shellcode, is_prev_page_bookmarks, None) 


def request_download_exploit():
    exploit = get_exploit_from_params(request)
    status, message = download_vulnerability_file(exploit)
    is_prev_page_bookmarks = is_previous_page_bookmarks(request)
    if status:
        return render_vulnerability_details(exploit, is_prev_page_bookmarks, message)
    else:
        return render_error_page(message)


def request_download_shellcode():
    shellcode = get_shellcode_from_params(request)
    print(shellcode.id)
    status, message = download_vulnerability_file(shellcode)
    is_prev_page_bookmarks = is_previous_page_bookmarks(request)
    if status:
        return render_vulnerability_details(shellcode, is_prev_page_bookmarks, message)
    else:
        return render_error_page(message)


def request_add_bookmark_exploit():
    exploit = get_exploit_from_params(request)
    is_prev_page_bookmarks = is_previous_page_bookmarks(request)
    status, message = new_bookmark(exploit)
    if status:
        return render_vulnerability_details(exploit, is_prev_page_bookmarks, None)
    else:
        return render_error_page(message)


def request_add_bookmark_shellcode():
    shellcode = get_shellcode_from_params(request)
    is_prev_page_bookmarks = is_previous_page_bookmarks(request)
    status, message = new_bookmark(shellcode)
    if status:
        return render_vulnerability_details(shellcode, is_prev_page_bookmarks, None)
    else:
        return render_error_page(message)


def request_delete_bookmark_exploit():
    exploit = get_exploit_from_params(request)
    is_prev_page_bookmarks = is_previous_page_bookmarks(request)
    status, message = remove_bookmark(exploit)
    if status:
        return render_vulnerability_details(exploit, is_prev_page_bookmarks, None)
    else:
        return render_error_page(message)


def request_delete_bookmark_shellcode():
    shellcode = get_shellcode_from_params(request)
    is_prev_page_bookmarks = is_previous_page_bookmarks(request)
    status, message = remove_bookmark(shellcode)
    if status:
        return render_vulnerability_details(shellcode, is_prev_page_bookmarks, None)
    else:
        return render_error_page(message)



def request_settings():
    return render_settings(False, False, False)


def request_update():
    install_updates()
    db_update_alert = check_db_changes()
    sw_update_alert = check_software_changes()
    no_updates_alert = check_no_updates(db_update_alert, sw_update_alert)
    return render_settings(db_update_alert, sw_update_alert, no_updates_alert)
    

def request_suggestions_manager():
    return render_template('suggestions.html', suggestions=get_custom_suggestions_list(), default_suggestions=DEFAULT_SUGGESTIONS)


def request_add_suggestion():
    searched = get_searched_text_suggestion(request)
    suggestion = get_search_suggestion(request)
    autoreplacement = get_suggestion_autoreplacement_flag(request)
    status, message = new_suggestion(searched, suggestion, autoreplacement)
    if (status):
        return render_suggestions()
    else:
        return render_error_page(message)


def request_delete_suggestion():
    searched = get_searched_text_suggestion(request)
    status, message = remove_suggestion(searched)
    if (status):
        return render_suggestions()
    else:
        return render_error_page(message)


def request_bookmarks_manager():
    searched_text, current_bookmarks_page = get_bookmarks_request_params(request)
    return render_bookmarks(searched_text, current_bookmarks_page)