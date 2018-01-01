from __future__ import print_function;
from skimage import color, io;
import os, time, csv;
import numpy as np;


def validationPAMS():
    startTime = time.time();
    outFile = open("..\\outAH.csv", "w",newline='');
    writer = csv.writer(outFile, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL);
    writer.writerow(["GROUP;NAME;A(AVERAGE);A(MEDIAN);H(AVERAGE);H(MEDIAN);"]);
    for subdir, dirs, files in os.walk(os.path.abspath(os.path.join('.\\', os.pardir))+'\\Images\\'):
        group = subdir.split("\\")[-1];
        print(subdir);
        for file in files:
            print("\t",file);
            name = file;
            file = subdir+"\\"+file
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



validationPAMS();



