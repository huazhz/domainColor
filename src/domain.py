from __future__ import print_function;
from skimage import color, data, novice;
import os, sys, time, csv;
from src.model.easyPlot import dotsPlot2D, dotsPlot3D, histogram;
from src.model.imageData import imageData;
import numpy as np;

'''
https://en.wikipedia.org/wiki/HSL_and_HSV#From_HSV
http://fourier.eng.hmc.edu/e161/lectures/ColorProcessing/node2.html
'''

'''
https://cate.blog/2013/08/26/extracting-the-dominant-color-from-an-image-in-processing/
https://cate.blog/about/
'''
hues = []
def getDomainColor(allPixels, width, height):
	hueRange = 360;
	hues = [0 for z in range(hueRange)];
	#hues = [0];
	#print(len(hues));
	saturations = [0 for z in range(hueRange)];
	brightnesses = [0 for z in range(hueRange)];
	
	for x in range(width):
		for y in range(height):
				#print("x: ",x,"y: ", y," value: ", allPixels[x][y]);
				pixel = allPixels[x][y];								
				#time.sleep(2);
				hues[int(pixel[0])]+=1;
				saturations[int(pixel[0])] += pixel[1];
				brightnesses[int(pixel[0])] += pixel[2];
	print(hues)
	'''
	for pixel in allPixels:
		hues[int(pixel[0])]+=1;
		saturations[int(pixel[0])] += pixel[1];
		brightnesses[int(pixel[0])] += pixel[2];
	'''
	maior = hues[0];
	hue = 0;
	cont = 0;
	for h  in hues:
		if(h > maior):
			maior = h; 
			hue = cont;
		cont+=1;
	
	h = hue;
	#s = saturations[h]/maior;
	#b = brightnesses[h]/maior;
	s = (saturations[h]/maior)*100;
	b = (brightnesses[h]/maior)*100;
	
	print("h: ",h,", com: ",maior," aparicoes");
	print("s: ",s);
	print("b: ",b);
	
	return [h, s, b], maior;


def HSVColor(file):	
	img = data.load(file, as_grey = False);
	#exposure.histogram(img);
	picture = novice.open(file);
	
	height, width = picture.size;	
	print("tamanho em pixels: ",picture.size);		
	hsvImage = color.rgb2hsv(img);	
	#hsvImage = color.rgb2hsv(picture);
	#hsvImage = color.convert_colorspace(img, 'RGB', 'HSV');
	domainColor, numApp = getDomainColor(hsvImage, width, height);
	imgData = imageData(file, img.size);
	imgData.setDomainColor(domainColor, numApp);
	return imgData;


def rgbHistogram(name, file):	
	picture = novice.open(file);	

	z = [x for x in range(256)];
	red = [0 for x in range(256)];
	green = [0 for x in range(256)];
	blue = [0 for x in range(256)];
	for pixel in picture:
		red[pixel.red]+=1;
		green[pixel.green]+=1;
		blue[pixel.blue]+=1;	
	name  = "..\\histograms\\hist_"+name
	histogram(name, file, "RGB histogram", "RGB range", "Value",
			 red, green, blue, z);


def histogramColor():
	startTime = time.time();
	for subdir, dirs, files in os.walk(os.path.abspath(os.path.join('.\\', os.pardir))+'\\Images\\'):
		group = subdir;		
		print(subdir.split("\\")[-1])
		print(subdir);
		for file in files:
			print("\t",file);
			name = file;
			file = subdir+"\\"+file
			rgbHistogram(name, file);									
	elapsedTime = time.time() - startTime;
	print("FINISH, ELAPSED TIME(seconds): ",elapsedTime);		


def domainColor2D():
	title = "DomainColor";
	xTitle = "Sample";
	yTitle = "Hue value";
	dots = dotsPlot2D(title, xTitle, yTitle);
	
	outFile = open("..\\output2d.csv", "w");
	writer = csv.writer(outFile, delimiter=',', quotechar=' ', quoting=csv.QUOTE_ALL);
	writer.writerow(["NAME;DOMAIN COLOR; NUMBER OF APPARITIONS; SIZE IN PIXELS"]);
	startTime = time.time();
	cont = 1;
	for subdir, dirs, files in os.walk(os.path.abspath(os.path.join('.\\', os.pardir))+'\\Images\\'):
		group = subdir;		
		x = [];
		y = [];		
		imgData = [];
		print(subdir)
		
		for file in files:
			print("\t",file);
			file = subdir+"\\"+file	
			i = HSVColor(file);
			imgData.append(i);
			x.append(cont);
			y.append(i.domainColor[0]);
			cont+=1;					
		
		if(len(x) != 0):		
			dots.addDot(x, y, group);						
			for im in imgData:
				writer.writerow([im]);			
	outFile.close();
	elapsedTime = time.time() - startTime;
	print("FINISH, ELAPSED TIME(seconds): ",elapsedTime);
	
	dots.plot();



