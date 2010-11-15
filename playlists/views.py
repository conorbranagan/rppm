# Create your views here.
import re, urllib, datetime, json, random
from radioparadise.playlists.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponse

PREFIX = '/home/squid890/tmp/'
#PREFIX = ''

def scrape(request):
	# Download latest plays on RP to file
	url = "http://www.radioparadise.com/content.php?name=Playlist&more=true"
	u = urllib.URLopener()
	u.retrieve(url, PREFIX + 'output.html')
	
	# Parse the HTML using a couple regexs to get the latest songs - make sure to NOT include duplicates
	f = open(PREFIX + 'output.html', 'r')
	s = f.read()
	exp = '<tr class=\"n?o?shade\"><td>(.*[am|pm])</td><td><a href=\"content.php\?name=songinfo&song_id=[0-9]+\">(.*)<br>(.*)</a></td><td>.*border=\"0\">(.*)</a>.*</tr>'
	exp2 = '<tr class=\"n?o?shade\"><td>.*[am|pm]</td><td><a href=\"content.php\?name=songinfo&song_id=[0-9]+\">.*<br>.*</a></td><td>.*border=\"0\">.*</a>.*</tr>'	
	x = re.findall(exp2, s)
	x.reverse()
	for res in x:
		m = re.match(exp, res);
		time = m.group(1)
		# Parse time out into Python time object
		hour = int(time.split(':')[0])
		minute = int(time.split(':')[1].split(' ')[0])
		meridian = time.split(':')[1].split(' ')[1]
		if meridian == 'pm':
			hour += 12
		time = datetime.time(hour = int(hour), minute = int(minute))
		artist = m.group(2)
		title = m.group(3)
		album = m.group(4)
		
		# Load song information from iTunes music store API (JSON)
		itunes_url = 'http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStoreServices.woa/wa/wsSearch?term=' + urllib.quote(artist + ' ' + title + ' '+ album)
		try:
			song = Song.objects.get(play_time = time, artist = artist, title = title, album = album)
		except:
			u.retrieve(itunes_url, PREFIX + 'itunes_output.html')
			f = open(PREFIX + 'itunes_output.html', 'r')
		 	results = json.loads(f.read());
			if results['resultCount'] > 0:
				itunes_song = results['results'][0]
				itunes_url = itunes_song['trackViewUrl'].replace('http', 'itms')
				preview_url = itunes_song['previewUrl']
				albumart_url = itunes_song['artworkUrl100']
			else:
				itunes_song = None
				preview_url = None
				itunes_url = None
				albumart_url = None
			song = Song.objects.create(play_time = time, artist = artist, title = title, album = album, itunes_url = itunes_url, sample_url = preview_url, albumart_url = albumart_url)
	return HttpResponse("Successfully scraped data")

def index(request):	
	total = len(Song.objects.all())
	return render_to_response('main.html', {'total': total})
	
def listing(request, start, end):
	songs = Song.objects.all().order_by('-id')[start:end]
	return render_to_response('list.html', {'songs': songs})
	
def save(request):
	if request.method == 'POST':
		p = Playlist.objects.create(uid = base62_encode(random.randint(1, 1000000)))		
		song_ids = request.POST['song_ids'].split(',')
		song_ids = song_ids[0:len(song_ids) - 1]
		songs = Song.objects.filter(id__in = song_ids)
		for s in songs:
			p.songs.add(s)
			if len(s.artist) > 30:
				s.artist = s.artist[0:27] + '...'
			if len(s.title) > 30:
				s.title = s.title[0:27] + '...'
			if len(s.album) > 30:
				s.album = s.album[0:27] + '...'
		return HttpResponse(p.uid)
	return HttpResponse('error')

def saved(request, uid):
	if(uid != 'error'):
		playlist = Playlist.objects.get(uid = uid)
		songs = playlist.songs.all()
		for s in songs:
			if len(s.artist) > 28:
				s.artist = s.artist[0:25] + '...'
			if len(s.title) > 28:
				s.title = s.title[0:25] + '...'
			if len(s.album) > 28:
				s.album = s.album[0:25] + '...'
		return render_to_response('playlist.html', {'songs': songs})
	return HttpResponse('There was an error. Please go back and try again.')
	

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def base62_encode(num, alphabet=ALPHABET):
    """Encode a number in Base X

    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    """
    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)