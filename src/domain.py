from __future__ import print_function;
from skimage import color, io;
import os, sys, time, csv;
from src.model.easyPlot import dotsPlot2D, dotsPlot3D, histogram;
from src.model.imageData import imageData;
from matplotlib import pyplot as plt;
from matplotlib import ticker
#from mpl_toolkits.mplot3d import axes3d, Axes3D
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
	saturations = [0 for z in range(hueRange)];
	brightnesses = [0 for z in range(hueRange)];
	
	for x in range(width):
		for y in range(height):
			pixel = allPixels[x, y];
			c1 = int( round(pixel[0]*359) );
			hues[c1]+=1;
			saturations[c1] += pixel[1]*101;
			brightnesses[c1] += pixel[2]*101;	
	maior = hues[0];
	hue = 0;
	cont = 0;
	for h  in hues:
		if(h > maior):
			maior = h; 
			hue = cont;
		cont+=1;	
	h = hue;
	s = int(round(saturations[h]/maior));
	b = int(round(brightnesses[h]/maior));	
	#return [h, s, b], maior;
	return h, s, b;


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


def calculateLUV():
	startTime = time.time();
	outFile = open("..\\outputLUV.csv", "w",newline='');
	writer = csv.writer(outFile, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL);
	writer.writerow(["GROUP;NAME;L(AVARAGE);U(AVARAGE);V(AVARAGE);L(MEDIAN);U(MEDIAN);V(MEDIAN);L(MODE);U(MODE);V(MODE)"]);
	for subdir, dirs, files in os.walk(os.path.abspath(os.path.join('.\\', os.pardir))+'\\Images\\'):
		group = subdir.split("\\")[-1];
		print(subdir);
		for file in files:
			print("\t",file);
			name = file;
			file = subdir+"\\"+file
			luvAva, luvMed, luvMode = calculeLUVHistogram(file);
			print("luvAvarage ", luvAva);
			print("luvMedian ", luvMed);
			print("luvMode ", luvMode);
			#time.sleep(3);			
			row = ("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s") % (group, name, str(luvAva[0]), str(luvAva[1]), str(luvAva[2]),
				str(luvMed[0]), str(luvMed[1]), str(luvMed[2]), str(luvMode[0]), str(luvMode[1]), str(luvMode[2]));
			writer.writerow([row]);										
	elapsedTime = time.time() - startTime;
	outFile.close();
	print("FINISH, ELAPSED TIME(seconds): ",elapsedTime);


def calculeLUVHistogram(file):
	img = io.imread(file);
	height, width = len(img), len(img[0]);		
	luvImage = color.rgb2luv(img);
	
	l = [0 for x in range(101)];#   0 : 100
	#u = [0 for x in range(201)];#-100 : 100
	#v = [0 for x in range(201)];#-100 : 100
	u = [0 for x in range(501)];#-100 : 100
	v = [0 for x in range(501)];#-100 : 100
	for i in range(height):
		for j in range(width):
			pixel = luvImage[i,j];
			#print(pixel);
			l[int(round(pixel[0]))]+=1;
			#u[int(round(pixel[1] + 100))]+=1;			
			#v[int(round(pixel[2] + 100))]+=1;
			u[int(round(pixel[1] + 250))]+=1;
			v[int(round(pixel[2] + 250))]+=1;
	#mode of LUV
	luvMode = [getMode(l), getMode(u), getMode(v)];
	luvMode[1] = luvMode[1] - 250;
	luvMode[2] = luvMode[2] - 250; 
	
	#median of LUV
	half = height*width/2;
	luvMed = getMedian(half, l, u, v);
	luvMed[1] = luvMed[1] - 250;
	luvMed[2] = luvMed[2] - 250;
	
	#avarage of LUV
	luvAva = [getAvarage(l, height*width), getAvarage(u, height*width), getAvarage(v, height*width)];
	luvAva[1] = luvAva[1] - 250;
	luvAva[2] = luvAva[2] - 250;
	
	return luvAva, luvMed, luvMode;


