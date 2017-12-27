from matplotlib import pyplot as plt;
from skimage import color, io, exposure;
import os, time, pickle;
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import classification_report, confusion_matrix;
from sklearn.svm import SVC;
import numpy as np; 

labelHEE = 0;
labelPAS = 1;
qtdDataTrainning = 530;
qtdDataTestHEE = 223;
qtdDataTestPAS = 30;

def testSVM(channels, numberOfShifts):
    startTime = time.time();                     
    fHEE = "..\\Logs\\3\\Teste\\"+channels+"\\test"+channels+"_"+str(numberOfShifts)+"HistogramColors_H&E.bin";
    fPAS = "..\\Logs\\3\\Teste\\"+channels+"\\test"+channels+"_"+str(numberOfShifts)+"HistogramColors_PAS.bin";
    fSVM = "..\\trainedSVM_SVC_"+str(numberOfShifts)+"HistogramColors_"+channels+".bin";
    inFHEE = open(fHEE, 'rb');
    inFPAS = open(fPAS, 'rb');
    fileSVM = open(fSVM, 'rb');
    base = 256>>numberOfShifts;

    svm = pickle.load(fileSVM);               
        
    y_true = np.zeros((qtdDataTestHEE + qtdDataTestPAS), dtype=np.int);
    y_pred = np.zeros((qtdDataTestHEE + qtdDataTestPAS), dtype=np.int);
        
    data = np.zeros((qtdDataTestHEE + qtdDataTestPAS, base*base), dtype=np.float32);
    if(len(channels) == 3):
            data = np.zeros((qtdDataTestHEE + qtdDataTestPAS, base*base*base), dtype=np.float32);    
    
    for i in range(qtdDataTestHEE):
        data[i] = linearize(base, pickle.load(inFHEE), channels);
        y_true[i] = labelHEE;
    for i in range(qtdDataTestPAS):
        data[qtdDataTestHEE+i] = linearize(base, pickle.load(inFPAS), channels);        
        y_true[qtdDataTestHEE+i] = labelPAS;
    
    y_pred[ :qtdDataTestHEE] = svm.predict(data[ :qtdDataTestHEE]);    
    y_pred[qtdDataTestHEE: ] = svm.predict(data[qtdDataTestHEE: ]);
    
    target_names = ['HEE', 'PAS'];
    
    elapsedTime = time.time() - startTime;
    print(fSVM);
    print("TIME: ",elapsedTime);
    
    print("CLASSIFICATION FOR SVM, \n"+classification_report(y_true, y_pred, target_names=target_names));
    
    print("\nCONFUSION MATRIX FOR SVM, (tn, fp, fn, tp)")
    print(confusion_matrix(y_true, y_pred).ravel())
    
    inFHEE.close();
    inFPAS.close();
    fileSVM.close();
    
    text = classification_report(y_true, y_pred, target_names=target_names);
    text = text.split('    ');
    
    HEEStatiscs = [text[7], text[8], text[9]];
    PASStatiscs = [text[13], text[14], text[15]];
    ALLStatis = [text[18], text[19], text[20]];
    
    #return HEEStatiscs, PASStatiscs, ALLStatis;
    return ALLStatis;

def traineSVM(channels, numberOfShifts):    
    fHEE = "..\\Logs\\3\\Treinamento\\"+channels+"\\output"+channels+"_"+str(numberOfShifts)+"HistogramColors_H&E.bin";
    fPAS = "..\\Logs\\3\\Treinamento\\"+channels+"\\output"+channels+"_"+str(numberOfShifts)+"HistogramColors_PAS.bin";
    inFHEE = open(fHEE, 'rb');
    inFPAS = open(fPAS, 'rb');
    print("Training SVM (C-Support Vector Classification) to channels "+channels+" with "+str(numberOfShifts)+" shifts");

    base = 256>>numberOfShifts;
    X = [];
    y = [];

    for i in range(int(qtdDataTrainning/2)):
        X.append(pickle.load(inFHEE));
        y.append(labelHEE);
        X.append(pickle.load(inFPAS));
        y.append(labelPAS);        
    inFHEE.close();
    inFPAS.close();
    
    X1  = linearizeTraining(base, channels, X);
    y1 = np.array(y);
    clf = SVC();        
    kf = KFold(n_splits=10);    
    
    for k, (train, test) in enumerate(kf.split(X1, y1)):  
        print("TRAIN:", train, " - TEST:", test);
        clf.fit(X1[train], y1[train]);        
        print("K ->",k);        
        print(clf.score(X1[test], y1[test]));    
    svmFile = open("..\\trainedSVM_SVC_"+str(numberOfShifts)+"HistogramColors_"+channels+".bin", "wb");
    print(clf.get_params());        
    pickle.dump(clf, svmFile);        
    svmFile.close();

