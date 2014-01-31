from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django_facebook.api import get_facebook_graph
from time import sleep

stopwords = "a,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your,yesterday,today".split(',')

class GoodThing(models.Model):
    goodThing = models.CharField("Good thing",max_length=200);
    reason = models.CharField("reason",max_length=200,blank=True,default=None)
    posted = models.DateTimeField(auto_now_add=True,editable=False)
    user = models.ForeignKey(User,editable=False)
    friends = models.CommaSeparatedIntegerField(max_length=128,blank=True,default=None)
    public = models.BooleanField(default=True,help_text="Make public within 3GT")
    wall = models.BooleanField(default=False,help_text="Post to Facebook NewsFeed")
    fbid = models.CharField(max_length=100,blank=True,default=None,editable=False)
    deleted = models.BooleanField(default=False,editable=False)
    
    def link(self):
        return "https://www.threegthings.net/user/"+self.user.username+"/"+str(self.id)
     
    def postFB(self,fb=None,useog=True):
        #new one with actions
        try:
            if useog:
                rdata = fb.set('me/threegoodthings:celebrate',good_thing=self.link(),tags=self.friends,scrape=True,explicitly_shared=True) 
            else:
                #if it's not set to use open graph, go ahead and use the old method.
                rdata = fb.set('me/feed', message=self.goodThing, link=self.link(), name=self.user.first_name + " celebrated a Good Thing!")
            self.fbid = rdata['id']
            self.save()
        except:
            pass
            
    def fbLink(self):
        if self.fbid == None: return False
        else:
            if len(self.fbid.split("_")) > 1:
                pid = self.fbid.split("_")[1]
                if self.user.username: return "http://facebook.com/%s/posts/%s"%(self.user.username,pid)
                else: return "http://www.facebook.com/permalink.php?id=%s&v=wall&story_fbid=%s"%(self.user.get_profile().facebook_id,pid)        
            else:
                if self.user.username: return "http://facebook.com/%s/activity/%s"%(self.user.username,self.fbid)
                else: return False

class Cheer(models.Model):
    user = models.ForeignKey(User)
    goodThing = models.ForeignKey(GoodThing)
    cheered = models.DateTimeField(auto_now_add=True)

class Settings(models.Model):
    user = models.ForeignKey(User)
    twitterHandle = models.CharField(max_length=24,blank=True,default=None)
    reminderDays = models.IntegerField(default=0)
    defaultFB = models.BooleanField(default=False)
    defaultPublic = models.BooleanField(default=True)

class WordClouds(models.Model):
        user = models.ForeignKey(User,editable=False,unique=True)
        rCloudPublic = models.TextField(blank=True)
        rCloudPrivate = models.TextField(blank=True)
        gtCloudPublic = models.TextField(blank=True)
        gtCloudPrivate = models.TextField(blank=True)
        
        def wordCloud(self,sources):
            words = []
            maxlength = 20
            
            for source in sources: words.extend(source.lower().split())
            from collections import defaultdict
            import operator
            d = defaultdict(int)
            for word in [w for w in words if not w in stopwords]: d[word] += 1
            counts = sorted(d.iteritems(), key=operator.itemgetter(1), reverse=True)
            if len(counts) > 0:
                del counts[maxlength:]
                minct = float(counts[-1][1])
                diff = max((counts[0][1]-minct),1.0)
                counts.sort()
                cloud = ["<span class='size%s'>%s</span>"%(int((wc[1]-minct)/diff*10),wc[0]) for wc in counts]
                
                return " ".join(cloud)
            return ''
            
        def updateClouds(self):
            import string
            
            tostrip="/\"?.\\<>,;:()*&^$#@!"
            punctuation = string.maketrans(tostrip," "*len(tostrip)).decode("latin-1")
            
            goodThings = GoodThing.objects.filter(deleted=False).filter(user=self.user)
            self.gtCloudPrivate = self.wordCloud([gt.goodThing.translate(punctuation) for gt in goodThings])
            reasons = [gt.reason.translate(punctuation) for gt in goodThings if gt.reason is not None]
            if len(reasons) > 0: self.rCloudPrivate = self.wordCloud(reasons)
            else: self.rCloudPrivate = ""
            
            goodThings = goodThings.filter(public=True)
            self.gtCloudPublic = self.wordCloud([gt.goodThing.translate(punctuation) for gt in goodThings])
            #self.rCloudPublic = self.wordCloud([gt.reason.translate(punctuation) for gt in goodThings])
            self.rCloudPublic = ""
        
            self.save()
            
            
