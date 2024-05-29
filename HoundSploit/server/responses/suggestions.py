from flask import render_template
from HoundSploit.searcher.entities.suggestion import DEFAULT_SUGGESTIONS
from HoundSploit.searcher.engine.suggestions import get_custom_suggestions_list
  
  
def render_suggestions():
    return render_template('suggestions.html', suggestions=get_custom_suggestions_list(), default_suggestions=DEFAULT_SUGGESTIONS)