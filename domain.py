from __future__ import print_function
from PIL import Image
import colorsys
import os, sys, time
from dotsPlot import dotsPlot
from matplotlib.streamplot import DomainMap

'''
https://en.wikipedia.org/wiki/HSL_and_HSV#From_HSV
http://fourier.eng.hmc.edu/e161/lectures/ColorProcessing/node2.html
'''

'''
https://cate.blog/2013/08/26/extracting-the-dominant-color-from-an-image-in-processing/
https://cate.blog/about/
'''
def getDomainColor(allPixels, width, height):
	hueRange = 360;
	hues = [0 for z in range(hueRange)];
	#hues = [0];
	#print(len(hues));
	saturations = [0 for z in range(hueRange)];
	brightnesses = [0 for z in range(hueRange)];
	for x in range(width):
		for y in range(height):
				pixel = allPixels[x][y];				
				#print("x: ",x,"y: ", y," value: ", pixel);
				#time.sleep(2);
				hues[pixel[0]]+=1;
				saturations[pixel[0]] += pixel[1];
				brightnesses[pixel[0]] += pixel[2];
	
	maior = hues[0];
	hue = 0;
	cont = 0;
	for h  in hues:
		if(h > maior):
			maior = h; 
			hue = cont;
		cont+=1;
	
	h = hue;
	s = saturations[h]/maior;
	b = brightnesses[h]/maior;
	
	print("h: ",h,", com: ",maior," aparicoes");
	print("s: ",s);
	print("b: ",b);
	
	return [h, s, b];
	
'''
http://code.activestate.com/recipes/576919-python-rgb-and-hsv-conversion/
http://www.rapidtables.com/convert/color/rgb-to-hsv.htm
'''
def rgb2hsv(pixel):
	r = pixel[0];
	g = pixel[1];
	b = pixel[2];
	r, g, b = r/255.0, g/255.0, b/255.0
	mx = max(r, g, b)
	mn = min(r, g, b)
	df = mx-mn
	if mx == mn:
		h = 0
	elif mx == r:
		h = (60 * ((g-b)/df) + 360) % 360
	elif mx == g:
		h = (60 * ((b-r)/df) + 120) % 360
	elif mx == b:
		h = (60 * ((r-g)/df) + 240) % 360	
	if mx == 0:
	    s = 0
	else:
	    s = df/mx
	v = mx
	
	#formatando
	h = int(round(h));
	if(h==360):
		h=0;
	s = s*100;
	v = v*100;
	#s = int(round(s*100));
	#v = int(round(v*100));
	#print("HSV ",[h, s, v]);	
	#time.sleep(2);
	#return h, s, v;
	return [h, s, v];

'''
http://www.rapidtables.com/convert/color/hsv-to-rgb.htm
'''
def hsv2rgb(pixel):
	h = pixel[0];
	s = pixel[1];
	v = pixel[2];
	
	c = v*s;
	x = c*(1 - abs(((h/60)%2)-1) );
	m = v-c;
	
	r1 = g1 = b1 = 0;
	if(h < 60):
		r1 = c;
		g1 = x;
		b1 = 0;
	elif(h < 120):
		r1 = x;
		g1 = c;
		b1 = 0;
	elif(h < 180):
		r1 = 0;
		g1 = c;
		b1 = x;	
	elif(h < 240):
		r1 = 0;
		g1 = x;
		b1 = c;
	elif(h < 300):
		r1 = x;
		g1 = 0;
		b1 = c;	
	elif(h < 360):
		r1 = c;
		g1 = 0;
		b1 = x;	
	
	r = (r1+m)*255;
	g = (g1+m)*255;
	b = (b1+m)*255;
	
	return [r, g, b];
			
'''
http://www.rapidtables.com/convert/color/rgb-to-hsl.htm
'''
def rgb2hsl(pixel):
	r = pixel[0];
	g = pixel[1];
	b = pixel[2];
	r, g, b = r/255.0, g/255.0, b/255.0
	mx = max(r, g, b)
	mn = min(r, g, b)
	df = mx-mn
	if mx == mn:
		h = 0
	elif mx == r:
		h = (60 * ((g-b)/df) + 360) % 360
	elif mx == g:
		h = (60 * ((b-r)/df) + 120) % 360
	elif mx == b:
		h = (60 * ((r-g)/df) + 240) % 360	
	if mx == 0:
	    s = 0
	else:
	    s = df/mx
	l = (mx+mn)/2;
	
	#formatando
	h = int(round(h));
	if(h==360):
		h=0;
	s = s*100;
	l = l*100;
	#s = int(round(s*100));
	#v = int(round(v*100));
	#print("HSL ",[h, s, l]);	
	time.sleep(2);
	return h, s, l;


