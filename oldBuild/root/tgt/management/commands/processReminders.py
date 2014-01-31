from django.core.management.base import NoArgsCommand
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template import Context
from tgt.models import GoodThing, Settings

class Command(NoArgsCommand):
    help = 'Run daily to remind people.'
    
    def handle_noargs(self, **options):
        import datetime
        reminderUsers = Settings.objects.filter(reminderDays__gt=0)
        for setting in reminderUsers:
            cutoff = datetime.datetime.now() - datetime.timedelta(setting.reminderDays)
            user = setting.user
            gts = GoodThing.objects.filter(user=user).filter(posted__gte=cutoff).count()
            if gts == 0:
                
                t = get_template('reminderemail.txt')
                c = Context({ 'user': user })
                message = t.render(c)
                
                send_mail("A reminder from 3GT", message, "reminders@threegthings.net", [user.email])