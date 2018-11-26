from django.shortcuts import render, redirect
from searcher.search_engine import search_exploits_in_db


def home_page(request):
    if request.POST:
        search_text = request.POST['search_item']
        return render(request, "home.html", {'searched_item': str(search_text),
                                             'results': search_exploits_in_db(search_text),
                                             'n_results': len(search_exploits_in_db(search_text))})
    else:
        return render(request, 'home.html')