def calculateLAB():
	startTime = time.time();
	outFile = open("..\\outputLAB.csv", "w",newline='');
	writer = csv.writer(outFile, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL);
	writer.writerow(["GROUP;NAME;L(AVARAGE);A(AVARAGE);B(AVARAGE);L(MEDIAN);A(MEDIAN);B(MEDIAN);L(MODE);A(MODE);B(MODE)"]);
	for subdir, dirs, files in os.walk(os.path.abspath(os.path.join('.\\', os.pardir))+'\\Images\\'):
		group = subdir.split("\\")[-1];
		print(subdir);
		for file in files:
			print("\t",file);
			name = file;
			file = subdir+"\\"+file
			labAva, labMed, labMode = calculeLABHistogram(file);
			print("labAvarage ", labAva);
			print("labMedian ", labMed);
			print("labMode ", labMode);
			#time.sleep(10);			
			row = ("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s") % (group, name, str(labAva[0]), str(labAva[1]), str(labAva[2]),
				str(labMed[0]), str(labMed[1]), str(labMed[2]), str(labMode[0]), str(labMode[1]), str(labMode[2]));
			writer.writerow([row]);										
	elapsedTime = time.time() - startTime;
	outFile.close();
	print("FINISH, ELAPSED TIME(seconds): ",elapsedTime);


def calculeLABHistogram(file):
	img = io.imread(file);
	height, width = len(img), len(img[0]);
	labImage = color.rgb2lab(img);	
	
	l = [0 for x in range(101)];#   0 : 100
	a = [0 for x in range(256)];#-128 : 127
	b = [0 for x in range(256)];#-128 : 127
	for i in range(height):
		for j in range(width):
			pixel = labImage[i,j];
			#print(pixel);
			l[int(round(pixel[0]))]+=1;
			a[int(round(pixel[1] + 128))]+=1;
			b[int(round(pixel[2] + 128))]+=1;
	#mode of LAB
	labMode = [getMode(l), getMode(a), getMode(b)];
	labMode[1] = labMode[1] - 128;
	labMode[2] = labMode[2] - 128; 
	
	#median of LAB
	half = height*width/2;
	labMed = getMedian(half, l, a, b);
	labMed[1] = labMed[1] - 128;
	labMed[2] = labMed[2] - 128;
	
	#avarage of LAB
	labAva = [getAvarage(l, height*width), getAvarage(a, height*width), getAvarage(b, height*width)];
	labAva[1] = labAva[1] - 128;
	labAva[2] = labAva[2] - 128;
	
	return labAva, labMed, labMode;

def concertaLAB():	
	inFile = open("..\\outputLAB.csv", "r",newline='');
	reader = csv.reader(inFile);
	first = True;
	nRows = [];
	for row in reader:
		if(first):
			first = False;
		else:
			i = row[0].split(';');
			print(i)
			group = i[0];
			file = i[1];
			c1 = i[2];
			c2 = str( int(i[3]) - 128);
			c3 = str( int(i[4]) - 128);
			c4 = i[5];
			c5 = str( int(i[6]) - 128);
			c6 = str( int(i[7]) - 128);
			c7 = i[8];
			c8 = str( int(i[9]) - 128);
			c9 = str( int(i[10]) - 128);			
			nRows.append([
						( ("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s") %
				(group, file, c1, c2, c3, c4, c5, c6, c7, c8, c9) )
						]);			
	inFile.close
	
	outFile = open("..\\outputLAB2.csv", "w",newline='');
	writer = csv.writer(outFile, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL);
	writer.writerow(["GROUP;NAME;L(AVARAGE);A(AVARAGE);B(AVARAGE);L(MEDIAN);A(MEDIAN);B(MEDIAN);L(MODE);A(MODE);B(MODE)"]);
	
	for nR in nRows:
		writer.writerow(nR);		
			
	outFile.close()


def calculateHSV3D():
	startTime = time.time();
	outFile = open("..\\outputHSV3D.csv", "w",newline='');
	writer = csv.writer(outFile, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL);
	writer.writerow(["GROUP;NAME;H(MODE);S(AVARAGE);V(AVARAGE)"]);
	for subdir, dirs, files in os.walk(os.path.abspath(os.path.join('.\\', os.pardir))+'\\Images\\'):
		group = subdir.split("\\")[-1];
		print(subdir);
		for file in files:
			print("\t",file);
			name = file;
			file = subdir+"\\"+file
			hMode, sAva, vAva = calculeHSVHistogram3D(file);
			print("hMode ", hMode);
			print("sAva ", sAva);
			print("vAva ", vAva);
			row = ("%s;%s;%s;%s;%s") % (group, name, str(hMode), str(sAva), str(vAva));
			writer.writerow([row]);			
										
	elapsedTime = time.time() - startTime;
	outFile.close();
	print("FINISH, ELAPSED TIME(seconds): ",elapsedTime);


