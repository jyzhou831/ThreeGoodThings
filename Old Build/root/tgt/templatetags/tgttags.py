from django import template
from tgt.models import Cheer
register = template.Library()

@register.filter
def userHasCheered(user, gtid):
    return len(Cheer.objects.filter(user=user).filter(goodThing=gtid))
