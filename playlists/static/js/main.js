$(document).ready(function() {
	var id_string = '', row_color = 'white', cur_start = 0, cur_end = 10;
	$.get('/list/0/10', function(data){
		$('#songListing').html(data);
	});
	$('.addToPlaylist').live('click', function() {
		var goingToNext = false;
		id_string += $(this).parent().attr('id') + ',';
		artist = $(this).parent().find('.artist').text();
		title = $(this).parent().find('.title').text();
		album = $(this).parent().find('.album').text();		
		if (artist.length > 32) artist = artist.substring(0, 28) + '...';	
		if (title.length > 32) title = title.substring(0, 28) + '...';	
		if (album.length > 32) album = album.substring(0, 28) + '...';	

		var myRow = '<ul style = "background-color: ' + row_color + '">';
		myRow += '<li class = "title">' + title + '</li>';
		myRow += '<li class = "artist">' + artist + '</li>';
		myRow += '<li class = "album">' + album + '</li>';
		myRow += '</ul>';
		$(this).parent().slideUp(function() {
			if($(this).parent().find('.songItem').size() == 1) {
				goingToNext = true;
			}
			$(this).remove();
			if(goingToNext) {
				goToNext();
			}
		});
		$("#currentPlaylist").append(myRow); 
		if(row_color == 'white') row_color = 'lightGrey';
		else row_color = 'white';
		return false;
	})

	$('.next').click(function() {
		if(!$(this).attr('href') || $(this).attr('href') == '') {
			return;
		}
		goToNext();
	});

	$('.prev').click(function() {
		if(!$(this).attr('href') || $(this).attr('href') == '') {
			return;
		}
		$('#songListing').html('<div class = "loader"><img src = "/static/img/loader.gif" /></div>');			
		cur_start -= 10;
		cur_end -= 10;
		$.get('/list/' + cur_start + '/' + cur_end, function(data){
			$('#songListing').html(data);
		});
		if(cur_start == 0) {
			$('.nextPrevArea .prev').removeAttr('href');
		}
		if(cur_end < total) {
			$('.nextPrevArea .next').attr('href', '#');
		}
	});

	$('#savePlaylist').click(function() {
		if(id_string == '') {
			alert('You haven\'t added any songs yet');
			return;
		}			
		$.post('/save/', {'song_ids': id_string}, function(data) {
			window.location.href = "/playlist/" + data + "/";
		})
	})

	function goToNext() {
		$('#songListing').html('<div class = "loader"><img src = "/static/img/loader.gif" /></div>');
		cur_start += 10;
		cur_end += 10;
		$.get('/list/' + cur_start + '/' + cur_end, function(data){
			$('#songListing').html(data);
		});
		if(cur_end >= total) {
			$('.nextPrevArea .next').removeAttr('href');
		}
		if(cur_start >= 0) {
			$('.nextPrevArea .prev').attr('href', '#');
		}		
	}

});
