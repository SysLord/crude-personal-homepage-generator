import sys
import glob
import re
import os



resultsDir = 'OUTPUT'
tenmplateFile = 'template.htm'

def applyGalleries(data):
	m = re.findall('<!-- gallery:(.*):(.*) -->', data)
	
	tmp = data	
	for x in m:
		tmp = applyGallery(tmp, x)
	
	return tmp;

def applyGallery(data, x):
	
	#m = re.search('<!-- gallery:(.*) -->', data)
	#if m is None:
	#	return data
	
	relativeDir, classSize = x
	print 'gallery: "{}"'.format(relativeDir)
	
	mediadir = "media" + "/" + relativeDir
	jpg = glob.glob(resultsDir + "/" + mediadir + "/*.jpg")
	png = glob.glob(resultsDir + "/" + mediadir + "/*.png")
	gif = glob.glob(resultsDir + "/" + mediadir + "/*.gif")	
	images = jpg + png + gif
	
	#for x in images:
	#	print x
	
	sizeformat = 'style="max-height:{0}px; max-width:{0}px;"'
	cssclassformat = 'class="{0}"'
	style = ''
	try:
		int(classSize)
		style = sizeformat.format(classSize)
	except:
		style = cssclassformat.format(classSize)
	
	imageFormat = """
	<a href="{0}">
		<img {1} src="{0}" />
	</a>
	"""
	
	imgs = map(lambda imagepath: imageFormat.format(mediadir + "/" + os.path.basename(imagepath), style), images)
	imgs.sort()
	
	format = """
	<div class="gallery">
		{}
	</div>
	"""	
	galleryHtml = format.format("\n".join(imgs))
		
	#return re.sub(r'<!-- gallery:(*) -->', galleryHtml, data)
	#return re.sub(r'<!-- gallery:_build/2013-10-27_dr_horrible_freezeray -->', galleryHtml.replace("\\", "\\\\"), data)
	return re.sub(r'<!-- gallery:' + relativeDir + ':(.*) -->', galleryHtml.replace("\\", "\\\\"), data)
	
	
def applyTeaseImages(data):
	m = re.findall('<!-- teaseimg:(.*):(.*) -->', data) #, re.DOTALL)

	#for x in m:
	#	print x
	
	tmp = data	
	for x in m:
	#	print x
		tmp = applyTeaseImg(tmp, x)
	
	return tmp;
	
	
def applyTeaseImg(data, m):
	
	pagename, imgIndexStr = m
	imgIndex = int(imgIndexStr)
	print 'teaseimg: "{}" {}'.format(pagename, imgIndex)

	outputPageContent = read(resultsDir + "/" + pagename)
	if outputPageContent is None:
		print "Not found {}".format(pagename)
		return data	
	
	imageUrl = getNthImage(outputPageContent, imgIndex)
	print 'tease image: "{}"'.format(imageUrl) 
		
	if imageUrl is None:
		return data	
	
	title = getTagContent(outputPageContent, "h1")
	imageFormat = """	
	<a href="{0}">
		<img class="teaseimg" src="{1}" />
	</a>
	<h3 class="teaseheader">
		<a href="{0}">
			{2}
		</a>
	</h3>
	"""

	bloghtml = imageFormat.format(pagename, imageUrl, title)

	return re.sub(r'<!-- teaseimg:' + pagename + ':(.*) -->', bloghtml.replace("\\", "\\\\"), data)

def getTagContent(pageContent, tagname):	
	m = re.search('<' + tagname + '>(.*)</' + tagname + '>', pageContent)
	if m is None:
		return "missing"
	
	return m.group(1)
	
def getNthImage(pageContent, index):	
	finds = re.findall('src="(.*)"', pageContent)

	if len(finds) <= index:
		print "getNthImage INDEX FEHLER"
		return None
	# Warum keine group?
	return finds[index] #.group(1)
		
def read(path):
	try:
		f = open(path)
		raw = f.read()
		f.close()
		return raw;
	except:
		return None
		
def parse(pagePath):
	f = open(pagePath)
	raw = f.read()
	f.close()
	
	#menu = parseMenuPath(raw)
	return pagePath, raw, None

def applyTemplate(page):
	f = open(tenmplateFile)
	raw = f.read()
	f.close()
	
	return re.sub(r'<!-- include:content -->', page, raw)	
	
def save(path, page):
	print path
	outputPath = re.sub(r'content_', 'OUTPUT/', path)
	print outputPath
	#print page
	f = open(outputPath, "w+")
	f.write(page)
	f.close()
	

pagePaths = glob.glob('content_*.htm')
print '{} pages'.format(len(pagePaths))

pathPageMenu = map(lambda x: parse(x), pagePaths)

for path, page, menu in pathPageMenu:
	result = applyTemplate(page)
	result = applyGalleries(result)
	result = applyTeaseImages(result)
	save(path, result)

# find menues
#menues = {}
#for path, page, menu in pathPageMenu:
#	cats = menu.split('/')	
#	menues[menu] = cats, path

#categoryPages = {}
#categories = []
# generate categories
#for menu, (cats, path) in menues.iteritems():
#	if len(cats) == 2:
#		newcat = cats[0]
#		if newcat not in categories:
#			categories.append(newcat)
#			categoryPages[newcat] = 
#		else:
				
#pages = {}
#for path, page, menu in pathPageMenu:
#	p = applyTemplate(page, menues)
	#save(p, path)

print "-- helo --"
