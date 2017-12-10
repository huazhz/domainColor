#from __future__ import print_function;
from matplotlib import pyplot as plt;
from skimage import io, exposure;
from scipy import sparse;
import os, time, pickle;
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import classification_report, confusion_matrix;
import numpy as np; 

labelHEE = 0;
labelPAS = 1;
qtdDataTrainning = 530;
qtdDataTestHEE = 223;
qtdDataTestPAS = 30;

def makePlots():
    channels = ["RB", "RG", "GB", "RGB"];
    numberOfShifts = [3, 4, 5, 6];    
    dataRB = np.zeros((4,3,3), dtype=np.float32);
    dataRG = np.zeros((4,3,3), dtype=np.float32);
    dataGB = np.zeros((4,3,3), dtype=np.float32);
    dataRGB = np.zeros((4,3,3), dtype=np.float32);     
    for n in numberOfShifts:
        dataRB[n-3] = testKNN("RB", n);
        dataRG[n-3] = testKNN("RG", n);
        dataGB[n-3] = testKNN("GB", n);
        dataRGB[n-3] = testKNN("RGB", n);
    
    plotOneByOne("RG", "n of shitfs", "proportion of each variable", dataRB);

def plotOneByOne(title, xTitle, yTitle, data):
    fig, ax = plt.subplots();
    plt.title(title);
    plt.xlabel(xTitle);
    plt.ylabel(yTitle);
    plt.plot([3,4,5,6], data[:,0,:], label= "H&E CLASS")
    plt.plot([3,4,5,6], data[:,1,:], label= "PAS CLASS")
    plt.plot([3,4,5,6], data[:,2,:], label= "ALL CLASSES")    
    plt.legend();
    plt.grid(True);
    #fig.set_size_inches(14,6)        
    plt.show();
    plt.close();
    
    
def testKNN(channels, numberOfShifts):
    startTime = time.time();                     
    fHEE = "..\\Logs\\3\\Teste\\"+channels+"\\test"+channels+"_"+str(numberOfShifts)+"HistogramColors_H&E.bin";
    fPAS = "..\\Logs\\3\\Teste\\"+channels+"\\test"+channels+"_"+str(numberOfShifts)+"HistogramColors_PAS.bin";
    fKNN = "..\\trainedKNN_"+str(numberOfShifts)+"HistogramColors_"+channels+".bin";
    inFHEE = open(fHEE, 'rb');
    inFPAS = open(fPAS, 'rb');
    fileKNN = open(fKNN, 'rb');
    base = 256>>numberOfShifts;

    knn5 = pickle.load(fileKNN);
    knn10 = pickle.load(fileKNN);
    knn15 = pickle.load(fileKNN);
    knn20 = pickle.load(fileKNN);                
        
    y_true = np.zeros((qtdDataTestHEE + qtdDataTestPAS), dtype=np.int);
    y_pred5 = np.zeros((qtdDataTestHEE + qtdDataTestPAS), dtype=np.int);
    y_pred10 = np.zeros((qtdDataTestHEE + qtdDataTestPAS), dtype=np.int);
    y_pred15 = np.zeros((qtdDataTestHEE + qtdDataTestPAS), dtype=np.int);
    y_pred20 = np.zeros((qtdDataTestHEE + qtdDataTestPAS), dtype=np.int);
    data = np.zeros((qtdDataTestHEE + qtdDataTestPAS, base*base), dtype=np.float32);
    if(len(channels) == 3):
            data = np.zeros((qtdDataTestHEE + qtdDataTestPAS, base*base*base), dtype=np.float32);    
    
    for i in range(qtdDataTestHEE):
        data[i] = linearize(base, pickle.load(inFHEE), channels);
        y_true[i] = labelHEE;
    for i in range(qtdDataTestPAS):
        data[qtdDataTestHEE+i] = linearize(base, pickle.load(inFPAS), channels);        
        y_true[qtdDataTestHEE+i] = labelPAS;
    
    y_pred5[ :qtdDataTestHEE] = knn5.predict(data[ :qtdDataTestHEE]);
    y_pred10[ :qtdDataTestHEE] = knn10.predict(data[ :qtdDataTestHEE]);
    y_pred15[ :qtdDataTestHEE] = knn15.predict(data[ :qtdDataTestHEE]);
    y_pred20[ :qtdDataTestHEE] = knn20.predict(data[ :qtdDataTestHEE]);
    
    y_pred5[qtdDataTestHEE: ] = knn5.predict(data[qtdDataTestHEE: ]);
    y_pred10[qtdDataTestHEE: ] = knn10.predict(data[qtdDataTestHEE: ]);
    y_pred15[qtdDataTestHEE: ] = knn15.predict(data[qtdDataTestHEE: ]);
    y_pred20[qtdDataTestHEE: ] = knn20.predict(data[qtdDataTestHEE: ]);
    
    target_names = ['HEE', 'PAS'];
    #print("menor   ", y_true[ :qtdDataTestHEE ]);
    #print("maior   ", y_true[qtdDataTestHEE: ]);
    
    elapsedTime = time.time() - startTime;
    print(fKNN);
    print("TIME: ",elapsedTime);
    
    print("CLASSIFICATION FOR KNN, K = 5\n"+classification_report(y_true, y_pred5, target_names=target_names));
    print("CLASSIFICATION FOR KNN, K = 10\n"+classification_report(y_true, y_pred10, target_names=target_names));
    print("CLASSIFICATION FOR KNN, K = 15\n"+classification_report(y_true, y_pred15, target_names=target_names));
    print("CLASSIFICATION FOR KNN, K = 20\n"+classification_report(y_true, y_pred20, target_names=target_names));    
    '''
    print("\nCONFUSION MATRIX FOR KNN, K = 5 (tn, fp, fn, tp)")
    print(confusion_matrix(y_true, y_pred5).ravel())
    print("\nCONFUSION MATRIX FOR KNN, K = 10 (tn, fp, fn, tp)")
    print(confusion_matrix(y_true, y_pred10).ravel())
    print("\nCONFUSION MATRIX FOR KNN, K = 15 (tn, fp, fn, tp)")
    print(confusion_matrix(y_true, y_pred15).ravel())
    print("\nCONFUSION MATRIX FOR KNN, K = 20 (tn, fp, fn, tp)")
    print(confusion_matrix(y_true, y_pred20).ravel())
    '''
    inFHEE.close();
    inFPAS.close();
    fileKNN.close();
    
    text = classification_report(y_true, y_pred5, target_names=target_names);
    text = text.split('    ');
    
    HEEStatiscs = [text[7], text[8], text[9]];
    PASStatiscs = [text[13], text[14], text[15]];
    ALLStatis = [text[18], text[19], text[20]];
    
    return HEEStatiscs, PASStatiscs, ALLStatis;     
    
        
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
    

