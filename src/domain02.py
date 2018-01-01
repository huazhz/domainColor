from __future__ import print_function;
from skimage import color, io, exposure;
import os, time, csv, sys;
from matplotlib import pyplot as plt;
import numpy as np;


def calculateLUV():
    startTime = time.time();
    outFile = open("..\\outputLUV.csv", "w",newline='');
    writer = csv.writer(outFile, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL);
    writer.writerow(["GROUP;NAME;L(AVERAGE);U(AVERAGE);V(AVERAGE);L(MEDIAN);U(MEDIAN);V(MEDIAN);"
                     +"L(DEVIATION);U(DEVIATION);V(DEVIATION);L(VARIANCE);U(VARIANCE);V(VARIANCE);"]);
    for subdir, dirs, files in os.walk(os.path.abspath(os.path.join('.\\', os.pardir))+'\\Images\\'):
        group = subdir.split("\\")[-1];
        print(subdir);
        for file in files:
            print("\t",file);
            name = file;
            file = subdir+"\\"+file
            luvAve, luvMed, luvDev, luvVar = calculeLUVHistogram(file);
            print("luvAverage ", luvAve);
            print("luvMedian ", luvMed);
            print("luvDev ", luvDev);
            print("luvVar ", luvVar);
            #time.sleep(3);            
            row = ("%s;%s;%.5f;%.5f;%.5f;%.5f;%.5f;%.5f;%.5f;%.5f;%.5f;%.5f;%.5f;%.5f") % (group,
                name, luvAve[0], luvAve[1], luvAve[2], luvMed[0], luvMed[1], luvMed[2],
                luvDev[0], luvDev[1], luvDev[2], luvVar[0], luvVar[1], luvVar[2]);
            writer.writerow([row]);                                        
    elapsedTime = time.time() - startTime;
    outFile.close();
    print("FINISH, ELAPSED TIME(seconds): ",elapsedTime);


def calculeLUVHistogram(file):
    img = io.imread(file);
    height, width = len(img), len(img[0]);
    luvImage = color.rgb2luv(img);
    #print(np.amin(labImage[:, :, 0]))
    #print(np.amax(labImage[:, :, 0]))
    luvImage[:, :, 0] = exposure.rescale_intensity(luvImage[:, :, 0],
        in_range=(np.amin(luvImage[:, :, 0]), np.amax(luvImage[:, :, 0])), out_range=(0, 100));
    luvImage[:, :, 1] = exposure.rescale_intensity(luvImage[:, :, 1],
        in_range=(np.amin(luvImage[:, :, 1]), np.amax(luvImage[:, :, 1])), out_range=(-250, 249));
    luvImage[:, :, 2] = exposure.rescale_intensity(luvImage[:, :, 2],
        in_range=(np.amin(luvImage[:, :, 2]), np.amax(luvImage[:, :, 2])), out_range=(-250, 249));   
    #print(np.amin(labImage[:, :, 0]))
    #print(np.amax(labImage[:, :, 0]))        
    l = [];    
    u = [];
    v = [];
    for i in range(height):
        for j in range(width):
            pixel = luvImage[i,j];
            l.append(pixel[0]);
            u.append(pixel[1]);
            v.append(pixel[2]);     
    
    #median of LUV    
    luvMed = [np.median(l), np.median(u), np.median(v),];    
    #average of LUV
    luvAve = [np.average(l), np.average(u), np.average(v)];
    #deviation of LUV
    luvDev = [np.std(l), np.std(u), np.std(v)];
    #variance of LUV
    luvVar = [np.var(l), np.var(u), np.var(v)];
    return luvAve, luvMed, luvDev, luvVar;