def makePlots():
    channels = ["RB", "RG", "GB", "RGB"];
    
    numberOfShifts = [3, 4, 5, 6];    
    dataRB = np.zeros((4,3), dtype=np.float32);
    dataRG = np.zeros((4,3), dtype=np.float32);
    dataGB = np.zeros((4,3), dtype=np.float32);
    dataRGB = np.zeros((4,3), dtype=np.float32);
    '''
    numberOfShifts = [5, 6];    
    dataRB = np.zeros((2,3), dtype=np.float32);
    dataRG = np.zeros((2,3), dtype=np.float32);
    dataGB = np.zeros((2,3), dtype=np.float32);
    dataRGB = np.zeros((2,3), dtype=np.float32);
    '''
    for n in numberOfShifts:
        '''
        dataRB[n-5] = testKNN("RB", n);
        dataRG[n-5] = testKNN("RG", n);
        dataGB[n-5] = testKNN("GB", n);
        dataRGB[n-5] = testKNN("RGB", n);
        '''        
        dataRB[n-3] = testKNN("RB", n);
        dataRG[n-3] = testKNN("RG", n);
        dataGB[n-3] = testKNN("GB", n);
        dataRGB[n-3] = testKNN("RGB", n);
    '''
    plotOneByOne("RB", "n of shifts", "proportion of each variable", dataRB);
    plotOneByOne("RG", "n of shifts", "proportion of each variable", dataRG);
    plotOneByOne("GB", "n of shifts", "proportion of each variable", dataGB);
    plotOneByOne("RGB", "n of shifts", "proportion of each variable", dataRGB);
    '''
    plotOneByOne("RB", "n of bins for channel", "proportion of each variable", dataRB);
    plotOneByOne("RG", "n of bins for channel", "proportion of each variable", dataRG);
    plotOneByOne("GB", "n of bins for channel", "proportion of each variable", dataGB);
    plotOneByOne("RGB", "n of bins for channel", "proportion of each variable", dataRGB);

def plotOneByOne(title, xTitle, yTitle, data):
    fig, ax = plt.subplots();
    plt.title(title);
    plt.xlabel(xTitle);
    plt.ylabel(yTitle);
    '''
    3 shifts -> 32 bins
    4 shifts -> 16 bins
    5 shifts -> 8 bins
    6 shifts -> 4 bins
    '''
    plt.scatter([32, 16, 8, 4], data[:,0], label= "Precision")
    plt.scatter([32, 16, 8, 4], data[:,1], label= "Recall")
    plt.scatter([32, 16, 8, 4], data[:,2], label= "F1-score")
    '''
    plt.plot([3,4,5,6], data[:,0,:], label= "H&E CLASS ");
    plt.plot([3,4,5,6], data[:,1,:], label= "PAS CLASS");
    plt.plot([3,4,5,6], data[:,2,:], label= "ALL CLASSES");    
    '''    
    plt.legend();
    plt.grid(True);            
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
    
    #return HEEStatiscs, PASStatiscs, ALLStatis;
    return ALLStatis;
    
        
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
    
    base = 256>>numberOfShifts;    
    X = [];
    y = [];
    '''
    X = np.zeros((265*2), dtype=np.float32);
    y = np.zeros((2), dtype=np.int)
    '''
    for i in range(int(qtdDataTrainning/2)):                        
        X.append(pickle.load(inFHEE));
        y.append(labelHEE);
        X.append(pickle.load(inFPAS));
        y.append(labelPAS);
        
    inFHEE.close();
    inFPAS.close();
    
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
    

