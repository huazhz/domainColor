from __future__ import print_function;
from skimage import color, io, exposure;
from sklearn.metrics import classification_report;
import os, time, csv, pickle;
import numpy as np;

labelPAMS = 0;
labelNotPAMS = 1;


def validationPAMS():
    startTime = time.time();
    outFile = open("..\\outAH MEMBRANOUS DATASET.csv", "w", newline='');
    writer = csv.writer(outFile, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL);
    writer.writerow(["GROUP;NAME;A(AVERAGE);A(MEDIAN);H(AVERAGE);H(MEDIAN);"]);
    for subdir, dirs, files in os.walk(os.path.abspath(os.path.join('.\\', os.pardir))+'\\Images\\'):
        group = subdir.split("\\")[-1];
        print(subdir);
        for file in files:
            print("\t",file);
            name = file;
            file = subdir+"\\"+file;
            aAve, aMed, hAve, hMed = calculatePAMS(file);
            print("aAve ", aAve);
            print("aMed ", aMed);
            print("hAve ", hAve);
            print("hMed ", hMed);                                    
            row = ("%s;%s;%.4f;%4.f;%.4f;%.4f") % (group, name, aAve, aMed, hAve, hMed);
            writer.writerow([row]);
                                        
    elapsedTime = time.time() - startTime;
    outFile.close();
    print("FINISH, ELAPSED TIME(seconds): ",elapsedTime);


def calculatePAMS(file):
    img = io.imread(file);
    height, width = len(img), len(img[0]);
    hsvImage = color.rgb2hsv(img);
    labImage = color.rgb2lab(img);

    h = [];
    a = [];    
    for i in range(height):
        for j in range(width):
            hsv = hsvImage[i,j];
            lab = labImage[i,j];
            h.append(hsv[0]*359);
            a.append(lab[1]);            
    aAve = np.nanmean(a);
    aMed = np.nanmedian(a);
    hAve = np.nanmean(h);
    hMed = np.nanmedian(h);    
    
    return aAve, aMed, hAve, hMed;


def calculateLABColor(isTest):
    startTime = time.time();
    a = "output";
    if(isTest):
            a = "test";        
    for subdir, dirs, files in os.walk(os.path.abspath(os.path.join('.\\', os.pardir))+'\\Images\\'):
        group = subdir.split("\\")[-1];
        outFileAB5 = open("..\\"+a+"AB_5HistogramColors_"+group+".bin", "wb");
        outFileAB6 = open("..\\"+a+"AB_6HistogramColors_"+group+".bin", "wb");
        print(subdir); 
        for file in files:
            print("\t",file);
            file = subdir+"\\"+file
            ab5, ab6 = calculeLABColorHistogram(file);            
            pickle.dump(ab5, outFileAB5);
            pickle.dump(ab6, outFileAB6);        
        outFileAB5.close();
        outFileAB6.close();
    elapsedTime = time.time() - startTime;    
    print("FINISH, ELAPSED TIME(seconds): ",elapsedTime);
    
    
def calculeLABColorHistogram(file):
    img = io.imread(file);
    height, width = len(img), len(img[0]);    
    size = height*width;
    labImage = color.rgb2lab(img);        
    #fazendo a equalização de histograma
    labImage[:, :, 0] = exposure.rescale_intensity(labImage[:, :, 0],
        in_range=(np.amin(labImage[:, :, 0]), np.amax(labImage[:, :, 0])), out_range=(0, 100));
    labImage[:, :, 1] = exposure.rescale_intensity(labImage[:, :, 1],
        in_range=(np.amin(labImage[:, :, 1]), np.amax(labImage[:, :, 1])), out_range=(-128, 127));
    labImage[:, :, 2] = exposure.rescale_intensity(labImage[:, :, 2],
        in_range=(np.amin(labImage[:, :, 2]), np.amax(labImage[:, :, 2])), out_range=(-128, 127));  
        
    ab5 = np.zeros((8, 8), dtype=np.float32);
    ab6 = np.zeros((4, 4), dtype=np.float32);
    for i in range(height):
        for j in range(width):
            pixel = labImage[i, j];
            a = 128 + int(pixel[1]);
            b = 128 + int(pixel[2]);                            
            ab5[a>>5][b>>5]+=1;
            ab6[a>>6][b>>6]+=1;
                                        
    ab5 = np.divide(ab5, size);
    ab5 = np.multiply(ab5, 100);
    ab6 = np.divide(ab6, size);
    ab6 = np.multiply(ab6, 100);
            
    ab5 = np.float32(linearize(8, ab5, "AB"));
    ab6 = np.float32(linearize(4, ab6, "AB"));
    return ab5, ab6;


def linearize(base, data, channels):
    cont = 0;
    if(len(channels) == 3):
        X1 = np.zeros((base*base*base), dtype=np.float32);
        for i in range(base):
            for j in range(base):
                for k in range(base):
                    X1[cont] = data[i][j][k];
                    cont+=1;
        return X1;
    elif(len(channels) == 2):
        X1 = np.zeros((base*base), dtype=np.float32);
        for i in range(base):
            for j in range(base):                
                    X1[cont] = data[i][j];
                    cont+=1;
        return X1;