def calculateLAB():
    startTime = time.time();
    outFile = open("..\\outputLAB.csv", "w",newline='');
    writer = csv.writer(outFile, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL);
    writer.writerow(["GROUP;NAME;L(AVERAGE);A(AVERAGE);B(AVERAGE);L(MEDIAN);A(MEDIAN);B(MEDIAN);"
                     +"L(DEVIATION);A(DEVIATION);B(DEVIATION);L(VARIANCE);A(VARIANCE);B(VARIANCE);"]);
    for subdir, dirs, files in os.walk(os.path.abspath(os.path.join('.\\', os.pardir))+'\\Images\\'):
        group = subdir.split("\\")[-1];
        print(subdir);
        for file in files:
            print("\t",file);
            name = file;
            file = subdir+"\\"+file
            labAve, labMed, labDev, labVar = calculeLABHistogram(file);            
            print("labAverage ", labAve);
            print("labMedian ", labMed);
            print("labDev ", labDev);
            print("labVar ", labVar);
            #time.sleep(3);
            row = ("%s;%s;%.5f;%.5f;%.5f;%.5f;%.5f;%.5f;%.5f;%.5f;%.5f;%.5f;%.5f;%.5f") % (group,
                name, labAve[0], labAve[1], labAve[2], labMed[0],
                labMed[1], labMed[2], labDev[0], labDev[1], labDev[2],
                labVar[0], labVar[1], labVar[2]);
            '''            
            row = ("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s") % (group,
                name, str(labAve[0]), str(labAve[1]), str(labAve[2]), str(labMed[0]),
                str(labMed[1]), str(labMed[2]), str(labDev[0]), str(labDev[1]), str(labDev[2]),
                str(labVar[0]), str(labVar[1]), str(labVar[2]));
            '''
            writer.writerow([row]);
    elapsedTime = time.time() - startTime;
    outFile.close();
    print("FINISH, ELAPSED TIME(seconds): ",elapsedTime);


def calculeLABHistogram(file):
    img = io.imread(file);
    height, width = len(img), len(img[0]);
    labImage = color.rgb2lab(img);
    #print(np.amin(labImage[:, :, 0]))
    #print(np.amax(labImage[:, :, 0]))
    labImage[:, :, 0] = exposure.rescale_intensity(labImage[:, :, 0],
        in_range=(np.amin(labImage[:, :, 0]), np.amax(labImage[:, :, 0])), out_range=(0, 100));
    labImage[:, :, 1] = exposure.rescale_intensity(labImage[:, :, 1],
        in_range=(np.amin(labImage[:, :, 1]), np.amax(labImage[:, :, 1])), out_range=(-128, 127));
    labImage[:, :, 2] = exposure.rescale_intensity(labImage[:, :, 2],
        in_range=(np.amin(labImage[:, :, 2]), np.amax(labImage[:, :, 2])), out_range=(-128, 127));   
    #print(np.amin(labImage[:, :, 0]))
    #print(np.amax(labImage[:, :, 0]))        
    l = [];    
    a = [];
    b = [];
    for i in range(height):
        for j in range(width):
            pixel = labImage[i,j];
            l.append(pixel[0]);
            a.append(pixel[1]);
            b.append(pixel[2]);                    
    #average of LAB
    labAve = [np.average(l), np.average(a), np.average(b)];
    #median of LAB
    labMed = [np.median(l), np.median(a), np.median(b)];
    #variance of LAB
    labVar = [np.var(l), np.var(a), np.var(b)];    
    #dispersion of LAB
    labDev = [np.std(l), np.std(a), np.std(b)];
    
    return labAve, labMed, labDev, labVar;
     
            
def calculateHSV():
    startTime = time.time();
    outFile = open("..\\outputHSV.csv", "w",newline='');
    writer = csv.writer(outFile, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL);
    writer.writerow(["GROUP;NAME;H(AVERAGE);S(AVERAGE);V(AVERAGE);H(MEDIAN);S(MEDIAN);V(MEDIAN);"
                     +"H(DEVIATION);S(DEVIATION);V(DEVIATION);H(VARIANCE);S(VARIANCE);V(VARIANCE);"]);
    for subdir, dirs, files in os.walk(os.path.abspath(os.path.join('.\\', os.pardir))+'\\Images\\'):
        group = subdir.split("\\")[-1];
        print(subdir);
        for file in files:
            print("\t",file);
            name = file;
            file = subdir+"\\"+file
            hsvAve, hsvMed, hsvDev, hsvVar = calculeHSVHistogram(file);            
            print("hsvAverage ", hsvAve);
            print("hsvMedian ", hsvMed);
            print("hsvDev ", hsvDev);
            print("hsvVar ", hsvVar);
            #time.sleep(3);
            row = ("%s;%s;%.4f;%4.f;%.4f;%.4f;%.4f;%.4f;%.4f;%.4f;%.4f;%.4f;%.4f;%.4f") % (group,
                name, hsvAve[0], hsvAve[1], hsvAve[2], hsvMed[0],
                hsvMed[1], hsvMed[2], hsvDev[0], hsvDev[1], hsvDev[2],
                hsvVar[0], hsvVar[1], hsvVar[2]);
            writer.writerow([row]);
                                        
    elapsedTime = time.time() - startTime;
    outFile.close();
    print("FINISH, ELAPSED TIME(seconds): ",elapsedTime);