'''
http://fourier.eng.hmc.edu/e161/lectures/ColorProcessing/node2.html
'''
def rgb2hsi(pixel):
	r = pixel[0];
	g = pixel[1];
	b = pixel[2];
	r, g, b = r/255.0, g/255.0, b/255.0
	mx = max(r, g, b)
	mn = min(r, g, b)
	df = mx-mn
	if mx == mn:
		h = 0
	elif mx == r:
		h = (60 * ((g-b)/df) + 360) % 360
	elif mx == g:
		h = (60 * ((b-r)/df) + 120) % 360
	elif mx == b:
		h = (60 * ((r-g)/df) + 240) % 360	
	if mx == 0:
	    s = 0
	else:
	    s = df/mx
	i = (pixel[0]+pixel[1]+pixel[2])/3;
	
	#formatando
	h = int(round(h));
	if(h==360):
		h=0;
	s = s*100;
	i = i*100;
	#s = int(round(s*100));
	#v = int(round(v*100));
	print("HSI ",[h, s, i]);	
	#time.sleep(2);
	return h, s, i;


'''
http://www.easyrgb.com/en/math.php#text2
'''
def rgb2xyz(pixel):
	r = pixel[0]/255;
	g = pixel[1]/255;
	b = pixel[2]/255;
	
	if(r > 0.04045):
		r = ( (r+0.055) / 1.055 ) ** 2.4;
	else:
		r = r/12.92;
	if(g > 0.04045):
		g = ( (g+0.055) / 1.055 ) ** 2.4;
	else:
		g = g/12.92;
	if(b > 0.04045):
		b = ( (b+0.055) / 1.055 ) ** 2.4;
	else:
		b = b/12.92;

	r = r*100;
	g = g*100;
	b = b*100;

	x = r*0.4124 + g*0.3576 + b*0.1805
	y = r*0.2126 + g*0.7152 + b*0.0722
	z = r*0.0193 + g*0.1192 + b*0.9505
	
	return [x,y,z];

'''
http://www.easyrgb.com/en/math.php#text9
https://gist.github.com/manojpandey/f5ece715132c572c80421febebaf66ae
'''
def xyz2cieLab(pixel):
	x = pixel[0]/95.047;#reference x
	y = pixel[1]/100.0;#reference y
	z = pixel[2]/108.883;#reference z
	
	if(x > 0.008856):
		x = x ** (1/3);
	else:
		x = (7.787*x) + (16/116);
	if(y>0.008856):
		y = y ** (1/3);
	else:
		y = (7.787*y) + (16/116);
	if(z > 0.008856):
		z = z ** (1/3);
	else:
		z = (7.787*z) + (16/116);

	l = (116*y) - 16;
	a = 500 * (x - y);
	b = 200 * (y - z);
	
	return [l, a ,b];
	
def rgb2cieLab(pixel):
	p1 = rgb2xyz(pixel);
	p2 = xyz2cieLab(p1);
	return p2;


def HSVColor(subdir, img):	
	img = Image.open(subdir+"/"+img);
	if isinstance(img ,Image.Image):		
		#print(img);
		#img = img.convert('HSV');

		pix = img.load();
		
		print("tamanho em pixels",img.size);
		time.sleep(2);
		width, height = img.size;
		#all_pixels[width][height];
		all_pixels= [[[0 for z in range(3)] for x in range(height)] for y in range(width)]; 
		#line = [];
		x=0; y =0;
		for x in range(width):
			for y in range(height):
				cpixel = pix[x, y];
				#print("RGB ",cpixel);				
				#rgb2hsv(cpixel)
				a = rgb2hsv(cpixel);
				#print(a);
				#all_pixels.append(a);		
		 		all_pixels[x][y] = a;
		 		#print("x: ",x,"y: ", y," value: ", a);
		 		#line.append(a);
         	#all_pixels.append(line);
		
		#print("tamanho em HSV ",len(all_pixels));
		#time.sleep(2);
		domainColor = getDomainColor(all_pixels, width, height);
		return domainColor;
			
title = "DomainColor";
xTitle = "Sample";
yTitle = "Hue value";
dots = dotsPlot(title, xTitle, yTitle);
cont = 1;
for subdir, dirs, files in os.walk('./Images/'):
	group = subdir;
	x = [];
	y = [];
	print(subdir)
	for file in files:
		print(file);
		domainColor = HSVColor(subdir, file);
		#dots.addDot(cont, domainColor[0], group);
		#cont+=1;
		y.append(domainColor[0]);
		x.append(cont);
		cont+=1;
	if(len(x) != 0):
		dots.addDot2(x, y, group);
		cont+=1;
	
dots.plot();



#r, g, b = im.split()
#im = Image.merge("RGB", (b, g, r))