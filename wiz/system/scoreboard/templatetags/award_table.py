from django.template import Library

register = Library()

def award_table(award):
    return {'award':award}

register.inclusion_tag('scoreboard/award_table.html')(award_table)
