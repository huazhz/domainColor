from __future__ import print_function;
from skimage import color, io;
import os, sys, time, csv;
from src.model.easyPlot import dotsPlot2D, dotsPlot3D, histogram;
from src.model.imageData import imageData;
from matplotlib import pyplot as plt;
from matplotlib import ticker
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
	img = io.imread(file);
	height, width = len(img), len(img[0]);	
	
	print("tamanho em pixels: ", height, width);		
	hsvImage = color.rgb2hsv(img);
	#hsvImage = color.rgb2hsv(picture);
	#hsvImage = color.convert_colorspace(img, 'RGB', 'HSV');
	domainColor, numApp = getDomainColor(hsvImage, width, height);
	imgData = imageData(file, img.size);
	imgData.setDomainColor(domainColor, numApp);
	return imgData;


def rgbHistogram(name, file):	
	img = io.imread(file);
	height, width = len(img), len(img[0]);	

	z = [x for x in range(256)];
	red = [0 for x in range(256)];
	green = [0 for x in range(256)];
	blue = [0 for x in range(256)];
	for i in range(height):
		for j in range(width):
			pixel = img[i, j];
			red[pixel[0]]+=1;
			green[pixel[1]]+=1;
			blue[pixel[2]]+=1;	
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


def calculateHSV():
	startTime = time.time();
	outFile = open("..\\outputHSV.csv", "w",newline='');
	writer = csv.writer(outFile, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL);
	writer.writerow(["GROUP;NAME;H(AVARAGE);S(AVARAGE);V(AVARAGE);H(MEDIAN);S(MEDIAN);V(MEDIAN);H(MODE);S(MODE);V(MODE)"]);
	for subdir, dirs, files in os.walk(os.path.abspath(os.path.join('.\\', os.pardir))+'\\Images\\'):
		group = subdir.split("\\")[-1];
		print(subdir);
		for file in files:
			print("\t",file);
			name = file;
			file = subdir+"\\"+file
			hsvAva, hsvMed, hsvMode = calculeHSVHistogram(file);
			print("hsvAvarage ", hsvAva);
			print("hsvMedian ", hsvMed);
			print("hsvMode ", hsvMode);
			#time.sleep(10);
			row = str(str(group)+";"+str(name)+";"+str(hsvAva[0])+";"+str(hsvAva[1])+";"+str(hsvAva[2])+";"+str(hsvMed[0])+";"+str(hsvMed[1])+";"+str(hsvMed[2])+";"+str(hsvMode[0])+";"+str(hsvMode[1])+";"+str(hsvMode[2]));
			writer.writerow([row]);
										
	elapsedTime = time.time() - startTime;
	outFile.close();
	print("FINISH, ELAPSED TIME(seconds): ",elapsedTime);


def calculeHSVHistogram(file):
	img = io.imread(file);
	height, width = len(img), len(img[0]);		
	hsvImage = color.rgb2hsv(img);
	
	h = [0 for x in range(360)];
	s = [0 for x in range(101)];
	v = [0 for x in range(101)];
	for i in range(height):
		for j in range(width):
			#p1 = img[i, j];
			#print("p1 ",p1);
			pixel = hsvImage[i,j];
			pixel[0] = int(round(pixel[0]*359));
			pixel[1] = int(round(pixel[1]*100));
			pixel[2] = int(round(pixel[2]*100));
			#print(pixel);
			#print(pixel[0]);
			#print(pixel[1]);
			#print(pixel[2]);
			h[int(round(pixel[0]))]+=1;
			s[int(round(pixel[1]))]+=1;
			v[int(round(pixel[2]))]+=1;			
	#mode of RGB
	hsvMode = [getMode(h), getMode(s), getMode(v)];	
	#median of RGB
	#h.sort();
	#s.sort();
	#v.sort();
	half = height*width/2;
	hsvMed = getMedian(half, h, s, v);	
	#avarage of RGB
	hsvAva = getAvarage(hsvImage, height, width);
	
	return hsvAva, hsvMed, hsvMode; 

	
def calculateRGB():
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
	img = io.imread(file);
	height, width = len(img), len(img[0]);
	red = [0 for x in range(256)];
	green = [0 for x in range(256)];
	blue = [0 for x in range(256)];
	for i in range(height):
		for j in range(width): 
			pixel = img[i, j];
			red[pixel[0]]+=1;
			green[pixel[1]]+=1;
			blue[pixel[2]]+=1;	
	#mode of RGB
	rgbMode = [getMode(red), getMode(green), getMode(blue)];	
	#median of RGB
	#red.sort();
	#green.sort();
	#blue.sort();
	half = height*width/2;
	rgbMed = getMedian(half, red, green, blue);	
	#avarage of RGB
	rgbAva = getAvarage(img, height, width);
	
	return rgbAva, rgbMed, rgbMode; 