def testPams(f):
    lim_h_Average = [i for i in range(150, 251, 5)];
    lim_h_Median  = [i for i in range(200, 301, 5)];
    lim_a_Average = [i for i in range(0, 21, 1)];
    lim_a_Median  = [i for i in range(0, 21, 1)];
    '''
    print(lim_h_Average)
    print(lim_h_Median)
    print(lim_a_Average)
    print(lim_a_Median)
    time.sleep(10)
    #'''    
    outFile = open("..\\outTestPams.csv", "w",newline='');
    writer = csv.writer(outFile, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL);
    writer.writerow(["VARIABLE;VALUE;PAMS PRECISION;NOT PAMS PRECISION;PAMS RECALL;NOT PAMS RECALL;"+
                    "PAMS F1-SCORE;NOT PAMS F1-SCORE"]);
                     
    for boundary in lim_h_Average:        
        pamsPrecision, pamsRecall, pamsF1, nPamsPrecision, nPamsRecall, nPamsF1 = testBoundary(f, boundary, 0);
        row = ("%s;%d;%s;%s;%s;%s;%s;%s") % ("Average of H", boundary, pamsPrecision, nPamsPrecision,
                                             pamsRecall, nPamsRecall, pamsF1, nPamsF1);
        writer.writerow([row]);
    
    for boundary in lim_h_Median:        
        pamsPrecision, pamsRecall, pamsF1, nPamsPrecision, nPamsRecall, nPamsF1 = testBoundary(f, boundary, 1);
        row = ("%s;%d;%s;%s;%s;%s;%s;%s") % ("Median of H", boundary, pamsPrecision, nPamsPrecision,
                                             pamsRecall, nPamsRecall, pamsF1, nPamsF1);
        writer.writerow([row]);
    
    for boundary in lim_a_Average:        
        pamsPrecision, pamsRecall, pamsF1, nPamsPrecision, nPamsRecall, nPamsF1 = testBoundary(f, boundary, 2);
        row = ("%s;%d;%s;%s;%s;%s;%s;%s") % ("Average of A", boundary, pamsPrecision, nPamsPrecision,
                                             pamsRecall, nPamsRecall, pamsF1, nPamsF1);
        writer.writerow([row]);
        
    for boundary in lim_a_Median:        
        pamsPrecision, pamsRecall, pamsF1, nPamsPrecision, nPamsRecall, nPamsF1 = testBoundary(f, boundary, 3);
        row = ("%s;%d;%s;%s;%s;%s;%s;%s") % ("Median of A", boundary, pamsPrecision, nPamsPrecision,
                                             pamsRecall, nPamsRecall, pamsF1, nPamsF1);
        writer.writerow([row]);
    
    outFile.close();
        
def testBoundary(f, boundary, type):    
    inFile = open(f, "r",newline='');
    reader = csv.reader(inFile);
    first = True;
    y_true = np.zeros(502, dtype=np.int);
    y_pred = np.zeros(502, dtype=np.int);
    i = 0;
    for row in reader:
        items = row[0].split(";");
        if(first):
            first = False;            
        else:                        
            group = items[0];
            name = items[1];
            aAve = float(items[2]);
            aMed = float(items[3]);
            hAve = float(items[4]);
            hMed = float(items[5]);            
            if(group == " PAMS"):
                y_true[i] = labelPAMS;                
            else:
                y_true[i] = labelNotPAMS;
            if(type == 0):             
                y_pred[i] = predictPamsNPams(hAve, boundary);
            elif(type == 1):
                y_pred[i] = predictPamsNPams(hMed, boundary);
            elif(type == 2):
                y_pred[i] = predictPamsNPams(aAve, boundary);
            elif(type == 3):
                y_pred[i] = predictPamsNPams(aMed, boundary);
            i+=1;    
    target_names = ['PAMS', 'Not PAMS'];
    resp = classification_report(y_true, y_pred, target_names=target_names)
    print(resp);    
    
    x = resp.split('    ');    
    
    return x[6], x[7], x[8], x[11], x[12], x[13];
    '''
    cont = 0;
    for x in resp.split('    '):
        print(str(cont)+"-"+x);
        cont+=1;
    time.sleep(10)
    '''

    
def predictPamsNPams(value, boundary):
    if(value <= boundary):
        return labelPAMS;
    else:
        return labelNotPAMS;


def defineStaining(f, fSVM, abFile):
    outFile = open("..\\a.csv", "w", newline='');
    writer = csv.writer(outFile, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL);
    writer.writerow(["NAME;PREDICTED GROUP"]);
    inFile = open(f, "r",newline='');
    reader = csv.reader(inFile);
    
    fileSVM = open(fSVM, 'rb');
    svm = pickle.load(fileSVM);
        
    fileAB = open(abFile, 'rb');    
    
    first = True;
    for row in reader:
        items = row[0].split(";");
        if(first):
            first = False;            
        else:                        
            group = items[0];
            name = items[1];
            aAve = float(items[2]);
            aMed = float(items[3]);
            hAve = float(items[4]);
            hMed = float(items[5]);
            a = pickle.load(fileAB);
            #print(len(a))
            #print(a)
            resp = svm.predict( [a] );
            p = makePrediction(hMed, resp);
            print(name);
            print("\t"+p);
            #time.sleep(10);
            row = name+";"+p;
            #row = ("%s") % (name+";"+p);
            writer.writerow([row]);
            
    outFile.close()
    inFile.close()
    fileAB.close()
    fileSVM.close()

def makePrediction(hMedian, pred):
    boundary = 255;
    if(hMedian <= boundary):
        return "PAMS";
    #NOT PAMS
    else:
        if(pred == 0):
            return "HEE";
        elif(pred == 1):
            return "PAS";
'''
def makePredictionAMedian4(aMedian):
    boundary = 4;
    if(aMedian <= boundary):
        return "PAMS";
    #NOT PAMS
    else: 
''' 


defineStaining("..\\outAH MEMBRANOUS DATASET.csv", "..\\trainedSVM_SVC_6HistogramColors_AB.bin",               
               "..\\outputAB_6HistogramColors_MEMBRANOUS DATASET.bin");
#validationPAMS();
#calculateLABColor(isTest=False);
#testPams("..\\outAH.csv");