def calculeHSVHistogram(file):
    img = io.imread(file);
    height, width = len(img), len(img[0]);
    hsvImage = color.rgb2hsv(img);    

    hsvImage[:, :, 0] = exposure.rescale_intensity(hsvImage[:, :, 0],
        in_range=(np.amin(hsvImage[:, :, 0]), np.amax(hsvImage[:, :, 0])), out_range=(0.0, 1.0));
    hsvImage[:, :, 1] = exposure.rescale_intensity(hsvImage[:, :, 1],
        in_range=(np.amin(hsvImage[:, :, 1]), np.amax(hsvImage[:, :, 1])), out_range=(0.0, 1.0));
    hsvImage[:, :, 2] = exposure.rescale_intensity(hsvImage[:, :, 2],
        in_range=(np.amin(hsvImage[:, :, 2]), np.amax(hsvImage[:, :, 2])), out_range=(0.0, 1.0));   
    #print(np.amin(hsvImage[:, :, 0]))
    #print(np.amax(hsvImage[:, :, 0]))
    
    h = [];
    s = [];
    v = [];
    for i in range(height):
        for j in range(width):
            pixel = hsvImage[i,j];            
            h.append(pixel[0]*359);
            s.append(pixel[1]*100);
            v.append(pixel[2]*100);
    #average of HSV
    hsvAve = [np.nanmean(h), np.nanmean(s), np.nanmean(v)];
    #median of HSV
    hsvMed = [np.nanmedian(h), np.nanmedian(s), np.nanmedian(v)];
    #variance of HSV
    hsvVar = [np.var(h), np.var(s), np.var(v)];    
    #dispersion of HSV
    hsvDev = [np.std(h), np.std(s), np.std(v)];
    
    return hsvAve, hsvMed, hsvDev, hsvVar;

def calculateGrey():
    startTime = time.time();
    outFile = open("..\\outputGrey.csv", "w",newline='');
    writer = csv.writer(outFile, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL);
    writer.writerow(["GROUP;NAME;Grey(AVERAGE);Grey(MEDIAN);Grey(DEVIATION);Grey(VARIANCE);"]);
    for subdir, dirs, files in os.walk(os.path.abspath(os.path.join('.\\', os.pardir))+'\\Images\\'):
        group = subdir.split("\\")[-1];
        print(subdir);
        for file in files:
            print("\t",file);
            name = file;
            file = subdir+"\\"+file
            greyAve, greyMed, greyDev, greyVar = calculeGreyHistogram(file);            
            print("Greyverage ", greyAve);
            print("Greyedian ", greyMed);
            print("GreyDev ", greyDev);
            print("GreyVar ", greyVar);
            #time.sleep(3);
            row = ("%s;%s;%.2f;%.2f;%.2f;%.2f") % (group,
                name, greyAve, greyMed, greyDev, greyVar);
            writer.writerow([row]);
                                        
    elapsedTime = time.time() - startTime;
    outFile.close();
    print("FINISH, ELAPSED TIME(seconds): ",elapsedTime);
    
    
