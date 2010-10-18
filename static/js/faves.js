function init(screen_name, pages) {
	loadFaves(screen_name, pages);
	
	window.mtimeout = 3000;
	window.ptimeout = (5*pages);
	$("#progressbar").progressbar({ value: 0 });
	loading();
	ptimeout_id = setTimeout('updateProgress()', window.ptimeout);	
}

function loadFaves(screen_name, pages) {
	
	base_url =  "/faves/"+screen_name+"/"
	url = ""
	if (pages == 25) {
		url = base_url + "medium/"
	}
	else if (pages == 50) {
		url = base_url + "large/"
	}
	else if (pages == 100) {
		url = base_url + "xlarge/"
	}
	else {
		url = base_url + "small/"
	}
	
	$.ajax({
		type: "GET",
		url: url,
		data: "",
		success: function(data){
		    $("#data").html( data ).slideDown("slow");
			clearTimeout(ptimeout_id);
			$("#progressbar").hide().fadeOut("slow");
			$("#titlebar").show("slow").fadeIn("slow");
			$("#fave_deets").html( "* Faves between " + window.last_fave ).fadeIn("slow");
			$("#tweet_this_link").html(window.tweet_this_link)
		},
		error: function(data){
			clearTimeout(ptimeout_id);
			$("#progressbar").hide().fadeOut("slow");
		    $("#data").html( "<br/><br/><center><h1 class='title alt'>Oops! Something bad happened. Try, try again!</h1></center>" ).slideDown("slow");
		}
	});
}

function loading() {
	setLoadingMessage();
	timeout_id = setTimeout('loading()', window.mtimeout);
}

function updateProgress() {
	var progress;
	progress = $("#progressbar").progressbar("option","value");

	if (progress < 99) {
		$("#progressbar")
		.progressbar("option", "value", progress + 1);
		setTimeout(updateProgress, window.ptimeout);
	}

}

function setLoadingMessage() {
	var loading = new Array('Preparing unicorns for release...', 'Staring at Care Bears...', 'Sealing rainbows in Tupperware...', 'Preparing for inevitable butthurt...', 'Fitting Care Bears with stare-proof googles...', 'Securing all unicorns in spacepods...', 'Faving some dick jokes...', 'Mocking your tweets...', 'Obsessively refreshing Favrd...', 'Tumbling some LOLcats', 'Tweeting a Your Mom joke', 'Eating bacon', 'Tweeting about eating bacon', 'Running away with the circus...', 'Teaching old dogs new tricks...', 'Watching my stories...', 'Thinking up some clever status messages...', 'Hangin tough...', 'Diddling your sister...');
	var randomNum = Math.floor(Math.random() * loading.length);
	$('#status_message').html(loading[randomNum]);
}