def traineKNNLAB(numberOfShifts):    
    fHEE = "..\\Logs\\3\\Treinamento\\LAB\\outputAB_"+str(numberOfShifts)+"HistogramColors_H&E.bin";
    fPAS = "..\\Logs\\3\\Treinamento\\LAB\\outputAB_"+str(numberOfShifts)+"HistogramColors_PAS.bin";
    inFHEE = open(fHEE, 'rb');
    inFPAS = open(fPAS, 'rb');
    print("Training KNN to channels AB of LAB space with "+str(numberOfShifts)+" shifts");
    
    base = 256>>numberOfShifts;
    X = [];
    y = [];    
    for i in range(int(qtdDataTrainning/2)):                        
        X.append(pickle.load(inFHEE));
        y.append(labelHEE);
        X.append(pickle.load(inFPAS));
        y.append(labelPAS);
    
    inFHEE.close();
    inFPAS.close();
    
    X1  = np.array(X);
    y1 = np.array(y);
    knn5 = KNeighborsClassifier(n_neighbors=5);
    knn10 = KNeighborsClassifier(n_neighbors=10);
    knn15 = KNeighborsClassifier(n_neighbors=15);
    knn20 = KNeighborsClassifier(n_neighbors=20);        
    kf = KFold(n_splits=10);
    print(len(y1), len(X1));
    
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
    
    knnFile = open("..\\trainedKNN_"+str(numberOfShifts)+"HistogramColors_AB.bin", "wb");
    print(knn5.get_params());
    print(knn10.get_params());
    print(knn15.get_params());
    print(knn20.get_params());
    pickle.dump(knn5, knnFile);
    pickle.dump(knn10, knnFile);
    pickle.dump(knn15, knnFile);
    pickle.dump(knn20, knnFile);
    knnFile.close();


def testKNNLAB(numberOfShifts):
    startTime = time.time();    
    fHEE = "..\\Logs\\3\\Teste\\LAB\\testAB_"+str(numberOfShifts)+"HistogramColors_H&E.bin";
    fPAS = "..\\Logs\\3\\Teste\\LAB\\testAB_"+str(numberOfShifts)+"HistogramColors_PAS.bin";
    fKNN = "..\\trainedKNN_"+str(numberOfShifts)+"HistogramColors_AB.bin";
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
    
    for i in range(qtdDataTestHEE):
        data[i] = pickle.load(inFHEE);
        y_true[i] = labelHEE;
    for i in range(qtdDataTestPAS):
        data[qtdDataTestHEE+i] = pickle.load(inFPAS);        
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

def testAllKNNLAB():
    for i in [1, 2, 3, 4, 5, 6]:
        testKNNLAB(i);


def traineAllKNNHSV():
    fHEE0 = "..\\Logs\\3\\Treinamento\\HSV\\outputH_0HistogramColors_H&E.bin";
    fPAS0 = "..\\Logs\\3\\Treinamento\\HSV\\outputH_0HistogramColors_PAS.bin";
    fHEE1 = "..\\Logs\\3\\Treinamento\\HSV\\outputH_1HistogramColors_H&E.bin";
    fPAS1 = "..\\Logs\\3\\Treinamento\\HSV\\outputH_1HistogramColors_PAS.bin";
    fHEE2 = "..\\Logs\\3\\Treinamento\\HSV\\outputH_2HistogramColors_H&E.bin";
    fPAS2 = "..\\Logs\\3\\Treinamento\\HSV\\outputH_2HistogramColors_PAS.bin";
    fHEE3 = "..\\Logs\\3\\Treinamento\\HSV\\outputH_3HistogramColors_H&E.bin";
    fPAS3 = "..\\Logs\\3\\Treinamento\\HSV\\outputH_3HistogramColors_PAS.bin";
    inFHEE0 = open(fHEE0, 'rb');
    inFPAS0 = open(fPAS0, 'rb');
    inFHEE1 = open(fHEE1, 'rb');
    inFPAS1 = open(fPAS1, 'rb');
    inFHEE2 = open(fHEE2, 'rb');
    inFPAS2 = open(fPAS2, 'rb');
    inFHEE3 = open(fHEE3, 'rb');
    inFPAS3 = open(fPAS3, 'rb');
    
    traineKNNHSV(inFHEE0, inFPAS0, 360);
    traineKNNHSV(inFHEE1, inFPAS1, 180);
    traineKNNHSV(inFHEE2, inFPAS2, 90);
    traineKNNHSV(inFHEE3, inFPAS3, 45);
    
    