def calculeGreyHistogram(file):
    img = io.imread(file, as_grey=True);
    #print(img[0])    
    img = exposure.rescale_intensity(img);
    #print(img[0])
    height, width = len(img), len(img[0]);
    grey = [];
    for i in range(height):
        for j in range(width): 
            pixel = img[i, j];                    
            grey.append(pixel);                
    #r = exposure.equalize_hist(r1);        
    #g = exposure.equalize_hist(g1);
    #b = exposure.equalize_hist(b1);
    #average of RGB
    greyAve = np.average(grey);
    #median of RGB
    greyMed = np.median(grey);
    #variance of RGB
    greyVar = np.var(grey);
    #dispersion of RGB
    greyDev = np.std(grey);    
    
    return greyAve, greyMed, greyDev, greyVar;

   
def calculateRGB():
    startTime = time.time();
    outFile = open("..\\outputRGB.csv", "w",newline='');
    writer = csv.writer(outFile, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL);
    writer.writerow(["GROUP;NAME;R(AVERAGE);G(AVERAGE);B(AVERAGE);R(MEDIAN);G(MEDIAN);B(MEDIAN);"
                     +"R(DEVIATION);G(DEVIATION);B(DEVIATION);R(VARIANCE);G(VARIANCE);B(VARIANCE);"]);
    for subdir, dirs, files in os.walk(os.path.abspath(os.path.join('.\\', os.pardir))+'\\Images\\'):
        group = subdir.split("\\")[-1];
        print(subdir);
        for file in files:
            print("\t",file);
            name = file;
            file = subdir+"\\"+file
            rgbAve, rgbMed, rgbDev, rgbVar = calculeRGBHistogram(file);            
            print("rgbAverage ", rgbAve);
            print("rgbMedian ", rgbMed);
            print("rgbDev ", rgbDev);
            print("rgbVar ", rgbVar);            
            row = ("%s;%s;%.4f;%4.f;%.4f;%.4f;%.4f;%.4f;%.4f;%.4f;%.4f;%.4f;%.4f;%.4f") % (group,
                name, rgbAve[0], rgbAve[1], rgbAve[2], rgbMed[0],
                rgbMed[1], rgbMed[2], rgbDev[0], rgbDev[1], rgbDev[2],
                rgbVar[0], rgbVar[1], rgbVar[2]);            
            writer.writerow([row]);                        
                                        
    elapsedTime = time.time() - startTime;
    outFile.close();
    print("FINISH, ELAPSED TIME(seconds): ",elapsedTime);
    
    
def calculeRGBHistogram(file):
    img = io.imread(file);
    
    #print(img[0])
    '''
    for channel in range(img.shape[2]):  # equalizing each channel
        img[:, :, channel] = exposure.equalize_hist(img[:, :, channel])    
    '''
    #print(np.amin(img[:, :, 0]))
    #print(np.amax(img[:, :, 0]))
    for channel in range(img.shape[2]):
        img[:, :, channel] = exposure.rescale_intensity(img[:, :, channel],
            in_range=(np.amin(img[:, :, channel]), np.amax(img[:, :, channel])), out_range=(0, 255));
    #print(np.amin(img[:, :, 0]))
    #print(np.amax(img[:, :, 0]))
    #print(img[0])
    #time.sleep(10);
    height, width = len(img), len(img[0]);
    r = [];
    g = [];
    b = [];
    for i in range(height):
        for j in range(width): 
            pixel = img[i, j];
            r.append(pixel[0]);
            g.append(pixel[1]);
            b.append(pixel[2]);    
    #r = exposure.equalize_hist(r1);
    #g = exposure.equalize_hist(g1);
    #b = exposure.equalize_hist(b1);
    #average of RGB
    rgbAve = [np.average(r), np.average(g), np.average(b)];
    #median of RGB
    rgbMed = [np.median(r), np.median(g), np.median(b)];
    #variance of RGB
    rgbVar = [np.var(r), np.var(g), np.var(b)];
    #dispersion of RGB
    rgbDev = [np.std(r), np.std(g), np.std(b)];    
    
    return rgbAve, rgbMed, rgbDev, rgbVar;

