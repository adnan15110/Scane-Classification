from random import shuffle
import os,shutil,math

class trainTestandValidationDataCreator:
    
    def __init__(self):
        self.meanscore = 0.50294268497489492 # output from DataReader.calculateAverageScore()
        self.per_train = .6
        self.per_test = .2
        self.per_validation = .2
        self.img_names=[]
        self.cls_labels=[]
        self.labels_file = 'labels.txt'
        self.createListOfImagesAndLabels()
        
    def createListOfImagesAndLabels(self, regresssion_flag = False):
        '''
        populates img_names=[] and scores=[]
        score < mean == class 0
        score > mean == class 1 
        '''
        if (regresssion_flag):
            f = open(self.labels_file,'r')
            lines = shuffle(f.readlines())
            for line in lines:
                img_name,score = line.strip().split(',')
                self.img_names.append(img_name)
                self.cls_labels.append(score)
                        # preprocess class score here.
            f.close()
        else:
            f = open(self.labels_file,'r')
            for line in f.readlines():
                img_name,score = line.strip().split(',')
                self.img_names.append(img_name)
                cls_label = 0 if float(score) < self.meanscore else 1
                self.cls_labels.append(cls_label)
            f.close()

    def createBalanceDataSet(self):
        cls_one_imgs = [] # < mean
        cls_two_imgs = [] # > means
        
        for img_name, score in zip(self.img_names,self.cls_labels):
            if score == 0:
                cls_one_imgs.append(img_name)
            else:
                cls_two_imgs.append(img_name)
        
        #shuffling the dataset
        shuffle(cls_one_imgs)
        shuffle(cls_two_imgs)
        
        #storage for training_datasets
        training_datasets= []
        training_labels= []
        validation_datasets = []
        validation_labels = []
        test_datasets= []
        test_labels =[]
        
        # creating dataset for class 0
        total_class_one = len(cls_one_imgs)
        num_training_img = int(math.ceil(total_class_one*self.per_train))
        num_test_img = int(math.ceil(total_class_one*self.per_test))
        num_val_img = total_class_one-num_training_img-num_test_img
        
        print num_training_img
        print num_test_img
        print num_val_img

        training_datasets +=cls_one_imgs[:num_training_img]
        training_labels += [0]*num_training_img
        
        test_datasets+= cls_one_imgs[num_training_img+1:num_training_img+1+num_test_img]
        test_labels+=[0]*num_test_img
        
        validation_datasets += cls_one_imgs[num_training_img+num_test_img:]
        validation_labels += [0]*num_val_img
        
        print len(test_datasets)
        print len(test_labels)
        
        print len(validation_datasets)
        print len(validation_labels)

        # creating dataset for class 0
        total_class_two = len(cls_two_imgs)
        num_training_img = int(total_class_two*self.per_train)
        num_test_img = int(total_class_two*self.per_test)
        num_val_img = total_class_two-num_training_img-num_test_img
        
        training_datasets +=cls_two_imgs[:num_training_img+1]
        training_labels += [1]*num_training_img
        
        test_datasets+= cls_two_imgs[num_training_img+1:num_training_img+1+num_test_img]
        test_labels+=[1]*num_test_img
        
        validation_datasets += cls_two_imgs[num_training_img+1+num_test_img:]
        validation_labels += [1]*num_val_img
        
        return training_datasets,training_labels,test_datasets,test_labels,validation_datasets,validation_labels               
        
    def createDatasetForClassificationProblem(self):
        '''
        create folder and move images to particular folder
        
        -classification_datasets
            -train
                -class1
                -class2
            -test
                -class1
                -class2
            -validation
                -class1
                -class2
        
        '''
        training_datasets,training_labels,test_datasets,test_labels,validation_datasets,\
        validation_labels = self.createBalanceDataSet()
        
        dataset_folder = os.path.join(os.getcwd(),'datasets')

        #creates folders for each datasets
        train_dataset_folder_path = os.path.join(os.getcwd(),'classification-datasets','train')
        if not os.path.exists(train_dataset_folder_path):
            os.mkdir(train_dataset_folder_path)
            os.mkdir(os.path.join(train_dataset_folder_path,'0'))
            os.mkdir(os.path.join(train_dataset_folder_path,'1'))

        test_dataset_folder_path = os.path.join(os.getcwd(),'classification-datasets','test')
        if not os.path.exists(test_dataset_folder_path):
            os.mkdir(test_dataset_folder_path)
            os.mkdir(os.path.join(test_dataset_folder_path,'0'))
            os.mkdir(os.path.join(test_dataset_folder_path,'1'))
        
        val_dataset_folder_path = os.path.join(os.getcwd(),'classification-datasets','val')
        if not os.path.exists(val_dataset_folder_path):
            os.mkdir(val_dataset_folder_path)
            os.mkdir(os.path.join(val_dataset_folder_path,'0'))
            os.mkdir(os.path.join(val_dataset_folder_path,'1'))
        
        #copies img to their coresponding folders
        for img,label in zip(training_datasets,training_labels):
            src = os.path.join(dataset_folder,img)
            if label == 0:    
                dest = os.path.join(train_dataset_folder_path,'0',img)
                shutil.copyfile(src, dest)
            else:
                dest = os.path.join(train_dataset_folder_path,'1',img)
                shutil.copyfile(src, dest)
        
        for img,label in zip(test_datasets,test_labels):
            src = os.path.join(dataset_folder,img)
            if label == 0:    
                dest = os.path.join(test_dataset_folder_path,'0',img)
                shutil.copyfile(src, dest)
            else:
                dest = os.path.join(test_dataset_folder_path,'1',img)
                shutil.copyfile(src, dest)

        for img,label in zip(validation_datasets,validation_labels):
            src = os.path.join(dataset_folder,img)
            if label == 0:    
                dest = os.path.join(val_dataset_folder_path,'0',img)
                shutil.copyfile(src, dest)
            else:
                dest = os.path.join(val_dataset_folder_path,'1',img)
                shutil.copyfile(src, dest)

    def createDatasetForR'''
        '''
        create folder and move images to particular folder
        
        -classification_datasets
            -train
            -test
            -validation
        '''
        training_datasets,training_labels,test_datasets,test_labels,validation_datasets,\
        validation_labels = self.createBalanceDataSet()
        
        dataset_folder = os.path.join(os.getcwd(),'datasets')

        #creates folders for each datasets
        train_dataset_folder_path = os.path.join(os.getcwd(),'classification-datasets','train')
        if not os.path.exists(train_dataset_folder_path):
            os.mkdir(train_dataset_folder_path)
            os.mkdir(os.path.join(train_dataset_folder_path,'0'))
            os.mkdir(os.path.join(train_dataset_folder_path,'1'))

        test_dataset_folder_path = os.path.join(os.getcwd(),'classification-datasets','test')
        if not os.path.exists(test_dataset_folder_path):
            os.mkdir(test_dataset_folder_path)
            os.mkdir(os.path.join(test_dataset_folder_path,'0'))
            os.mkdir(os.path.join(test_dataset_folder_path,'1'))
        
        val_dataset_folder_path = os.path.join(os.getcwd(),'classification-datasets','val')
        if not os.path.exists(val_dataset_folder_path):
            os.mkdir(val_dataset_folder_path)
            os.mkdir(os.path.join(val_dataset_folder_path,'0'))
            os.mkdir(os.path.join(val_dataset_folder_path,'1'))
        
        #copies img to their coresponding folders
        for img,label in zip(training_datasets,training_labels):
            src = os.path.join(dataset_folder,img)
            if label == 0:    
                dest = os.path.join(train_dataset_folder_path,'0',img)
                shutil.copyfile(src, dest)
            else:
                dest = os.path.join(train_dataset_folder_path,'1',img)
                shutil.copyfile(src, dest)
        
        for img,label in zip(test_datasets,test_labels):
            src = os.path.join(dataset_folder,img)
            if label == 0:    
                dest = os.path.join(test_dataset_folder_path,'0',img)
                shutil.copyfile(src, dest)
            else:
                dest = os.path.join(test_dataset_folder_path,'1',img)
                shutil.copyfile(src, dest)

        for img,label in zip(validation_datasets,validation_labels):
            src = os.path.join(dataset_folder,img)
            if label == 0:    
                dest = os.path.join(val_dataset_folder_path,'0',img)
                shutil.copyfile(src, dest)
            else:
                dest = os.path.join(val_dataset_folder_path,'1',img)
                shutil.copyfile(src, dest)egression(self):
        '''
        create folder and move images to particular folder
        
        -classification_datasets
            -train
                -class1
                -class2
            -test
                -class1
                -class2
            -validation
                -class1
                -class2
        
        '''
        training_datasets,training_labels,test_datasets,test_labels,validation_datasets,\
        validation_labels = self.createBalanceDataSet()
        
        dataset_folder = os.path.join(os.getcwd(),'datasets')

        #creates folders for each datasets
        train_dataset_folder_path = os.path.join(os.getcwd(),'classification-datasets','train')
        if not os.path.exists(train_dataset_folder_path):
            os.mkdir(train_dataset_folder_path)
            os.mkdir(os.path.join(train_dataset_folder_path,'0'))
            os.mkdir(os.path.join(train_dataset_folder_path,'1'))

        test_dataset_folder_path = os.path.join(os.getcwd(),'classification-datasets','test')
        if not os.path.exists(test_dataset_folder_path):
            os.mkdir(test_dataset_folder_path)
            os.mkdir(os.path.join(test_dataset_folder_path,'0'))
            os.mkdir(os.path.join(test_dataset_folder_path,'1'))
        
        val_dataset_folder_path = os.path.join(os.getcwd(),'classification-datasets','val')
        if not os.path.exists(val_dataset_folder_path):
            os.mkdir(val_dataset_folder_path)
            os.mkdir(os.path.join(val_dataset_folder_path,'0'))
            os.mkdir(os.path.join(val_dataset_folder_path,'1'))
        
        #copies img to their coresponding folders
        for img,label in zip(training_datasets,training_labels):
            src = os.path.join(dataset_folder,img)
            if label == 0:    
                dest = os.path.join(train_dataset_folder_path,'0',img)
                shutil.copyfile(src, dest)
            else:
                dest = os.path.join(train_dataset_folder_path,'1',img)
                shutil.copyfile(src, dest)
        
        for img,label in zip(test_datasets,test_labels):
            src = os.path.join(dataset_folder,img)
            if label == 0:    
                dest = os.path.join(test_dataset_folder_path,'0',img)
                shutil.copyfile(src, dest)
            else:
                dest = os.path.join(test_dataset_folder_path,'1',img)
                shutil.copyfile(src, dest)

        for img,label in zip(validation_datasets,validation_labels):
            src = os.path.join(dataset_folder,img)
            if label == 0:    
                dest = os.path.join(val_dataset_folder_path,'0',img)
                shutil.copyfile(src, dest)
            else:
                dest = os.path.join(val_dataset_folder_path,'1',img)
                shutil.copyfile(src, dest)