def traineKNNHSV(inFHEE, inFPAS, base):
    X = [];
    y = [];    
    for i in range(int(qtdDataTrainning/2)):                        
        X.append(pickle.load(inFHEE));
        y.append(labelHEE);
        X.append(pickle.load(inFPAS));
        y.append(labelPAS);
    
    inFHEE.close();
    inFPAS.close();
    
    X1  = np.array(X);
    y1 = np.array(y);
    knn5 = KNeighborsClassifier(n_neighbors=5);
    knn10 = KNeighborsClassifier(n_neighbors=10);
    knn15 = KNeighborsClassifier(n_neighbors=15);
    knn20 = KNeighborsClassifier(n_neighbors=20);        
    kf = KFold(n_splits=10);
    print(len(y1), len(X1));
    
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
    n = "..\\trainedKNN_0HistogramColors_H.bin";
    if(base==360):
        n = "..\\trainedKNN_0HistogramColors_H.bin";
    elif(base==180):
        n = "..\\trainedKNN_1HistogramColors_H.bin";
    elif(base==90):
        n = "..\\trainedKNN_2HistogramColors_H.bin";
    elif(base==45):
        n = "..\\trainedKNN_3HistogramColors_H.bin";
    knnFile = open(n, "wb");
    print(knn5.get_params());
    print(knn10.get_params());
    print(knn15.get_params());
    print(knn20.get_params());
    pickle.dump(knn5, knnFile);
    pickle.dump(knn10, knnFile);
    pickle.dump(knn15, knnFile);
    pickle.dump(knn20, knnFile);
    knnFile.close();

def testAllKNNHSV():
    x = [0, 1, 2, 3];
    for n in x:
        testKNNHSV(n);

def testKNNHSV(numberOfShifts):
    startTime = time.time();
    base = 360;    
    if(numberOfShifts==0):
        base = 360;
    elif(numberOfShifts==1):
        base = 180;
    elif(numberOfShifts==2):
        base = 90;
    elif(numberOfShifts==3):
        base = 45;
        
    fHEE = "..\\Logs\\3\\Teste\\HSV\\testH_"+str(numberOfShifts)+"HistogramColors_H&E.bin";
    fPAS = "..\\Logs\\3\\Teste\\HSV\\testH_"+str(numberOfShifts)+"HistogramColors_PAS.bin";
    fKNN = "..\\trainedKNN_"+str(numberOfShifts)+"HistogramColors_H.bin";
    inFHEE = open(fHEE, 'rb');
    inFPAS = open(fPAS, 'rb');
    fileKNN = open(fKNN, 'rb');    

    knn5 = pickle.load(fileKNN);
    knn10 = pickle.load(fileKNN);
    knn15 = pickle.load(fileKNN);
    knn20 = pickle.load(fileKNN);
        
    y_true = np.zeros((qtdDataTestHEE + qtdDataTestPAS), dtype=np.int);
    y_pred5 = np.zeros((qtdDataTestHEE + qtdDataTestPAS), dtype=np.int);
    y_pred10 = np.zeros((qtdDataTestHEE + qtdDataTestPAS), dtype=np.int);
    y_pred15 = np.zeros((qtdDataTestHEE + qtdDataTestPAS), dtype=np.int);
    y_pred20 = np.zeros((qtdDataTestHEE + qtdDataTestPAS), dtype=np.int);
    data = np.zeros((qtdDataTestHEE + qtdDataTestPAS, base), dtype=np.float32);    
    
    for i in range(qtdDataTestHEE):
        data[i] = pickle.load(inFHEE);
        y_true[i] = labelHEE;
    for i in range(qtdDataTestPAS):
        data[qtdDataTestHEE+i] = pickle.load(inFPAS);        
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
        
    return np.float32(rb), np.float32(rg), np.float32(gb), np.float32(rgb);


