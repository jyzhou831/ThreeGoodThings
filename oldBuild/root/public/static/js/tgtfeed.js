// Scroll globals
var	pageNum = 0, // The latest page loaded
	hasNextPage = true, // Indicates whether to expect another page after this one
	baseUrl = '/api/things/', // The root for the JSON calls
	loadOnScroll = function() {
	   // If the current scroll position is past out cutoff point...
	    if ($(window).scrollTop() > $(document).height() - ($(window).height()*3)) {
	        // temporarily unhook the scroll event watcher so we don't call a bunch of times in a row
	        $(window).unbind();
	        // execute the load function below that will visit the JSON feed and stuff data into the HTML
	        loadItems();
	    }
	},

	
	myGoodThingTemplateMarkup = "<li class='media myGoodThing'><a class='pull-left' style='margin-right:0px' href='/user/${username}/'><img class='media-object' src='http://graph.facebook.com/${fbuid}/picture?type=square' alt='${user}'></a><a class='pull-left' href='#' style='margin-left:2px; margin-right:0px; padding-top:10px'><i class='right-caret'></i></a><div class='media-body'><div class='well' style='padding-bottom:5px'><div class='name'><a href='#' title='${id}' class='delete'>delete</a><h4 class='media-heading'>${user}</h4></div><div class='gtcontent'>${goodThing}</div><div class='control'><h6>${reason}<i class='icon-lock'></i></h6>${postedreadable} &middot; <span class='commentcount'><a href='/user/${username}/${id}' class='link'><fb:comments-count href='http://www.threegthings.net/user/${username}/${id}'></fb:comments-count></a></span> &middot; <span class='cheercount'>${cheers} cheers</span> </a></div></div></div></li>";
	GoodThingTemplateMarkup = "<li class='media GoodThing'><a class='pull-left' style='margin-right:0px' href='/user/${username}/'><img class='media-object' src='http://graph.facebook.com/${fbuid}/picture?type=square' alt='${user}'></a><a class='pull-left' href='#' style='margin-left:2px; margin-right:0px; padding-top:10px'><i class='right-caret'></i></a><div class='media-body'><div class='well' style='padding-bottom:5px'><div class='name'><h4 class='media-heading'>${user}</h4></div><div class='gtcontent'>${goodThing}</div><div class='control'>${postedreadable} &middot; <span class='commentcount'><a href='/user/${username}/${id}' class='link'><fb:comments-count href='http://www.threegthings.net/user/${username}/${id}'></fb:comments-count></a></span> &middot; <a id='${uncheer}cheer${id}' class='${uncheer}cheer' href='#posted${id}' title='${id}'>${uncheer}cheer</a> alongside <span class='cheercount'><span id='cheers${id}'>${cheers}</span></span> others</a></div></div></div></li>";
	LoggedOutGoodThingTemplateMarkup = "<li class='media GoodThing'><a class='pull-left' style='margin-right:0px' href='/user/${username}/'><img class='media-object' src='http://graph.facebook.com/${fbuid}/picture?type=square' alt='${user}'></a><a class='pull-left' href='#' style='margin-left:2px; margin-right:0px; padding-top:10px'><i class='right-caret'></i></a><div class='media-body'><div class='well' style='padding-bottom:5px'><div class='name'><h4 class='media-heading'>${user}</h4></div><div class='gtcontent'>${goodThing}</div><div class='control'>${postedreadable} &middot; <span class='commentcount'><a href='/user/${username}/${id}' class='link'><fb:comments-count href='http://www.threegthings.net/user/${username}/${id}'></fb:comments-count></a></span> &middot; <span class='cheercount'><span id='cheers${id}'>${cheers}</span></span> cheers</a></div></div></div></li>";