def traineKNN(channels, numberOfShifts):    
    fHEE = "..\\Logs\\3\\Treinamento\\"+channels+"\\output"+channels+"_"+str(numberOfShifts)+"HistogramColors_H&E.bin";
    fPAS = "..\\Logs\\3\\Treinamento\\"+channels+"\\output"+channels+"_"+str(numberOfShifts)+"HistogramColors_PAS.bin";
    inFHEE = open(fHEE, 'rb');
    inFPAS = open(fPAS, 'rb');
    print("Training KNN to channels "+channels+" with "+str(numberOfShifts)+" shifts");
    #vHEE = [];
    #vPAS = [];
    base = 256>>numberOfShifts;    
    X = [];
    y = [];
    '''
    X = np.zeros((265*2), dtype=np.float32);
    y = np.zeros((2), dtype=np.int)
    '''
    for i in range(int(qtdDataTrainning/2)):
        '''        
        print(i);
        if(i==0):
            X = np.concatenate([pickle.load(inFHEE), pickle.load(inFPAS)], axis=0);
            y = np.concatenate([labelHEE, labelPAS], axis=0);            
        else:
            X = np.concatenate([X, pickle.load(inFHEE), pickle.load(inFPAS)], axis=0)
            y = np.concatenate([y, labelHEE, labelPAS], axis=0);
        time.sleep(2);
        '''
        #vHEE.append(pickle.load(inFHEE));
        #vPAS.append(pickle.load(inFPAS));                
        X.append(pickle.load(inFHEE));
        y.append(labelHEE);
        X.append(pickle.load(inFPAS));
        y.append(labelPAS);
        '''
        if(i<265):
            X[i] = pickle.load(inFHEE);
            y[i] = labelHEE;
        else:
            X[i] = pickle.load(inFPAS);
            y[i] = labelPAS;
        '''
    inFHEE.close();
    inFPAS.close();
    '''
    print(X[0]);
    print(len(X));
    print(len(X[0]));    
    print(len(X[0][0]));
    print(X[0][0]);
    print(y[0]);
    '''
    X1  = linearizeTraining(base, channels, X);    
    y1 = np.array(y);
    knn5 = KNeighborsClassifier(n_neighbors=5);
    knn10 = KNeighborsClassifier(n_neighbors=10);
    knn15 = KNeighborsClassifier(n_neighbors=15);
    knn20 = KNeighborsClassifier(n_neighbors=20);        
    kf = KFold(n_splits=10);
    print(len(y1), len(X1))
    
    for k, (train, test) in enumerate(kf.split(X1, y1)):  
        print("TRAIN:", train, " - TEST:", test);
        knn5.fit(X1[train], y1[train]);
        knn10.fit(X1[train], y1[train]);
        knn15.fit(X1[train], y1[train]);
        knn20.fit(X1[train], y1[train]);
        print("K ->",k);
        
        print(knn5.score(X1[test], y1[test]));
        print(knn10.score(X1[test], y1[test]));
        print(knn15.score(X1[test], y1[test]));
        print(knn20.score(X1[test], y1[test]));
    
    knnFile = open("..\\trainedKNN_"+str(numberOfShifts)+"HistogramColors_"+channels+".bin", "wb");
    print(knn5.get_params());
    print(knn10.get_params());
    print(knn15.get_params());
    print(knn20.get_params());    
    pickle.dump(knn5, knnFile);    
    pickle.dump(knn10, knnFile);    
    pickle.dump(knn15, knnFile);    
    pickle.dump(knn20, knnFile);
    knnFile.close();
    
    