def calculeHSVHistogram3D(file):
	img = io.imread(file);
	height, width = len(img), len(img[0]);		
	hsvImage = color.rgb2hsv(img);
	
	hsvAva, hsvMed, hsvMode = getDomainColor(hsvImage, height, width);
	
	return hsvAva, hsvMed, hsvMode; 
			
			
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
			row = ("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s") % (group, name, str(hsvAva[0]), str(hsvAva[1]), str(hsvAva[2]),
				str(hsvMed[0]), str(hsvMed[1]), str(hsvMed[2]), str(hsvMode[0]), str(hsvMode[1]), str(hsvMode[2]));
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
	#mode of HSV
	hsvMode = [getMode(h), getMode(s), getMode(v)];	
	#median of HSV	
	half = height*width/2;
	hsvMed = getMedian(half, h, s, v);	
	#avarage of HSV
	hsvAva = [getAvarage(h, height*width), getAvarage(s, height*width),getAvarage(v, height*width)];
	
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
			row = ("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s") % (group, name, str(rgbAva[0]), str(rgbAva[1]), str(rgbAva[2]),
				str(rgbMed[0]), str(rgbMed[1]), str(rgbMed[2]), str(rgbMode[0]), str(rgbMode[1]), str(rgbMode[2]));
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
	rgbAva = [getAvarage(red, height*width), getAvarage(green, height*width), getAvarage(blue, height*width)];
	
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


def getAvarage(c, size):
	cAvarage = 0.0;	
	
	for i in range(len(c)):
		cAvarage+=(c[i]*i);
	cAvarage= cAvarage/size;	
	
	return int(cAvarage);


def getMedian(half, c1, c2, c3):
	cont = 0;
	i = 0;
	while(cont+c1[i] < half):
		cont+=c1[i];
		i+=1;
	rMedian = i;
	cont = 0;
	i = 0;
	while(cont+c2[i] < half):
		cont+=c2[i];
		i+=1;
	gMedian = i;
	cont = 0;
	i = 0;
	while(cont+c3[i] < half):
		cont+=c3[i];
		i+=1;
	bMedian = i;
	return [rMedian, gMedian, bMedian];


def makePlot3D(f):
	inFile = open(f, "r",newline='');
	reader = csv.reader(inFile);	
	first = True;
	second = True;
	t1 = "H(MODE)";
	t2 = "S(AVARAGE)";
	t3 = "V(AVARAGE)";
	group = [];
	qtdGroup = [];
	file = [];
	c1 = [];
	c2 = [];
	c3 = [];	
	cont = 0;
	for row in reader:
		if(first):
			first = False;
			'''
			if(row[0].endswith("V(MODE) ")):
				t1 = "H";
				t2 = "S";
				t3 = "V";
			elif(row[0].endswith("B(MODE) ")):
				t1 = "L";
				t2 = "A";
				t3 = "B";
			'''	
		else:			
			item = row[0].split(";");
			if(second):
				second = False;
				group.append(item[0]);
				file.append(item[1]);
				c1.append(int(item[2]));
				c2.append(int(item[3]));
				c3.append(int(item[4]));				
				cont+=1;
			#new group to plot, so plot the actual before
			elif(group[-1] != item[0]):
				qtdGroup.append(cont);
				group.append(item[0]);
				file.append(item[1]);
				c1.append(int(item[2]));
				c2.append(int(item[3]));
				c3.append(int(item[4]));				
				cont+=1;
			else:
				file.append(item[1]);
				c1.append(int(item[2]));
				c2.append(int(item[3]));
				c3.append(int(item[4]));				
				cont+=1;	
	qtdGroup.append(cont);
	inFile.close();
	a = qtdGroup[0];#1: 0 	 - 149
	b = qtdGroup[1];#2: 150 - 299
	c = qtdGroup[2];#3: 300 - 499	
	
	fig = plt.figure();        
	ax = fig.add_subplot(111, projection = '3d');
	#ax = fig.gca(projection='3d');
	#ax = Axes3D(fig)    
	ax.set_xlabel("X - Value(Avarage)");
	ax.set_ylabel("Y - Saturation(Avarage)");
	ax.set_zlabel("Z - Hue(Mode)");	
	ax.scatter(c3[0:a-1], c2[0:a-1], c1[0:a-1], label=group[0]);
	ax.scatter(c3[a:b-1], c2[a:b-1], c1[a:b-1], label=group[1]);
	ax.scatter(c3[b:c-1], c2[b:c-1], c1[b:c-1], label=group[2]);	            	
	plt.grid();        
	plt.legend();
	plt.show();						


