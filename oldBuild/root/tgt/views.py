from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from django.db.models import Q
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt
from django_facebook.canvas import generate_oauth_url
from django.shortcuts import render_to_response
from django import forms
from models import GoodThing, WordClouds, Cheer, Settings
from django.contrib.auth.models import User
from django.contrib.auth import logout
import django_facebook
from django.core.paginator import Paginator, InvalidPage
from django.utils import timezone
#import urllib, urllib2
#from tasks import scrapeGoodThing

### FORMS GO HERE

class GoodThingForm(forms.ModelForm):
    class Meta:
        model = GoodThing
        widgets = {'goodThing':forms.Textarea(),
                   'reason':forms.Textarea(),
                  }
                  
class SettingsForm(forms.Form):
    reminders = forms.BooleanField(required=False)
    reminderDays = forms.ChoiceField(choices=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5')))
    defaultFB = forms.BooleanField(required=False)
    defaultPublic = forms.BooleanField(required=False)
    
### API STUFF GOES HERE

def api_things(request):
    t = loader.get_template('thingsjson.json')
    page = request.GET.get("page",1)

    #objectlist will eventually depend on what they are asking for. but for now...
    specificUser = request.GET.get("uid",False)
    if specificUser:
         gtlist = GoodThing.objects.filter(deleted=False).order_by('-posted').filter(public=1).filter(user=specificUser)
    elif request.user.is_authenticated():
        gtlist = GoodThing.objects.filter(deleted=False).order_by('-posted').filter(Q(public=1)|Q(user=request.user))
    else:
         gtlist = GoodThing.objects.filter(deleted=False).order_by('-posted').filter(public=1)

    paginator = Paginator(gtlist,30)
    page_obj = paginator.page(page)
    c = RequestContext(request,{
            "object_list": page_obj.object_list,
            "page": page_obj
            })
    return HttpResponse(t.render(c))

def api_delete(request):
    if request.user.is_authenticated():
        gt = GoodThing.objects.get(id=request.POST['gtid'])
        if gt.user == request.user:
            gt.deleted = True
            gt.save()
            
            try:
               wc = WordClouds.objects.get(user=request.user)
            except:
               wc = WordClouds()
               wc.user = request.user
           
            wc.updateClouds()
            return HttpResponse("")

    return HttpResponseForbidden()

def api_cheer(request):
    if request.user.is_authenticated():
        gt = GoodThing.objects.get(id=request.POST['gtid'])
        cheer = Cheer()
        cheer.user = request.user
        cheer.goodThing = gt
        cheer.save()
        
        return HttpResponse(str(gt.id))

    return HttpResponseForbidden()

def api_uncheer(request):
    if request.user.is_authenticated():
        gt = GoodThing.objects.get(id=request.POST['gtid'])
        cheers = Cheer.objects.all().filter(goodThing=gt).filter(user=request.user)
        for cheer in cheers: cheer.delete()
        return HttpResponse(str(gt.id))

    return HttpResponseForbidden()

def api_saveGoodThing(request):
    if request.user.is_authenticated():
        fb = django_facebook.api.get_persistent_graph(request)
        
        gt = GoodThing()
        gt.user = request.user
        gt = GoodThingForm(request.POST,instance=gt)
        gt.save()
        
        #if gt.instance.public:
            #vals = {'id':gt.instance.link(),'scrape':'true'}
            #data = urllib.urlencode(vals)
            #req = urllib2.Request("https://graph.facebook.com", data)
            #response = urllib2.urlopen(req)
            #scrapeGoodThing.delay(gt.instance.id)
                        
        try:
            wc = WordClouds.objects.get(user=request.user)
        except:
            wc = WordClouds()
            wc.user = request.user
        wc.updateClouds()
        
        if gt.instance.wall:
            if not gt.instance.public:
                gt.instance.postFB(fb,useog=False)
            else:
                gt.instance.postFB(fb)
        
        t =  loader.get_template('thingjson.json')
        c = RequestContext(request,{'obj':gt.instance})
        return HttpResponse(t.render(c))
    else:
        return HttpResponseForbidden()

def api_saveSettings(request):
    if request.user.is_authenticated():
        try:
            settings = Settings.objects.get(user=request.user)
        except:
            settings = Settings()
            settings.user = request.user
        
        form = SettingsForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            if form.cleaned_data['reminders']:
                settings.reminderDays = form.cleaned_data['reminderDays']
            else:
                settings.reminderDays = 0
            settings.defaultFB = form.cleaned_data['defaultFB']
            settings.defaultPublic = form.cleaned_data['defaultPublic']
            settings.save()
            return HttpResponse("Saved.") 
        else:
            return HttpResponse("Something broke.")
    else:
        return HttpResponseForbidden()

def api_updateAuthToken(request):
    if request.user.is_authenticated():
        profile = request.user.get_profile()
        access_token = request.POST['accessToken']
        profile.access_token = access_token
        profile.save()
        return HttpResponse("Updated.") 
        
    return HttpResponseForbidden()


### ACTUAL PAGES GO HERE
def index(request,username=None,inFb=False):

    if request.user.is_authenticated() or username is not None:
        
        import datetime
        if request.user.is_authenticated(): gtForm = GoodThingForm()
        else: gtForm = None
        
        #get some stats for the user
        if username is not None: 
            try:
                statsuser = User.objects.get(username=username)
            except:
                return HttpResponseNotFound("User not found.")
        else:
            #someone is looking at their homepage. let's make sure we have a current token.
            fb = django_facebook.api.get_persistent_graph(request)
            try: 
                trial = fb.get('me/friends')
            except:
                #no valid oauth token, get them to log in again.
                logout(request) 
                t = loader.get_template('index.html')
                c = RequestContext(request,{'inFb':inFb})
                return HttpResponse(t.render(c))
            
            statsuser = request.user
            #okay, so we should add some settings
            try:
                settings = Settings.objects.select_related().get(user=request.user)
            except:
                settings = Settings()
                settings.user = request.user
                settings.save()
            
            initial={'defaultFB': settings.defaultFB, 'defaultPublic': settings.defaultPublic}
            if settings.reminderDays != 0:
                initial['reminders']=True
                initial['reminderDays']=settings.reminderDays
            else: 
                initial['reminders'] = False;
            
            settingsForm = SettingsForm(initial=initial)
            
        gtcount = GoodThing.objects.filter(user=statsuser).filter(deleted=False).count()
        perday = float(gtcount)/max(((timezone.now() - statsuser.date_joined).days),1)
        
        if gtcount > 0:
            try:
                wc = WordClouds.objects.get(user=statsuser)
            except:
                wc = WordClouds()
                wc.user = statsuser
                wc.updateClouds()
        else: wc = None
        
        t = loader.get_template('myview.html')
        cdict = {'form':gtForm,'gtcount':gtcount,'perday':perday,'wc':wc,'inFb':inFb}
        if username is not None: cdict['viewuser'] = statsuser
        else:
            cdict['settings'] = settings
            cdict['settingsform'] = settingsForm
        
        c = RequestContext(request,cdict)
        
        return HttpResponse(t.render(c))
    #and if not, let's get them logged in
    
    else:
        #return HttpResponse(request.__str__())
        t = loader.get_template('index.html')
        c = RequestContext(request,{'inFb':inFb})
        return HttpResponse(t.render(c))

def privacy(request):
    t = loader.get_template('privacy.html')
    c = RequestContext(request,{})
    return HttpResponse(t.render(c))

def tos(request):
    t = loader.get_template('tos.html')
    c = RequestContext(request,{})
    return HttpResponse(t.render(c))
    
def gtview(request,username,gtid,inFb=False):
    try:
        gt = GoodThing.objects.select_related('user').get(id=gtid)
        
        if gt.user.username == username:
            if not gt.public and gt.user != request.user: return HttpResponseForbidden("Sorry, you don't have permission to view this content.")
        
            friendshtml = None
            if gt.friends:
                fb = django_facebook.api.get_facebook_graph(request)
                friendnames = []
                for friend in gt.friends.split(','):
                    try:
                        friendnames.append(fb.get(friend,fields='name')['name'])
                    except: 
                        pass
                friendshtml=", ".join(friendnames)
        
            t = loader.get_template('goodthing.html')
            c = RequestContext(request,{'gt':gt,'inFb':inFb,'initialCheer':False,'friends':friendshtml})

            if request.user.is_authenticated():
                try:
                    for cheer in gt.cheer_set.filter(user=request.user): c['initialCheer'] = True
                except:
                    pass
            
            return HttpResponse(t.render(c))

        return HttpResponseNotFound("Good thing not found.")
    except:
        return HttpResponseNotFound("Good thing not found.")

@csrf_exempt
def canvas(request):
    return index(request, username=None, inFb=True)