def getMode(vector):
	bigger = vector[0];
	position = 0;
	cont = 0;
	for cont in range(len(vector)):
		if(vector[cont] > bigger):
			bigger = vector[cont];
			position = cont;
		cont+=1;
	return position;


def getAvarage(picture, height, width):
	rAvarage = 0.0;
	gAvarage = 0.0;
	bAvarage = 0.0;
	first = True;
	for i in range(height):
		for j in range(width):
			pixel = picture[i, j];
			rAvarage+= pixel[0];
			gAvarage+= pixel[1];
			bAvarage+= pixel[2];
	rAvarage/=(width*height);
	gAvarage/=(width*height);
	bAvarage/=(width*height);
	return [int(rAvarage), int(gAvarage), int(bAvarage)];


def getMedian(half, red, green, blue):
	cont = 0;
	i = 0;
	while(cont+red[i] < half):
		cont+=red[i];
		i+=1;
	rMedian = i;
	cont = 0;
	i = 0;
	while(cont+green[i] < half):
		cont+=green[i];
		i+=1;
	gMedian = i;
	cont = 0;
	i = 0;
	while(cont+blue[i] < half):
		cont+=blue[i];
		i+=1;
	bMedian = i;
	return [rMedian, gMedian, bMedian];


def makePlots(f):
	inFile = open(f, "r",newline='');
	reader = csv.reader(inFile);
	#plt.close('all');
	#f, axarr = plt.subplots(3, 3);
	fig, ax = plt.subplots();	
	first = True;
	second = True;
	t1 = "R";
	t2 = "G";
	t3 = "B";
	group = [];
	qtdGroup = [];
	file = [];
	c1Ava = [];
	c2Ava = [];
	c3Ava = [];
	c1Median = [];
	c2Median = [];
	c3Median = [];
	c1Mode = [];
	c2Mode = [];
	c3Mode = [];
	x = []
	cont = 0;
	for row in reader:
		if(first):
			first = False;
			if(row[0].endswith("V(MODE) ")):
				t1 = "H";
				t2 = "S";
				t3 = "V";
			#configAxarr(axarr, t1, t2, t3);
		else:			
			item = row[0].split(";");
			if(second):
				second = False;
				group.append(item[0]);
				file.append(item[1]);
				c1Ava.append(item[2]);
				c2Ava.append(item[3]);
				c3Ava.append(item[4]);
				c1Median.append(item[5]);
				c2Median.append(item[6]);
				c3Median.append(item[7]);
				c1Mode.append(item[8]);
				c2Mode.append(item[9]);
				c3Mode.append(item[10]);
				x.append(cont);
				cont+=1;
			#new group to plot, so plot the actual before
			if(group[-1] != item[0]):
				qtdGroup.append(cont);
				file.append(item[1]);				
				group.append(item[0]);
				file.append(item[1]);
				c1Ava.append(int(item[2]));
				c2Ava.append(int(item[3]));
				c3Ava.append(int(item[4]));
				c1Median.append(int(item[5]));
				c2Median.append(int(item[6]));
				c3Median.append(int(item[7]));
				c1Mode.append(int(item[8]));
				c2Mode.append(int(item[9]));
				c3Mode.append(int(item[10]));
				x.append(cont);
				cont+=1;
			else:
				file.append(item[1]);
				c1Ava.append(int(item[2]));
				c2Ava.append(int(item[3]));
				c3Ava.append(int(item[4]));
				c1Median.append(int(item[5]));
				c2Median.append(int(item[6]));
				c3Median.append(int(item[7]));
				c1Mode.append(int(item[8]));
				c2Mode.append(int(item[9]));
				c3Mode.append(int(item[10]));
				x.append(cont);
				cont+=1;
	
	qtdGroup.append(cont);	
	a = qtdGroup[0];
	b = qtdGroup[1];
	c = qtdGroup[2];
	
	#plot per plot	
	plt.title(t1+"(Avarage)x Sample");
	plt.xlabel("Sample");
	plt.ylabel(t1);
	ax.scatter(x[0:a], c1Ava[0:a], label = group[0]);	
	ax.scatter(x[a:b], c1Ava[a:b], label = group[1]);
	ax.scatter(x[b:c], c1Ava[b:c], label = group[2]);
	print(c1Ava)
	
	#ax.xaxis.set_major_locator(ticker.MultipleLocator(50));
	#ax.yaxis.set_major_locator(ticker.MultipleLocator(50));	
	plt.plot([-100, 600], [0,0], color='k');
	plt.plot([-100, 600], [100,100], color='k');
	plt.plot([-100, 600], [200,200], color='k');
	plt.plot([-100, 600], [256,256], color='k');
	plt.axis([-50, 550, 0, 300])
	plt.legend();
	#plt.grid(True)
	plt.show();
	
	'''
	plotOnlyOne(t1+"(Avarage)x Sample", "Sample", t1, group[0], x[:a], c1Ava[:a], ax);
	plotOnlyOne(t1+"(Avarage)x Sample", "Sample", t1, group[1], x[a:b], c1Ava[a:b], ax);
	plotOnlyOne(t1+"(Avarage)x Sample", "Sample", t1, group[2], x[b:c], c1Ava[b:c], ax);	
	'''
	
	'''
	#input("Press [enter] to continue.");
	plt.title(t2+"(Avarage)x Sample");
	plt.xlabel("Sample");
	plt.ylabel(t2);
	ax.scatter(x[:a], c2Ava[:a], label = group[0]);	
	ax.scatter(x[a:b], c2Ava[a:b], label = group[1]);
	ax.scatter(x[b:c], c2Ava[b:c], label = group[2]);
	plt.legend();
 
	plt.grid(True, which='both')
	plt.show();
	'''
	'''	
	plotOnlyOne(t2+"(Avarage)x Sample", "Sample", t2, group[0], x[:a], c2Ava[:a], ax);	
	plotOnlyOne(t3+"(Avarage)x Sample", "Sample", t3, group[0], x[:a], c3Ava[:a], ax);
	input("Press [enter] to continue.")	
	plt.show();			
	
	
	plotOnlyOne(t1+"(Median)x Sample", "Sample", t1, group[1], x[a:b], c1Median[a:b], ax);
	plotOnlyOne(t2+"(Median)x Sample", "Sample", t2, group[1], x[a:b], c2Median[a:b], ax);
	plotOnlyOne(t3+"(Median)x Sample", "Sample", t3, group[1], x[a:b], c3Median[a:b], ax);
	input("Press [enter] to continue.")	
	plt.show();			
	
	
	plotOnlyOne(t1+"(Mode)x Sample", "Sample", t1, group[2], x[b:c], c1Mode[b:c], ax);
	plotOnlyOne(t2+"(Mode)x Sample", "Sample", t2, group[2], x[b:c], c2Mode[b:c], ax);
	plotOnlyOne(t3+"(Mode)x Sample", "Sample", t3, group[2], x[b:c], c3Mode[b:c], ax);
	plt.show();	
	'''	
				
	
	inFile.close();
	
	
	