def makeSeparetedPlot(f):
    inFile = open(f, "r",newline='');
    reader = csv.reader(inFile);  
    first = True;
    second = True;
    t1 = "R";
    t2 = "G";
    t3 = "B";
    group = [];
    qtdGroup = [];
    file = [];
    c1Ave = [];
    c2Ave = [];
    c3Ave = [];
    c1Median = [];
    c2Median = [];
    c3Median = [];
    c1Deviation = [];
    c2Deviation = [];
    c3Deviation = [];
    c1Variance = [];
    c2Variance = [];
    c3Variance = [];
    x = []
    cont = 0;
    for row in reader:
        if(first):
            first = False;            
            if(row[0].endswith("H(VARIANCE);S(VARIANCE);V(VARIANCE); ")):
                t1 = "H";
                t2 = "S";
                t3 = "V";
            elif(row[0].endswith("L(VARIANCE);A(VARIANCE);B(VARIANCE); ")):
                t1 = "L";
                t2 = "A";
                t3 = "B";
            elif(row[0].endswith("L(VARIANCE);U(VARIANCE);V(VARIANCE); ")):
                t1 = "L";
                t2 = "U";
                t3 = "V";
        else:            
            item = row[0].split(";");
            if(second):
                second = False;
                group.append(item[0]);
                file.append(item[1]);
                c1Ave.append(float(item[2]));
                c2Ave.append(float(item[3]));
                c3Ave.append(float(item[4]));
                c1Median.append(float(item[5]));
                c2Median.append(float(item[6]));
                c3Median.append(float(item[7]));
                c1Deviation.append(float(item[8]));
                c2Deviation.append(float(item[9]));
                c3Deviation.append(float(item[10]));
                c1Variance.append(float(item[11]));
                c2Variance.append(float(item[12]));
                c3Variance.append(float(item[13]));
                x.append(cont);
                cont+=1;
            #new group to plot, so plot the actual before
            elif(group[-1] != item[0]):
                qtdGroup.append(cont);
                group.append(item[0]);
                file.append(item[1]);
                c1Ave.append(float(item[2]));
                c2Ave.append(float(item[3]));
                c3Ave.append(float(item[4]));
                c1Median.append(float(item[5]));
                c2Median.append(float(item[6]));
                c3Median.append(float(item[7]));
                c1Deviation.append(float(item[8]));
                c2Deviation.append(float(item[9]));
                c3Deviation.append(float(item[10]));
                c1Variance.append(float(item[11]));
                c2Variance.append(float(item[12]));
                c3Variance.append(float(item[13]));
                x.append(cont);
                cont+=1;
            else:
                file.append(item[1]);
                c1Ave.append(float(item[2]));
                c2Ave.append(float(item[3]));
                c3Ave.append(float(item[4]));
                c1Median.append(float(item[5]));
                c2Median.append(float(item[6]));
                c3Median.append(float(item[7]));
                c1Deviation.append(float(item[8]));
                c2Deviation.append(float(item[9]));
                c3Deviation.append(float(item[10]));
                c1Variance.append(float(item[11]));
                c2Variance.append(float(item[12]));
                c3Variance.append(float(item[13]));
                x.append(cont);
                cont+=1;    
    qtdGroup.append(cont);    
    a = qtdGroup[0];#1: 0      - 149
    b = qtdGroup[1];#2: 150 - 299
    c = qtdGroup[2];#3: 300 - 499
    
    resp = input("save it?(y/n): ");
    #'''
    #AVERAGES
    #c1(Avarage)
    plotOneByOne(t1+"(Average) x Sample", "Sample", t1, group, x, c1Ave, a, b, c, resp);
    #c2(Avarage)
    plotOneByOne(t2+"(Average) x Sample", "Sample", t2, group, x, c2Ave, a, b, c, resp);
    #c3(Avarage)
    plotOneByOne(t3+"(Average) x Sample", "Sample", t3, group, x, c3Ave, a, b, c, resp);    
    #MEDIAN
    #c1(Median)
    plotOneByOne(t1+"(Median) x Sample", "Sample", t1, group, x, c1Median, a, b, c, resp);
    #c2(Median)
    plotOneByOne(t2+"(Median) x Sample", "Sample", t2, group, x, c2Median, a, b, c, resp);
    #c3(Median)
    plotOneByOne(t3+"(Median) x Sample", "Sample", t3, group, x, c3Median, a, b, c, resp);    
    #MODE
    #c1(Mode)
    plotOneByOne(t1+"(Deviation) x Sample", "Sample", t1, group, x, c1Deviation, a, b, c, resp);
    #c2(Mode)
    plotOneByOne(t2+"(Deviation) x Sample", "Sample", t2, group, x, c2Deviation, a, b, c, resp);
    #c3(Mode)
    plotOneByOne(t3+"(Deviation) x Sample", "Sample", t3, group, x, c3Deviation, a, b, c, resp);
    #'''
    newPlot(t1+"(Average) x "+t1+"(Deviation)", t1, t1, group, c1Ave, c1Deviation, a, b, c, resp);
    newPlot(t2+"(Average) x "+t2+"(Deviation)", t2, t2, group, c2Ave, c2Deviation, a, b, c, resp);
    newPlot(t3+"(Average) x "+t3+"(Deviation)", t3, t3, group, c3Ave, c3Deviation, a, b, c, resp);
    
    newPlot(t1+"(Average) x "+t1+"(Variance)", t1, t1, group, c1Ave, c1Variance, a, b, c, resp);
    newPlot(t2+"(Average) x "+t2+"(Variance)", t2, t2, group, c2Ave, c2Variance, a, b, c, resp);
    newPlot(t3+"(Average) x "+t3+"(Variance)", t3, t3, group, c3Ave, c3Variance, a, b, c, resp);
    
    inFile.close();