def makeSeparetedPlot(f):
	inFile = open(f, "r",newline='');
	reader = csv.reader(inFile);
	#plt.close('all');
	#f, axarr = plt.subplots(3, 3);		
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
			if(row[0].endswith("S(MODE);V(MODE) ")):
				t1 = "H";
				t2 = "S";
				t3 = "V";
			elif(row[0].endswith("B(MODE) ")):
				t1 = "L";
				t2 = "A";
				t3 = "B";
			elif(row[0].endswith("U(MODE);V(MODE) ")):
				t1 = "L";
				t2 = "U";
				t3 = "V";	
		else:			
			item = row[0].split(";");
			if(second):
				second = False;
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
			#new group to plot, so plot the actual before
			elif(group[-1] != item[0]):
				qtdGroup.append(cont);
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
	a = qtdGroup[0];#1: 0 	 - 149
	b = qtdGroup[1];#2: 150 - 299
	c = qtdGroup[2];#3: 300 - 499
	
	resp = input("save it?(y/n): ");
	
	#AVARAGES
	#c1(Avarage)
	plotOneByOne(t1+"(Avarage) x Sample", "Sample", t1, group, x, c1Ava, a, b, c, resp);
	#c2(Avarage)
	plotOneByOne(t2+"(Avarage) x Sample", "Sample", t2, group, x, c2Ava, a, b, c, resp);
	#c3(Avarage)
	plotOneByOne(t3+"(Avarage) x Sample", "Sample", t3, group, x, c3Ava, a, b, c, resp);	
	#MEDIAN
	#c1(Median)
	plotOneByOne(t1+"(Median) x Sample", "Sample", t1, group, x, c1Median, a, b, c, resp);
	#c2(Median)
	plotOneByOne(t2+"(Median) x Sample", "Sample", t2, group, x, c2Median, a, b, c, resp);
	#c3(Median)
	plotOneByOne(t3+"(Median) x Sample", "Sample", t3, group, x, c3Median, a, b, c, resp);	
	#MODE
	#c1(Mode)
	plotOneByOne(t1+"(Mode) x Sample", "Sample", t1, group, x, c1Mode, a, b, c, resp);
	#c2(Mode)
	plotOneByOne(t2+"(Mode) x Sample", "Sample", t2, group, x, c2Mode, a, b, c, resp);
	#c3(Mode)
	plotOneByOne(t3+"(Mode) x Sample", "Sample", t3, group, x, c3Mode, a, b, c, resp);
				
	inFile.close();
		
	
def plotOneByOne(title, xTitle, yTitle, group, x, y, a, b, c, resp):
	fig, ax = plt.subplots();
	plt.title(title);
	plt.xlabel(xTitle);
	plt.ylabel(yTitle);
	ax.scatter(x[0:a-1], y[0:a-1], label = group[0]);	
	ax.scatter(x[a:b-1], y[a:b-1], label = group[1]);
	ax.scatter(x[b:c-1], y[b:c-1], label = group[2]);	
	plt.legend();
	plt.grid(True);
	fig.set_size_inches(14,6)
	if(resp == "y"):		
		plt.savefig("..\\plots\\"+title);	
	#plt.show();
	plt.close();