def plotOnlyOne(title, xTitle, yTitle, group, x, y, ax):
	plt.title(title);
	plt.xlabel(xTitle);
	plt.ylabel(xTitle);
	ax.scatter(x, y, label = group);	

'''
def makePlots(f):
	inFile = open(f, "r",newline='');
	reader = csv.reader(inFile);
	plt.close('all');
	f, axarr = plt.subplots(3, 3);
	first = True;
	second = True;
	t1 = "H";
	t2 = "S";
	t3 = "V";
	group = "";
	file = [];
	c1Ava = [];
	c2Ava = [];
	c3Ava = [];
	c1Median = [];
	c2Median = [];
	c3Median = [];
	c1Mode = [];
	c2Mode = [];
	c3Mode = [];
	x = []
	cont = 0;
	for row in reader:
		if(first):
			first = False;
			if(row[0].endswith("V(MODE) ")):
				t1 = "H";
				t2 = "S";
				t3 = "V";
			configAxarr(axarr, t1, t2, t3);
		else:			
			item = row[0].split(";");
			if(second):
				second = False;
				group = item[0];
				file.append(item[1]);
				c1Ava.append(item[2]);
				c2Ava.append(item[3]);
				c3Ava.append(item[4]);
				c1Median.append(item[5]);
				c2Median.append(item[6]);
				c3Median.append(item[7]);
				c1Mode.append(item[8]);
				c2Mode.append(item[9]);
				c3Mode.append(item[10]);
				x.append(cont);
				cont+=1;
			#new group to plot, so plot the actual before
			if(group != item[0]):
				print("size of c1 ",len(c1Ava))
				print("size of x ", len(x))
				print("x is ", x)
				axarr[0, 0].scatter(c1Ava, x, label = group);
				axarr[0, 1].scatter(c2Ava, x, label = group);
				axarr[0, 2].scatter(c3Ava, x, label = group);
				axarr[1, 0].scatter(c1Median, x, label = group);
				axarr[1, 1].scatter(c2Median, x, label = group);
				axarr[1, 2].scatter(c3Median, x, label = group);
				axarr[2, 0].scatter(c1Mode, x, label = group);
				axarr[2, 1].scatter(c2Mode, x, label = group);
				axarr[2, 2].scatter(c3Mode, x, label = group);
				file.append(item[1]);
				c1Ava = [];
				c2Ava = [];
				c3Ava = [];
				c1Median = [];
				c2Median = [];
				c3Median = [];
				c1Mode = [];
				c2Mode = [];
				c3Mode = [];
				x = [];
				group = item[0];
				file.append(item[1]);
				c1Ava.append(int(item[2]));
				c2Ava.append(int(item[3]));
				c3Ava.append(int(item[4]));
				c1Median.append(int(item[5]));
				c2Median.append(int(item[6]));
				c3Median.append(int(item[7]));
				c1Mode.append(int(item[8]));
				c2Mode.append(int(item[9]));
				c3Mode.append(int(item[10]));
				x.append(cont);
				cont+=1;
			else:
				file.append(item[1]);
				c1Ava.append(int(item[2]));
				c2Ava.append(int(item[3]));
				c3Ava.append(int(item[4]));
				c1Median.append(int(item[5]));
				c2Median.append(int(item[6]));
				c3Median.append(int(item[7]));
				c1Mode.append(int(item[8]));
				c2Mode.append(int(item[9]));
				c3Mode.append(int(item[10]));
				x.append(cont);
				cont+=1;		
	axarr[0, 0].legend();
	plt.show();			
	inFile.close();
'''