def newPlot(title, xTitle, yTitle, group, x, y, a, b, c, resp):
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
    if(resp == "y" or resp == "Y"):        
        plt.savefig("..\\plots\\"+title);    
    #plt.show();
    plt.close();
        
    
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
    if(resp == "y" or resp == "Y"):        
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
    c1Ave = [];
    c2Ave = [];
    c3Ave = [];
    c1Median = [];
    c2Median = [];
    c3Median = [];
    c1Deviation = [];
    c2Deviation = [];
    c3Deviation = [];
    c1Variance = [];
    c2Variance = [];
    c3Variance = [];
    x = []
    cont = 0;
    for row in reader:
        if(first):
            first = False;
            if(row[0].endswith("S(VARIANCE);V(VARIANCE) ")):
                t1 = "H";
                t2 = "S";
                t3 = "V";
                name = "ALL_PLOTS_HSV";
            elif(row[0].endswith("B(VARIANCE) ")):
                t1 = "L";
                t2 = "A";
                t3 = "B";
                name = "ALL_PLOTS_LAB";
            elif(row[0].endswith("U(VARIANCE);V(VARIANCE) ")):
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
                c1Ave.append(int(item[2]));
                c2Ave.append(int(item[3]));
                c3Ave.append(int(item[4]));
                c1Median.append(int(item[5]));
                c2Median.append(int(item[6]));
                c3Median.append(int(item[7]));
                c1Deviation.append(int(item[8]));
                c2Deviation.append(int(item[9]));
                c3Deviation.append(int(item[10]));
                c1Variance.append(item[11]);
                c2Variance.append(item[12]);
                c3Variance.append(item[13]);
                x.append(cont);
                cont+=1;
            #new group to plot, so plot the actual before
            elif(group[-1] != item[0]):
                qtdGroup.append(cont);
                group.append(item[0]);
                file.append(item[1]);
                c1Ave.append(int(item[2]));
                c2Ave.append(int(item[3]));
                c3Ave.append(int(item[4]));
                c1Median.append(int(item[5]));
                c2Median.append(int(item[6]));
                c3Median.append(int(item[7]));
                c1Deviation.append(int(item[8]));
                c2Deviation.append(int(item[9]));
                c3Deviation.append(int(item[10]));
                c1Variance.append(item[11]);
                c2Variance.append(item[12]);
                c3Variance.append(item[13]);
                x.append(cont);
                cont+=1;
            else:
                file.append(item[1]);
                c1Ave.append(int(item[2]));
                c2Ave.append(int(item[3]));
                c3Ave.append(int(item[4]));
                c1Median.append(int(item[5]));
                c2Median.append(int(item[6]));
                c3Median.append(int(item[7]));
                c1Deviation.append(int(item[8]));
                c2Deviation.append(int(item[9]));
                c3Deviation.append(int(item[10]));
                c1Variance.append(item[11]);
                c2Variance.append(item[12]);
                c3Variance.append(item[13]);
                x.append(cont);
                cont+=1;    
    qtdGroup.append(cont);
    
    a = qtdGroup[0];#1: 0   - 149
    b = qtdGroup[1];#2: 150 - 299
    c = qtdGroup[2];#3: 300 - 499
    
    plotAxarr(f, axarr, x, c1Ave, c2Ave, c3Ave, c1Median, c2Median, c3Median,
            c1Deviation, c2Deviation, c3Deviation, c1Variance, c2Variance, c3Variance, a, b, c, group, name);
                
    inFile.close();