def makePlots(f):
	inFile = open(f, "r",newline='');
	reader = csv.reader(inFile);
	plt.close('all');
	f, axarr = plt.subplots(3, 3);
	first = True;
	second = True;
	t1 = "R";
	t2 = "G";
	t3 = "B";
	name = "ALL_PLOTS_RGB";
	qtdGroup = [];
	group = [];
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
			if(row[0].endswith("S(MODE)V(MODE) ")):
				t1 = "H";
				t2 = "S";
				t3 = "V";
				name = "ALL_PLOTS_HSV";
			elif(row[0].endswith("B(MODE) ")):
				t1 = "L";
				t2 = "A";
				t3 = "B";
				name = "ALL_PLOTS_LAB";
			elif(row[0].endswith("U(MODE);V(MODE) ")):
				t1 = "L";
				t2 = "U";
				t3 = "V";
				name = "ALL_PLOTS_LUV";
			configAxarr(axarr, t1, t2, t3);
		else:			
			item = row[0].split(";");
			if(second):
				second = False;
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
			#new group to plot, so plot the actual before
			elif(group[-1] != item[0]):
				qtdGroup.append(cont);
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
	
	a = qtdGroup[0];#1: 0 	 - 149
	b = qtdGroup[1];#2: 150 - 299
	c = qtdGroup[2];#3: 300 - 499
	
	resp = input("save it?(y/n): ");
	
	plotAxarr(f, axarr, x, c1Ava, c2Ava, c3Ava, c1Median, c2Median, c3Median,
			c1Mode, c2Mode, c3Mode, a, b, c, group, resp, name);
				
	inFile.close();

def plotAxarr(f, axarr,x, c1Ava, c2Ava, c3Ava, c1Median, c2Median, c3Median,
			c1Mode, c2Mode, c3Mode, a, b, c, group, resp, name):
	#AVARAGE
	#c1Ava
	axarr[0, 0].scatter(x[0:a-1], c1Ava[0:a-1], label = group[0]);
	axarr[0, 0].scatter(x[a:b-1], c1Ava[a:b-1], label = group[1]);
	axarr[0, 0].scatter(x[b:c-1], c1Ava[b:c-1], label = group[2]);
	axarr[0, 0].legend();
	#c2Ava
	axarr[0, 1].scatter(x[0:a-1], c2Ava[0:a-1], label = group[0]);
	axarr[0, 1].scatter(x[a:b-1], c2Ava[a:b-1], label = group[1]);
	axarr[0, 1].scatter(x[b:c-1], c2Ava[b:c-1], label = group[2]);
	axarr[0, 1].legend();
	#c3Ava
	axarr[0, 2].scatter(x[0:a-1], c3Ava[0:a-1], label = group[0]);
	axarr[0, 2].scatter(x[a:b-1], c3Ava[a:b-1], label = group[1]);
	axarr[0, 2].scatter(x[b:c-1], c3Ava[b:c-1], label = group[2]);
	axarr[0, 2].legend();
	
	#MEDIAN
	#c1Median
	axarr[1, 0].scatter(x[0:a-1], c1Median[0:a-1], label = group[0]);
	axarr[1, 0].scatter(x[a:b-1], c1Median[a:b-1], label = group[1]);
	axarr[1, 0].scatter(x[b:c-1], c1Median[b:c-1], label = group[2]);
	axarr[1, 0].legend();
	#c2Median
	axarr[1, 1].scatter(x[0:a-1], c2Median[0:a-1], label = group[0]);
	axarr[1, 1].scatter(x[a:b-1], c2Median[a:b-1], label = group[1]);
	axarr[1, 1].scatter(x[b:c-1], c2Median[b:c-1], label = group[2]);
	axarr[1, 1].legend();
	#c3Median
	axarr[1, 2].scatter(x[0:a-1], c3Median[0:a-1], label = group[0]);
	axarr[1, 2].scatter(x[a:b-1], c3Median[a:b-1], label = group[1]);
	axarr[1, 2].scatter(x[b:c-1], c3Median[b:c-1], label = group[2]);
	axarr[1, 2].legend();
	
	#MODE
	#c1Mode
	axarr[2, 0].scatter(x[0:a-1], c1Mode[0:a-1], label = group[0]);
	axarr[2, 0].scatter(x[a:b-1], c1Mode[a:b-1], label = group[1]);
	axarr[2, 0].scatter(x[b:c-1], c1Mode[b:c-1], label = group[2]);
	axarr[2, 0].legend();
	#c2Mode
	axarr[2, 1].scatter(x[0:a-1], c2Mode[0:a-1], label = group[0]);
	axarr[2, 1].scatter(x[a:b-1], c2Mode[a:b-1], label = group[1]);
	axarr[2, 1].scatter(x[b:c-1], c2Mode[b:c-1], label = group[2]);
	axarr[2, 1].legend();
	#c3Mode
	axarr[2, 2].scatter(x[0:a-1], c3Mode[0:a-1], label = group[0]);
	axarr[2, 2].scatter(x[a:b-1], c3Mode[a:b-1], label = group[1]);
	axarr[2, 2].scatter(x[b:c-1], c3Mode[b:c-1], label = group[2]);
	axarr[2, 2].legend();
	
	f.set_size_inches(14,6)
	#f.figsize=(8, 6)
	if(resp=='y'):
		plt.savefig("..\\plots\\"+name);		
	plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.6);	
	plt.show();
	