def calculateLABColor(isTest):
    startTime = time.time();
    
    a = "output";
    if(isTest):
            a = "test";        
    for subdir, dirs, files in os.walk(os.path.abspath(os.path.join('.\\', os.pardir))+'\\Images\\'):
        group = subdir.split("\\")[-1];

        outFileAB1 = open("..\\"+a+"AB_1HistogramColors_"+group+".bin", "wb");
        outFileAB2 = open("..\\"+a+"AB_2HistogramColors_"+group+".bin", "wb");
        outFileAB3 = open("..\\"+a+"AB_3HistogramColors_"+group+".bin", "wb");
        outFileAB4 = open("..\\"+a+"AB_4HistogramColors_"+group+".bin", "wb");
        outFileAB5 = open("..\\"+a+"AB_5HistogramColors_"+group+".bin", "wb");
        outFileAB6 = open("..\\"+a+"AB_6HistogramColors_"+group+".bin", "wb");
                
        print(subdir); 
        for file in files:
            print("\t",file);
            file = subdir+"\\"+file
            ab1, ab2, ab3, ab4, ab5, ab6 = calculeLABColorHistogram(file);            
            pickle.dump(ab1, outFileAB1);
            pickle.dump(ab2, outFileAB2);
            pickle.dump(ab3, outFileAB3);
            pickle.dump(ab4, outFileAB4);
            pickle.dump(ab5, outFileAB5);
            pickle.dump(ab6, outFileAB6);        
        outFileAB1.close();
        outFileAB2.close();
        outFileAB3.close();
        outFileAB4.close();
        outFileAB5.close();
        outFileAB6.close();
                         
    elapsedTime = time.time() - startTime;    
    print("FINISH, ELAPSED TIME(seconds): ",elapsedTime);
    
    
def calculeLABColorHistogram(file):
    img = io.imread(file);
    height, width = len(img), len(img[0]);    
    size = height*width;
    labImage = color.rgb2lab(img);        
    
    labImage[:, :, 0] = exposure.rescale_intensity(labImage[:, :, 0],
        in_range=(np.amin(labImage[:, :, 0]), np.amax(labImage[:, :, 0])), out_range=(0, 100));
    labImage[:, :, 1] = exposure.rescale_intensity(labImage[:, :, 1],
        in_range=(np.amin(labImage[:, :, 1]), np.amax(labImage[:, :, 1])), out_range=(-128, 127));
    labImage[:, :, 2] = exposure.rescale_intensity(labImage[:, :, 2],
        in_range=(np.amin(labImage[:, :, 2]), np.amax(labImage[:, :, 2])), out_range=(-128, 127));  
    
    
    ab1 = np.zeros((128, 128), dtype=np.float32);
    ab2 = np.zeros((64, 64), dtype=np.float32);
    ab3 = np.zeros((32, 32), dtype=np.float32);
    ab4 = np.zeros((16, 16), dtype=np.float32);
    ab5 = np.zeros((8, 8), dtype=np.float32);
    ab6 = np.zeros((4, 4), dtype=np.float32);
    for i in range(height):
        for j in range(width):
            pixel = labImage[i, j];
            a = 128 + int(pixel[1]);
            b = 128 + int(pixel[2]);            
            
            ab1[a>>1][b>>1]+=1;
            ab2[a>>2][b>>2]+=1;
            ab3[a>>3][b>>3]+=1;
            ab4[a>>4][b>>4]+=1;
            ab5[a>>5][b>>5]+=1;
            ab6[a>>6][b>>6]+=1;
                                    
    ab1 = np.divide(ab1, size);
    ab1 = np.multiply(ab1, 100);
    ab2 = np.divide(ab2, size);
    ab2 = np.multiply(ab2, 100);
    ab3 = np.divide(ab3, size);
    ab3 = np.multiply(ab3, 100);
    ab4 = np.divide(ab4, size);
    ab4 = np.multiply(ab4, 100);
    ab5 = np.divide(ab5, size);
    ab5 = np.multiply(ab5, 100);
    ab6 = np.divide(ab6, size);
    ab6 = np.multiply(ab6, 100);
        
    ab1 = np.float32(linearize(128, ab1, "AB"));
    ab2 = np.float32(linearize(64, ab2, "AB")); 
    ab3 = np.float32(linearize(32, ab3, "AB"));
    ab4 = np.float32(linearize(16, ab4, "AB")); 
    ab5 = np.float32(linearize(8, ab5, "AB"));
    ab6 = np.float32(linearize(4, ab6, "AB")); 
    return ab1, ab2, ab3, ab4, ab5, ab6;
    
    