def configAxarr(axarr, t1, t2, t3):
	axarr[0, 0].set_title(t1+"(Avarage)x Sample");
	axarr[0, 0].set_xlabel("Sample");
	axarr[0, 0].set_ylabel(t1);
	axarr[0, 0].grid();
	axarr[0, 1].set_title(t2+"(Avarage)x Sample");
	axarr[0, 1].set_xlabel("Sample");
	axarr[0, 1].set_ylabel(t2);
	axarr[0, 1].grid();
	axarr[0, 2].set_title(t3+"(Avarage)x Sample");
	axarr[0, 2].set_xlabel("Sample");
	axarr[0, 2].set_ylabel(t3);
	axarr[0, 2].grid();
	axarr[1, 0].set_title(t1+"(Median)x Sample");
	axarr[1, 0].set_xlabel("Sample");
	axarr[1, 0].set_ylabel(t1);
	axarr[1, 0].grid();
	axarr[1, 1].set_title(t2+"(Median)x Sample");
	axarr[1, 1].set_xlabel("Sample");
	axarr[1, 1].set_ylabel(t2);
	axarr[1, 1].grid();
	axarr[1, 2].set_title(t3+"(Median)x Sample");
	axarr[1, 2].set_xlabel("Sample");
	axarr[1, 2].set_ylabel(t3);
	axarr[1, 2].grid();
	axarr[2, 0].set_title(t1+"(Mode)x Sample");
	axarr[2, 0].set_xlabel("Sample");
	axarr[2, 0].set_ylabel(t1);
	axarr[2, 0].grid();
	axarr[2, 1].set_title(t2+"(Mode)x Sample");
	axarr[2, 1].set_xlabel("Sample");
	axarr[2, 1].set_ylabel(t2);
	axarr[2, 1].grid();
	axarr[2, 2].set_title(t3+"(Mode)x Sample");
	axarr[2, 2].set_xlabel("Sample");
	axarr[2, 2].set_ylabel(t3);
	axarr[2, 2].grid();	

	
#domainColor2D();
#domainColor3D();
#histogramColor();
#calculateRGB();
#calculateHSV();
makePlots("..\\outputRGB.csv");

#"""
import unittest;
class MyTest(unittest.TestCase):
	import numpy as np;
	def test(self):
		vec1 = [1 for i in range(10)];
		vec2 = [i for i in range(10)];
		vec3 = [0, 0, 0, 0, 10 ,15, 16, 22, 37];
		vec4 = [-100, 3, 5, 7, 12, 14, 18, 0, 0, 11, 11, 1, 1, 1, 1];
		vec5 = [[[1 for i in range(3)] for j in range(10)] for k in range(10)];
		vec6 = [[[i for i in range(3)] for j in range(10)] for k in range(10)];
		#tamanho 10
		vec7 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 2];
		vec8 = [10, 0, 0, 0, 0, 0, 0, 0, 0, 0];
		vec9 = [1, 0, 0, 0, 0, 0, 0, 0, 9, 0];
		#retorna a posicao do maior
		#getMode();
		self.assertEqual(getMode(vec1), 0);
		self.assertEqual(getMode(vec2), 9);
		self.assertEqual(getMode(vec3), 8);
		self.assertEqual(getMode(vec4), 6);
		
		#getAvarage();
		#self.assertEqual(getAvarage(vec5, len(vec5), len(vec5[0])), [1, 1, 1]);
		#self.assertEqual(getAvarage(vec6, len(vec6), len(vec6[0])), [0, 1, 2]);
		
		#getMedian();
		self.assertEqual(getMedian(5, vec7, vec8, vec9), [5, 0, 8]);		
#"""		
		