def makePlotsFloat(f):
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
    c1Ave = [];
    c2Ave = [];
    c3Ave = [];
    c1Median = [];
    c2Median = [];
    c3Median = [];
    c1Deviation = [];
    c2Deviation = [];
    c3Deviation = [];
    c1Variance = [];
    c2Variance = [];
    c3Variance = [];
    x = []
    cont = 0;
    for row in reader:
        if(first):
            first = False;
            if(row[0].endswith("S(VARIANCE);V(VARIANCE) ")):
                t1 = "H";
                t2 = "S";
                t3 = "V";
                name = "ALL_PLOTS_HSV";
            elif(row[0].endswith("B(VARIANCE) ")):
                t1 = "L";
                t2 = "A";
                t3 = "B";
                name = "ALL_PLOTS_LAB";
            elif(row[0].endswith("U(VARIANCE);V(VARIANCE) ")):
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
                c1Ave.append(float(item[2]));
                c2Ave.append(float(item[3]));
                c3Ave.append(float(item[4]));
                c1Median.append(float(item[5]));
                c2Median.append(float(item[6]));
                c3Median.append(float(item[7]));
                c1Deviation.append(float(item[8]));
                c2Deviation.append(float(item[9]));
                c3Deviation.append(float(item[10]));
                c1Variance.append(float(item[11]));
                c2Variance.append(float(item[12]));
                c3Variance.append(float(item[13]));
                x.append(cont);
                cont+=1;
            #new group to plot, so plot the actual before
            elif(group[-1] != item[0]):
                qtdGroup.append(cont);
                group.append(item[0]);
                file.append(item[1]);
                c1Ave.append(float(item[2]));
                c2Ave.append(float(item[3]));
                c3Ave.append(float(item[4]));
                c1Median.append(float(item[5]));
                c2Median.append(float(item[6]));
                c3Median.append(float(item[7]));
                c1Deviation.append(float(item[8]));
                c2Deviation.append(float(item[9]));
                c3Deviation.append(float(item[10]));
                c1Variance.append(float(item[11]));
                c2Variance.append(float(item[12]));
                c3Variance.append(float(item[13]));
                x.append(cont);
                cont+=1;
            else:
                file.append(item[1]);
                c1Ave.append(float(item[2]));
                c2Ave.append(float(item[3]));
                c3Ave.append(float(item[4]));
                c1Median.append(float(item[5]));
                c2Median.append(float(item[6]));
                c3Median.append(float(item[7]));
                c1Deviation.append(float(item[8]));
                c2Deviation.append(float(item[9]));
                c3Deviation.append(float(item[10]));
                c1Variance.append(float(item[11]));
                c2Variance.append(float(item[12]));
                c3Variance.append(float(item[13]));
                x.append(cont);
                cont+=1;    
    qtdGroup.append(cont);
    
    a = qtdGroup[0];#1: 0   - 149
    b = qtdGroup[1];#2: 150 - 299
    c = qtdGroup[2];#3: 300 - 499
    
    plotAxarr(f, axarr, x, c1Ave, c2Ave, c3Ave, c1Median, c2Median, c3Median,
            c1Deviation, c2Deviation, c3Deviation, c1Variance, c2Variance, c3Variance, a, b, c, group, name);
                
    inFile.close();
    