def calculateHSVColor(isTest):
    startTime = time.time();
    
    a = "output";
    if(isTest):
            a = "test";        
    for subdir, dirs, files in os.walk(os.path.abspath(os.path.join('.\\', os.pardir))+'\\Images\\'):
        group = subdir.split("\\")[-1];

        outFileH0 = open("..\\"+a+"H_0HistogramColors_"+group+".bin", "wb");
        outFileH1 = open("..\\"+a+"H_1HistogramColors_"+group+".bin", "wb");
        outFileH2 = open("..\\"+a+"H_2HistogramColors_"+group+".bin", "wb");
        outFileH3 = open("..\\"+a+"H_3HistogramColors_"+group+".bin", "wb");                
        print(subdir); 
        for file in files:
            print("\t",file);
            file = subdir+"\\"+file;
            h0, h1, h2, h3 = calculeHSVColorHistogram(file);
            pickle.dump(h0, outFileH0);
            pickle.dump(h1, outFileH1);
            pickle.dump(h2, outFileH2);
            pickle.dump(h3, outFileH3);            
        outFileH0.close();
        outFileH1.close();
        outFileH2.close();
        outFileH3.close();                                 
    elapsedTime = time.time() - startTime;    
    print("FINISH, ELAPSED TIME(seconds): ",elapsedTime);
    
    
def calculeHSVColorHistogram(file):
    img = io.imread(file);
    height, width = len(img), len(img[0]);    
    size = height*width;
    hsvImage = color.rgb2hsv(img);
    hsvImage[:, :, 0] = exposure.rescale_intensity(hsvImage[:, :, 0],
        in_range=(np.amin(hsvImage[:, :, 0]), np.amax(hsvImage[:, :, 0])), out_range=(0.0, 359.0));
    hsvImage[:, :, 1] = exposure.rescale_intensity(hsvImage[:, :, 1],
        in_range=(np.amin(hsvImage[:, :, 1]), np.amax(hsvImage[:, :, 1])), out_range=(0.0, 100.0));
    hsvImage[:, :, 2] = exposure.rescale_intensity(hsvImage[:, :, 2],
        in_range=(np.amin(hsvImage[:, :, 2]), np.amax(hsvImage[:, :, 2])), out_range=(0.0, 100.0));    
    
    h0 = np.zeros((360), dtype=np.float32);
    h1 = np.zeros((180), dtype=np.float32);
    h2 = np.zeros((90), dtype=np.float32);
    h3 = np.zeros((45), dtype=np.float32);
    for i in range(height):
        for j in range(width):
            pixel = hsvImage[i, j];
            h0[int(pixel[1])]+=1;                        
            h1[int(pixel[1]/2)]+=1;
            h2[int(pixel[1]/4)]+=1;
            h3[int(pixel[1]/8)]+=1;                                            
    h0 = np.divide(h0, size);
    h0 = np.multiply(h0, 100);
    h1 = np.divide(h1, size);
    h1 = np.multiply(h1, 100);
    h2 = np.divide(h2, size);
    h2 = np.multiply(h2, 100);
    h3 = np.divide(h3, size);
    h3 = np.multiply(h3, 100);
             
    return h0, h1, h2, h3;



#calculateRGBColor(n=1, isTest=True);
#calculateLABColor(isTest=False);
#calculateHSVColor(isTest=True);
#traineKNN(channels="GB", numberOfShifts=2);
#testKNN(channels="RGB", numberOfShifts=4);
#traineKNNLAB(numberOfShifts=1);
#testAllKNNLAB();
#traineKNNHSV(numberOfShifts=1);
#traineAllKNNHSV();
testAllKNNHSV();
#makePlots();
#traineSVM(channels="RG", numberOfShifts=3);
#testSVM(channels="RG", numberOfShifts=3);