def domainColor3D():	
	title = "DomainColor";
	xTitle = "x - Hue value";
	yTitle = "y - Saturation";
	zTitle = "z - Value";
	dots = dotsPlot3D(title, xTitle, yTitle, zTitle);

	outFile = open("output.csv", "w");
	writer = csv.writer(outFile, delimiter=',', quotechar=' ', quoting=csv.QUOTE_ALL);
	writer.writerow(["NAME;DOMAIN COLOR; NUMBER OF APPARITIONS; SIZE IN PIXELS"]);
	startTime = time.time();
	cont = 1;
	for subdir, dirs, files in os.walk(os.path.abspath(os.path.join('.\\', os.pardir))+'\\Images\\'):
		group = subdir;	
		x = [];
		y = [];
		z = [];
		imgData = [];
		print(subdir)
		for file in files:
			print("\t",file);				
			file = subdir+"\\"+file	
			i = HSVColor(file);
			imgData.append(i);			
			x.append(i.domainColor[0]);
			y.append(i.domainColor[1]);
			z.append(i.domainColor[2]);					
		
		if(len(x) != 0):			
			dots.addDot(x, y, z, group);
			for im in imgData:
				writer.writerow([im]);
	outFile.close();
	elapsedTime = time.time() - startTime;
	print("FINISH, ELAPSED TIME(seconds): ",elapsedTime);
	dots.plot();	
	
def calculateAll():
	startTime = time.time();
	outFile = open("..\\outputRGB.csv", "w",newline='');
	writer = csv.writer(outFile, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL);
	writer.writerow(["GROUP;NAME;R(AVARAGE);G(AVARAGE);B(AVARAGE);R(MEDIAN);G(MEDIAN);B(MEDIAN);R(MODE);G(MODE);B(MODE)"]);
	for subdir, dirs, files in os.walk(os.path.abspath(os.path.join('.\\', os.pardir))+'\\Images\\'):
		group = subdir.split("\\")[-1];
		print(subdir);
		for file in files:
			print("\t",file);
			name = file;
			file = subdir+"\\"+file
			rgbAva, rgbMed, rgbMode = calculeRGBHistogram(file);
			print("rgbAvarage ", rgbAva);
			print("rgbMedian ", rgbMed);
			print("rgbMode ", rgbMode);
			#time.sleep(10);
			row = str(str(group)+";"+str(name)+";"+str(rgbAva[0])+";"+str(rgbAva[1])+";"+str(rgbAva[2])+";"+str(rgbMed[0])+";"+str(rgbMed[1])+";"+str(rgbMed[2])+";"+str(rgbMode[0])+";"+str(rgbMode[1])+";"+str(rgbMode[2]));
			writer.writerow([row]);
										
	elapsedTime = time.time() - startTime;
	outFile.close();
	print("FINISH, ELAPSED TIME(seconds): ",elapsedTime);
	
	
def calculeRGBHistogram(file):
	picture = novice.open(file);
	height, width = picture.size;
	red = [0 for x in range(256)];
	green = [0 for x in range(256)];
	blue = [0 for x in range(256)];
	for pixel in picture:
		red[pixel.red]+=1;
		green[pixel.green]+=1;
		blue[pixel.blue]+=1;	
	#mode of RGB
	rgbMode = [getBigger(red), getBigger(green), getBigger(blue)];	
	#median of RGB
	red.sort();
	green.sort();
	blue.sort();
	half = height*width/2;
	rgbMed = rgbMedian(half, red, green, blue);	
	#avarage of RGB
	rgbAva = rgbAvarage(picture, height, width);
	
	return rgbAva, rgbMed, rgbMode; 


def getBigger(vector):
	bigger = vector[0];
	position = 0;
	cont = 0;
	for cont in range(len(vector)):
		if(vector[cont] > bigger):
			bigger = vector[cont];
			position = cont;
		cont+=1;
	return position;


def rgbAvarage(picture, height, width):
	rAvarage = 0;
	gAvarage = 0;
	bAvarage = 0;
	for i in range(height):
		for j in range(width):
			pixel = picture[i,j];
			rAvarage+= pixel.red;
			gAvarage+= pixel.green;
			bAvarage+= pixel.blue;
		rAvarage/=height;
		gAvarage/=height;
		bAvarage/=height;		
	return [int(rAvarage), int(gAvarage), int(bAvarage)];


def rgbMedian(half, red, green, blue):
	cont = 0;
	i = 0;
	while(cont < half):
		cont+=red[i];
		i+=1;
	rMedian = i;
	cont = 0;
	i = 0;
	while(cont < half):
		cont+=red[i];
		i+=1;
	gMedian = i;	
	cont = 0;
	i = 0;
	while(cont < half):
		cont+=red[i];
		i+=1;
	bMedian = i;		
	return [rMedian, gMedian, bMedian];


#domainColor2D();
#domainColor3D();
#histogramColor();
calculateAll();