def configAxarr(axarr, t1, t2, t3):
	axarr[0, 0].set_title(t1+"(Avarage) x Sample");
	axarr[0, 0].set_xlabel("Sample");
	axarr[0, 0].set_ylabel(t1);
	axarr[0, 0].grid();
	axarr[0, 1].set_title(t2+"(Avarage) x Sample");
	axarr[0, 1].set_xlabel("Sample");
	axarr[0, 1].set_ylabel(t2);
	axarr[0, 1].grid();
	axarr[0, 2].set_title(t3+"(Avarage) x Sample");
	axarr[0, 2].set_xlabel("Sample");
	axarr[0, 2].set_ylabel(t3);
	axarr[0, 2].grid();
	axarr[1, 0].set_title(t1+"(Median) x Sample");
	axarr[1, 0].set_xlabel("Sample");
	axarr[1, 0].set_ylabel(t1);
	axarr[1, 0].grid();
	axarr[1, 1].set_title(t2+"(Median) x Sample");
	axarr[1, 1].set_xlabel("Sample");
	axarr[1, 1].set_ylabel(t2);
	axarr[1, 1].grid();
	axarr[1, 2].set_title(t3+"(Median) x Sample");
	axarr[1, 2].set_xlabel("Sample");
	axarr[1, 2].set_ylabel(t3);
	axarr[1, 2].grid();
	axarr[2, 0].set_title(t1+"(Mode) x Sample");
	axarr[2, 0].set_xlabel("Sample");
	axarr[2, 0].set_ylabel(t1);
	axarr[2, 0].grid();
	axarr[2, 1].set_title(t2+"(Mode) x Sample");
	axarr[2, 1].set_xlabel("Sample");
	axarr[2, 1].set_ylabel(t2);
	axarr[2, 1].grid();
	axarr[2, 2].set_title(t3+"(Mode) x Sample");
	axarr[2, 2].set_xlabel("Sample");
	axarr[2, 2].set_ylabel(t3);
	axarr[2, 2].grid();	


	
#calculateRGB();
#calculateHSV();
#calculateLAB();
#calculateLUV();
#makePlot3D("..\\outputHSV3D.csv");
#calculeLUVHistogram("D:\Workspaces\Python\domainColor\Images\H&E\H&E-NORMAL GLOMERULUS  (238).jpg");
#calculateHSV3D();
#makePlots("..\\outputLUV.csv");
#concertaLAB();
makeSeparetedPlot("..\\outputLUV.csv");

import unittest;
class MyTest(unittest.TestCase):
	def test(self):
		vec1 = [1 for i in range(10)];
		vec2 = [i for i in range(10)];
		vec3 = [0, 0, 0, 0, 10 ,15, 16, 22, 37];
		vec4 = [-100, 3, 5, 7, 12, 14, 18, 0, 0, 11, 11, 1, 1, 1, 1];				
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
		self.assertEqual(getAvarage(vec1, len(vec1)), 4);
		self.assertEqual(getAvarage(vec9, len(vec9)), 7);
		
		#getMedian();
		self.assertEqual(getMedian(5, vec7, vec8, vec9), [5, 0, 8]);		






		