def plotAxarr(f, axarr, x, c1Ave, c2Ave, c3Ave, c1Median, c2Median, c3Median,
            c1Deviation, c2Deviation, c3Deviation, c1Variance, c2Variance, c3Variance, a, b, c, group, name):
    #AVERAGE
    #c1Ava
    axarr[0, 0].scatter(x[0:a-1], c1Ave[0:a-1], label = group[0]);
    axarr[0, 0].scatter(x[a:b-1], c1Ave[a:b-1], label = group[1]);
    axarr[0, 0].scatter(x[b:c-1], c1Ave[b:c-1], label = group[2]);
    axarr[0, 0].legend();
    #c2Ava
    axarr[0, 1].scatter(x[0:a-1], c2Ave[0:a-1], label = group[0]);
    axarr[0, 1].scatter(x[a:b-1], c2Ave[a:b-1], label = group[1]);
    axarr[0, 1].scatter(x[b:c-1], c2Ave[b:c-1], label = group[2]);
    axarr[0, 1].legend();
    #c3Ava
    axarr[0, 2].scatter(x[0:a-1], c3Ave[0:a-1], label = group[0]);
    axarr[0, 2].scatter(x[a:b-1], c3Ave[a:b-1], label = group[1]);
    axarr[0, 2].scatter(x[b:c-1], c3Ave[b:c-1], label = group[2]);
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
    
    #DEVIATION
    #c1Deviation
    axarr[2, 0].scatter(x[0:a-1], c1Deviation[0:a-1], label = group[0]);
    axarr[2, 0].scatter(x[a:b-1], c1Deviation[a:b-1], label = group[1]);
    axarr[2, 0].scatter(x[b:c-1], c1Deviation[b:c-1], label = group[2]);
    axarr[2, 0].legend();
    #c2Deviation
    axarr[2, 1].scatter(x[0:a-1], c2Deviation[0:a-1], label = group[0]);
    axarr[2, 1].scatter(x[a:b-1], c2Deviation[a:b-1], label = group[1]);
    axarr[2, 1].scatter(x[b:c-1], c2Deviation[b:c-1], label = group[2]);
    axarr[2, 1].legend();
    #c3Deviation
    axarr[2, 2].scatter(x[0:a-1], c3Deviation[0:a-1], label = group[0]);
    axarr[2, 2].scatter(x[a:b-1], c3Deviation[a:b-1], label = group[1]);
    axarr[2, 2].scatter(x[b:c-1], c3Deviation[b:c-1], label = group[2]);
    axarr[2, 2].legend();
    
    f.set_size_inches(14,6);
    #f.figsize=(8, 6)            
    plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.6);    
    plt.show();
    


def configAxarr(axarr, t1, t2, t3):
    axarr[0, 0].set_title(t1+"(Average) x Sample");
    axarr[0, 0].set_xlabel("Sample");
    axarr[0, 0].set_ylabel(t1);
    axarr[0, 0].grid();
    axarr[0, 1].set_title(t2+"(Average) x Sample");
    axarr[0, 1].set_xlabel("Sample");
    axarr[0, 1].set_ylabel(t2);
    axarr[0, 1].grid();
    axarr[0, 2].set_title(t3+"(Average) x Sample");
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
    axarr[2, 0].set_title(t1+"(Deviation) x Sample");
    axarr[2, 0].set_xlabel("Sample");
    axarr[2, 0].set_ylabel(t1);
    axarr[2, 0].grid();
    axarr[2, 1].set_title(t2+"(Deviation) x Sample");
    axarr[2, 1].set_xlabel("Sample");
    axarr[2, 1].set_ylabel(t2);
    axarr[2, 1].grid();
    axarr[2, 2].set_title(t3+"(Deviation) x Sample");
    axarr[2, 2].set_xlabel("Sample");
    axarr[2, 2].set_ylabel(t3);
    axarr[2, 2].grid();
    
#calculateRGB();
#calculateGrey();
#calculateHSV();
#calculateLAB();
#calculateLUV();
#makePlotsFloat("..\\outputRGB.csv");
makeSeparetedPlot("..\\outputLUV.csv");