myGoodThingPrivateTemplateMarkup = "<li class='media myGoodThing'><a class='pull-left' style='margin-right:0px' href='/user/${username}/'><img class='media-object' src='http://graph.facebook.com/${fbuid}/picture?type=square' alt='${user}'/></a><a class='pull-left' href='#' style='margin-left:2px; margin-right:0px; padding-top:10px'><i class='right-caret'></i></a><div class='media-body'><div class='well' style='padding-bottom:5px'><div class='name'><h4 class='media-heading'>${user}</h4></div><div class='gtcontent'>${goodThing}<i class='icon-lock'></i></div><div class='control'><h6>${reason}<i class='icon-lock'></i></h6>${postedreadable} </div></div></div></div></li>";
	
	singleUserThingTemplateMarkup = "<div class='singleUserGoodThing'><a class='posted' href='/user/${username}/${id}' title='${posted}'>${postedreadable}</a><div class='gt'>${goodThing}</div><div class='metadata'><span class='cheercount'><span id='cheers${id}'>${cheers}</span> cheers <span class='cheerlink'>(<a id='${uncheer}cheer${id}' class='${uncheer}cheer' href='#' title='${id}'>${uncheer}Cheer</a>)</span></span><span class='commentcount'><a href='/user/${username}/${id}'><fb:comments-count href='http://www.threegthings.net/user/${username}/${id}'></fb:comments-count></a></span></div></div></div>";
	
	
$.template("myGoodThingTemplate",myGoodThingTemplateMarkup);
$.template("myGoodThingPrivateTemplate",myGoodThingPrivateTemplateMarkup);
$.template("GoodThingTemplate",GoodThingTemplateMarkup);
$.template("singleUserThingTemplate",singleUserThingTemplateMarkup);
$.template("LoggedOutGoodThingTemplate",LoggedOutGoodThingTemplateMarkup);

function updateFeed(){
	$("a.posted").each(function(index) {
	    $(this).html(relativeDate($(this).attr("title")));
	});
};

function renderGoodThing(item){
	item['postedreadable'] = relativeDate(item['posted']);
	
	if (feedSelector != ''){
		return $.tmpl("singleUserThingTemplate", [item]);
	}else if (uid == -1){
	    return $.tmpl("LoggedOutGoodThingTemplate",[item]);
	}else{
		if (item['public'] == true) {item['publicreadable'] = "Public";}else{item['publicreadable'] = "Private";};
		if (item['uid'] == uid){
			if (item['publicreadable'] != "Public"){
				return $.tmpl("myGoodThingPrivateTemplate", [item]);
			}else{
				return $.tmpl("myGoodThingTemplate", [item]);
			};
		}else{
			return $.tmpl("GoodThingTemplate", [item]);
		};	
	};
};

function loadItems() {
    // If the next page doesn't exist, just quit now 
    if (hasNextPage === false) { return false; }
    pageNum = pageNum + 1;
    // Configure the url we're about to hit
    var url = baseUrl + "?page=" + pageNum + feedSelector;
    $.ajax({
        url: url,
        dataType: 'json',
        success: function(data) {
            // Update global next page variable
            hasNextPage = data.hasNext;
            $.each(data.itemList, function(index, item){
				renderGoodThing(item).appendTo("#goodThingsList");
            });
        },
        complete: function(data, textStatus){
			$(".myGoodThing").hover(function(){$(this).children('.tgtcontrols').children('.delete').fadeIn(150);},function(){$(this).children('.tgtcontrols').children('.delete').fadeOut(150);});
			if ($('#filter_you').hasClass('filter_selected')){filterYou();}
			FB.XFBML.parse();
			// Turn the scroll monitor back on
            $(window).bind('scroll', loadOnScroll);		
        }
    });
};

function tgtDocumentReady(){
	loadItems();     
   	$(window).bind('scroll', loadOnScroll);	
	$(document).on("click", "a.delete", function(){
		$.post('/api/delete',{ gtid: $(this).attr('title'), csrfmiddlewaretoken: csrfmiddlewaretoken });
		$( this ).parents(".myGoodThing").hide(300,function(){$( this ).remove();});
		$('#gtcount').html(Number($('#gtcount').html())-1);		
	}); 
	$(document).on("click", "a.cheer", function(){
		$.post('/api/cheer',{ gtid: $(this).attr('title'), csrfmiddlewaretoken: csrfmiddlewaretoken },function(data){$('#cheer'+data).replaceWith('<a id="uncheer'+data+'" class="uncheer" href="#" title="'+data+'">unCheer</a>');$('#cheers'+data).html(parseInt($('#cheers'+data).html())+1);});
	});	
	$(document).on("click", "a.uncheer", function(){
		$.post('/api/uncheer',{ gtid: $(this).attr('title'), csrfmiddlewaretoken: csrfmiddlewaretoken },function(data){$('#uncheer'+data).replaceWith('<a id="cheer'+data+'" class="cheer" href="#" title="'+data+'">Cheer</a>');$('#cheers'+data).html(parseInt($('#cheers'+data).html())-1);});
	});
	setInterval("updateFeed()",5000);
};