def linearizeTraining(base, channels, X):    
    if(len(channels) == 3):
        X1 = np.zeros((qtdDataTrainning, base*base*base), dtype=np.float32);        
        for i in range(qtdDataTrainning):
            a = []
            for j in range(base):
                for k in range(base):
                    for l in range(base):
                        a.append(X[i][j][k][l]);            
            X1[i] = a;
        return X1;
    elif(len(channels) == 2):
        X1 = np.zeros((qtdDataTrainning, base*base), dtype=np.float32);        
        for i in range(qtdDataTrainning):
            a = []
            for j in range(base):
                for k in range(base):
                    a.append(X[i][j][k]);            
            X1[i] = a;
        return X1;
   
def calculateRGBColor(n, isTest):
    startTime = time.time();
    #outFileRG = open("..\\outputRG_"+str(n)+"HistogramColors.bin", "wb");
    #outFileRB = open("..\\outputRB_"+str(n)+"HistogramColors.bin", "wb");
    #outFileGB = open("..\\outputGB_"+str(n)+"HistogramColors.bin", "wb");
    #outFileRGB = open("..\\outputRGB_"+str(n)+"HistogramColors.bin", "wb");
    a = "output";
    if(isTest):
            a = "test";        
    for subdir, dirs, files in os.walk(os.path.abspath(os.path.join('.\\', os.pardir))+'\\Images\\'):
        group = subdir.split("\\")[-1];
        outFileRG = open("..\\"+a+"RG_"+str(n)+"HistogramColors_"+group+".bin", "wb");
        outFileRB = open("..\\"+a+"RB_"+str(n)+"HistogramColors_"+group+".bin", "wb");
        outFileGB = open("..\\"+a+"GB_"+str(n)+"HistogramColors_"+group+".bin", "wb");
        outFileRGB = open("..\\"+a+"RGB_"+str(n)+"HistogramColors_"+group+".bin", "wb");        
        print(subdir);
        for file in files:
            print("\t",file);
            #name = file;
            file = subdir+"\\"+file
            rg, rb, gb, rgb = calculeRGBColorHistogram(file, n);
            
            pickle.dump(rg, outFileRG);
            pickle.dump(rb, outFileRB);
            pickle.dump(gb, outFileGB);
            pickle.dump(rgb, outFileRGB);
        outFileRG.close();
        outFileRB.close();
        outFileGB.close();
        outFileRGB.close();                 
    elapsedTime = time.time() - startTime;
    #outFileRG.close();
    #outFileRB.close();
    #outFileGB.close();
    #outFileRGB.close();
    print("FINISH, ELAPSED TIME(seconds): ",elapsedTime);
    
    
def calculeRGBColorHistogram(file, n):
    img = io.imread(file);
    height, width = len(img), len(img[0]);
    size = height*width;
    base = 256>>n
    for channel in range(img.shape[2]):
        img[:, :, channel] = exposure.rescale_intensity(img[:, :, channel],
            in_range=(np.amin(img[:, :, channel]), np.amax(img[:, :, channel])), out_range=(0, 255));
    
    rb = np.zeros((base, base), dtype=np.float32);
    rg = np.zeros((base, base), dtype=np.float32);
    gb = np.zeros((base, base), dtype=np.float32);
    rgb = np.zeros((base, base, base), dtype=np.float32);
    for i in range(height):
        for j in range(width):
            pixel = img[i, j];
            r = pixel[0];
            g= pixel[1];
            b = pixel[2];
            r1 = r>>n;
            g1 = g>>n;
            b1 = b>>n;
           
            rb[r1][b1]+=1;            
            rg[r1][g1]+=1;
            gb[g1][g1]+=1;
            rgb[r1][g1][b1]+=1;
                        
    rb = np.divide(rb, size);
    rb = np.multiply(rb, 100);
    gb = np.divide(gb, size);
    gb = np.multiply(gb, 100);
    rg = np.divide(rg, size);
    rg = np.multiply(rg, 100);
    rgb = np.divide(rgb, size);
    rgb = np.multiply(rgb, 100.0);
    
    '''
    print(rb);
    print(type(rb));
    print(type(rb[0]));
    print(type(rb[0][0]));
    print(len(rb));
    '''
    return np.float32(rb), np.float32(rg), np.float32(gb), np.float32(rgb);    


#calculateRGBColor(n=1, isTest=True);
#traineKNN(channels="GB", numberOfShifts=2);
#testKNN(channels="RGB", numberOfShifts=4);
makePlots();





