from __future__ import print_function;
from skimage import color, io, exposure;
import os, time, csv, sys, pickle;
from matplotlib import pyplot as plt;
import numpy as np; 

   
def calculateRGBColor():
    startTime = time.time();
    outFile = open("..\\outputRGBHistogramColors.bin", "wb");
    
    for subdir, dirs, files in os.walk(os.path.abspath(os.path.join('.\\', os.pardir))+'\\Images\\'):
        group = subdir.split("\\")[-1];
        print(subdir);
        for file in files:
            print("\t",file);
            name = file;
            file = subdir+"\\"+file
            rb, rg, gb, rgb = calculeRGBColorHistogram(file);                            
            pickle.dump(rb, outFile);
            pickle.dump(rg, outFile);
            pickle.dump(gb, outFile);
            pickle.dump(rgb, outFile);
            elapsedTime = time.time() - startTime;
            outFile.close();
            print("FINISH, ELAPSED TIME(seconds): ",elapsedTime);
            sys.exit();
            
    elapsedTime = time.time() - startTime;
    outFile.close();
    print("FINISH, ELAPSED TIME(seconds): ",elapsedTime);
    
    
def calculeRGBColorHistogram(file):
    img = io.imread(file);
    height, width = len(img), len(img[0]);
    size = height*width;
    for channel in range(img.shape[2]):
        img[:, :, channel] = exposure.rescale_intensity(img[:, :, channel],
            in_range=(np.amin(img[:, :, channel]), np.amax(img[:, :, channel])), out_range=(0, 255));
    
    rb1 = np.zeros((128, 128), dtype=np.float64);
    rg1 = np.zeros((128, 128), dtype=np.float64);
    gb1 = np.zeros((128, 128), dtype=np.float64);
    
    rb2 = np.zeros((64, 64), dtype=np.float64);
    rg2 = np.zeros((64, 64), dtype=np.float64);
    gb2 = np.zeros((64, 64), dtype=np.float64);
    
    rb3 = np.zeros((32, 32), dtype=np.float64);
    rg3 = np.zeros((32, 32), dtype=np.float64);
    gb3 = np.zeros((32, 32), dtype=np.float64);
    
    rb4 = np.zeros((16, 16), dtype=np.float64);
    rg4 = np.zeros((16, 16), dtype=np.float64);
    gb4 = np.zeros((16, 16), dtype=np.float64);
    
    rb5 = np.zeros((8, 8), dtype=np.float64);
    rg5 = np.zeros((8, 8), dtype=np.float64);
    gb5 = np.zeros((8, 8), dtype=np.float64);
    
    rb6 = np.zeros((4, 4), dtype=np.float64);
    rg6 = np.zeros((4, 4), dtype=np.float64);
    gb6 = np.zeros((4, 4), dtype=np.float64);
    
    rgb1 = np.zeros((128, 128, 128), dtype=np.float64);
    rgb2 = np.zeros((65, 64, 64), dtype=np.float64);
    rgb3 = np.zeros((32, 32, 32), dtype=np.float64);
    rgb4 = np.zeros((16, 16, 16), dtype=np.float64);
    rgb5 = np.zeros((8, 8, 8), dtype=np.float64);
    rgb6 = np.zeros((4, 4, 4), dtype=np.float64);
    #rb1 = [[0 for i in range(128)] for j in range(128)];
    #rg1 = [[0 for i in range(128)] for j in range(128)];
    #gb1 = [[0 for i in range(128)] for j in range(128)];
    
    #rb2 = [[0 for i in range(64)] for j in range(64)];
    #rg2 = [[0 for i in range(64)] for j in range(64)];
    #gb2 = [[0 for i in range(64)] for j in range(64)];
    
    #rb3 = [[0 for i in range(32)] for j in range(32)];
    #rg3 = [[0 for i in range(32)] for j in range(32)];
    #gb3 = [[0 for i in range(32)] for j in range(32)];
    
    #rb4 = [[0 for i in range(16)] for j in range(16)];
    #rg4 = [[0 for i in range(16)] for j in range(16)];
    #gb4 = [[0 for i in range(16)] for j in range(16)];
    
    #rb5 = [[0 for i in range(8)] for j in range(8)];
    #rg5 = [[0 for i in range(8)] for j in range(8)];
    #gb5 = [[0 for i in range(8)] for j in range(8)];
    
    #rb6 = [[0 for i in range(4)] for j in range(4)];
    #rg6 = [[0 for i in range(4)] for j in range(4)];
    #gb6 = [[0 for i in range(4)] for j in range(4)];
    
    #rgb3 = [[[0 for i in range(32)] for j in range(32)] for k in range(32)];
    #rgb4 = [[[0 for i in range(16)] for j in range(16)] for k in range(16)];
    #rgb5 = [[[0 for i in range(8)] for j in range(8)] for k in range(8)];
    #rgb6 = [[[0 for i in range(4)] for j in range(4)] for k in range(4)];
    
    for i in range(height):
        for j in range(width):
            pixel = img[i, j];
            r = pixel[0];
            g= pixel[1];
            b = pixel[2];
            r1 = r>>1;
            g1 = g>>1;
            b1 = b>>1;
            r2 = r>>2;
            g2 = g>>2;
            b2 = b>>2;
            r3 = r>>3;
            g3 = g>>3;
            b3 = b>>3;
            r4 = r>>4;
            g4 = g>>4;
            b4 = b>>4;
            r5 = r>>5;
            g5 = g>>5;
            b5 = b>>5;
            r6 = r>>6;
            g6 = g>>6;
            b6 = b>>6;
            
            rg1[r1][g1]+=1;
            rb1[r1][b1]+=1;
            gb1[g1][g1]+=1;
            
            rg2[r2][g2]+=1;
            rb2[r2][b2]+=1;
            gb2[g2][g2]+=1;
            
            rg3[r3][g3]+=1;
            rb3[r3][b3]+=1;
            gb3[g3][g3]+=1;
            
            rg4[r4][g4]+=1;
            rb4[r4][b4]+=1;
            gb4[g4][g4]+=1;
            
            rg5[r5][g5]+=1;
            rb5[r5][b5]+=1;
            gb5[g5][g5]+=1;
            
            rg6[r6][g6]+=1;
            rb6[r6][b6]+=1;
            gb6[g6][g6]+=1;
            
            rgb1[r1][g1][b1]+=1;
            rgb2[r2][g2][b2]+=1;
            rgb3[r3][g3][b3]+=1;
            rgb4[r4][g4][b4]+=1;            
            rgb5[r5][g5][b5]+=1;
            rgb6[r6][g6][b6]+=1;                        
        
    rb1 = np.divide(rb1, size);
    rb1 = np.multiply(rb1, 100);
    rg1 = np.divide(rg1, size);
    rg1 = np.multiply(rg1, 100);
    gb1 = np.divide(gb1, size);
    gb1 = np.multiply(gb1, 100);
    
    rb2 = np.divide(rb2, size);
    rb2 = np.multiply(rb2, 100);
    rg2 = np.divide(rg2, size);
    rg2 = np.multiply(rg2, 100);
    gb2 = np.divide(gb2, size);
    gb2 = np.multiply(gb2, 100);
    
    rb3 = np.divide(rb3, size);
    rb3 = np.multiply(rb3, 100);
    rg3 = np.divide(rg3, size);
    rg3 = np.multiply(rg3, 100);
    gb3 = np.divide(gb3, size);
    gb3 = np.multiply(gb3, 100);
    
    rb4 = np.divide(rb4, size);
    rb4 = np.multiply(rb4, 100);
    rg4 = np.divide(rg4, size);
    rg4 = np.multiply(rg4, 100);
    gb4 = np.divide(gb4, size);
    gb4 = np.multiply(gb4, 100);
    
    rb5 = np.divide(rb5, size);
    rb5 = np.multiply(rb5, 100);
    rg5 = np.divide(rg5, size);
    rg5 = np.multiply(rg5, 100);
    gb5 = np.divide(gb5, size);
    gb5 = np.multiply(gb5, 100);
    
    rb6 = np.divide(rb6, size);
    rb6 = np.multiply(rb6, 100.0);
    rg6 = np.divide(rg6, size);
    rg6 = np.multiply(rg6, 100.0);
    gb6 = np.divide(gb6, size);
    gb6 = np.multiply(gb6, 100.0);
    
    rgb1 = np.divide(rgb1, size);
    rgb1 = np.multiply(rgb1, 100.0);
    rgb2 = np.divide(rgb2, size);
    rgb2 = np.multiply(rgb2, 100.0);
    rgb3 = np.divide(rgb3, size);
    rgb3 = np.multiply(rgb3, 100.0);
    rgb4 = np.divide(rgb4, size);
    rgb4 = np.multiply(rgb4, 100.0);
    rgb5 = np.divide(rgb5, size);
    rgb5 = np.multiply(rgb5, 100.0);
    rgb6 = np.divide(rgb6, size);
    rgb6 = np.multiply(rgb6, 100.0);
    
    
    rb = [rb1, rb2, rb3, rb4, rb5, rb6];
    rg = [rg1, rg2, rg3, rg4, rg5, rg6];
    gb = [gb1, gb2, gb3, gb4, gb5, gb6];
    rgb = [rgb1, rgb2, rgb3, rgb4, rgb5, rgb6];
    
    print("rg6")
    print(rg6)
    print(np.sum(rg6))
    print("rb6")
    print(rb6)
    print(np.sum(rb6))
    print("gb6")
    print(gb6)
    print(np.sum(gb6))
    print("rgb6")
    print(rgb6)
    print(np.sum(rgb6))
    
    return rb, rg, gb, rgb;


        
calculateRGBColor();
#calculateGrey();
#calculateHSV();
#calculateLAB();
#calculateLUV();







