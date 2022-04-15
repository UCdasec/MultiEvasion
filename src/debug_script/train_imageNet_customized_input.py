"""
train image based malware detector

load image data with cusotmized function:
image --> bytes --> trim/padding --> reshape to greyscale image e.g. [1,224,224]

therefore, squeeze the label tensor to one dimension
"""
import os
os.sys.path.append('..')

import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import datasets
from PIL import Image
from PIL import ImageFile
import numpy as np
import torch.optim as optim
import time, argparse, os
from src.model import ImageNet, AlexNet, ResNet18,Xception
from src.util import ImageDataset_customized
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd

## avoid error when load image
ImageFile.LOAD_TRUNCATED_IMAGES = True      ## solve error "OSError: image file is truncated"
Image.MAX_IMAGE_PIXELS = None               ## solve error image with significant pixels


## random seed
import random
seed = 42
torch.manual_seed(seed)
np.random.seed(seed)
random.seed(seed)


class train_imageNet:

    def __init__(self):
        self.device = ('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.criterion = nn.CrossEntropyLoss()


    def binary_acc(self,preds,y):

        preds = torch.argmax(preds, 1)
        correct = (preds == y)
        acc = float(correct.sum()) / len(correct)

        return acc


    def evaluate_step(self, model=None, data_iterator=None):

        epoch_loss = 0
        epoch_acc = 0

        model.to(self.device)
        model.eval()

        with torch.no_grad():
            for batch in data_iterator:
                X,y = batch
                X,y = X.float().to(self.device), y.long().to(self.device)

                preds = model(X)
                loss = self.criterion(preds,y)

                acc = self.binary_acc(preds,y)

                epoch_loss += loss.item()
                epoch_acc += acc
        avg_loss = epoch_loss/len(data_iterator)
        avg_acc = epoch_acc/len(data_iterator)

        return avg_loss, avg_acc


    def train_step(self,model=None,data_iterator=None,optimizer=None):

        epoch_loss, epoch_acc = 0,0

        model.to(self.device)
        model.train()

        for batch in data_iterator:
            X, y = batch
            X, y = X.float().to(self.device), y.long().to(self.device)

            optimizer.zero_grad()

            preds = model(X)
            loss = self.criterion(preds,y.squeeze(1))
            acc = self.binary_acc(preds,y)

            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
            epoch_acc += acc

        avg_loss = epoch_loss/len(data_iterator)
        avg_acc = epoch_acc/len(data_iterator)

        return avg_loss,avg_acc


    def epoch_time(self,start,end):
        elapsed_time = end-start
        elapsed_mins = int(elapsed_time/60)
        elapsed_secs = int(elapsed_time-(elapsed_mins*60))
        return elapsed_mins,elapsed_secs

    def transform_operations(self):
        ## define transform operations to load image, the load data range [0,1]
        ## for training data to mitigate model overfitting by
        ## such as resizing, cropping, squishing, and padding.
        ## However, squishing and padding robs the original information from the images and adds additional pixels respectively.
        ## Hence, randomly resizing the images yields good results.
        transform = transforms.Compose([
            transforms.Grayscale(num_output_channels=1),
            transforms.Resize((args.resize_value,args.resize_value)), ## resize the input, nmust larger than Crop
            # transforms.CenterCrop(224),
            transforms.RandomCrop(args.image_resolution),   # crop a part from the resized image
            transforms.ToTensor(),
            # transforms.Normalize(mean=0.485, std=0.229)
        ])
        return transform


    def transform_operations_for_val(self):
        ## define transform operations to load image, the load data range [0,1]
        ## for validation/test data, no need to do transformations to avoid overfitting here
        transform = transforms.Compose([
            transforms.Grayscale(num_output_channels=1),
            transforms.Resize((args.image_resolution,args.image_resolution)),
            transforms.ToTensor(),
            # transforms.Normalize(mean=0.485, std=0.229)
        ])
        return transform


    def load_data(self,
                  data_path=None,
                  batch_size=16,
                  shuffle=True,
                  num_workers=2,
                  training_data=False):
        """
        load image data with api (image formal loading approach )
        :param data_path: parent folder path, eg. '../image/train/' which include benign and mal subfolders
        :param batch_size:
        :param shuffle:
        :param num_workers:
        :return:
        """
        if training_data:
            dataset = datasets.ImageFolder(data_path, transform=self.transform_operations())
        else:
            dataset = datasets.ImageFolder(data_path, transform=self.transform_operations_for_val())
        dataloader = torch.utils.data.DataLoader(dataset,
                                                 batch_size=batch_size,
                                                 shuffle=shuffle,
                                                 num_workers=num_workers)
        return dataloader


    def load_data_1(self,
                    data_label_table_path=None,
                    data_path='../data/image/',
                    batch_size=32,
                    shuffle=True,
                    num_workers=2):
        """
        load image --> convert to bytes --> trim or padding --> reshape to image [1,resolution,resolution]
        without any transformations
        :param data_label_table_path: data_label csv file path
        :param data_path: all image saved path
        :param batch_size:
        :param shuffle:
        :param num_workers:
        :return:
        """
        data_label_table = pd.read_csv(data_label_table_path, header=None, index_col=0)
        data_label_table = data_label_table.rename(columns={1: 'ground_truth'})

        # Dataloader: parallelly generate batch data
        data_loader = torch.utils.data.DataLoader(ImageDataset_customized(list(data_label_table.index),data_path,list(data_label_table.ground_truth),
                                                               args.first_n_byte,image_resolution=args.image_resolution),
                                                batch_size=batch_size,
                                                shuffle=shuffle,
                                                num_workers=num_workers)

        # output the statistic of loading data
        print(f'Dataset: {data_label_table_path}')
        print('\tTotal', len(data_label_table), 'files')
        print('\tMalware Count :', data_label_table['ground_truth'].value_counts()[1])
        print('\tGoodware Count:', data_label_table['ground_truth'].value_counts()[0])

        return data_loader


    def plot_loss_acc(self,train_loss=None,val_loss=None,train_acc=None,val_acc=None):
        save_path = '../result/model_training/plot/'
        Path(save_path).mkdir(parents=True, exist_ok=True)
        plot1 = plt.figure(1)
        plt.plot(train_acc, '-o')
        plt.plot(val_acc, '-o')
        plt.xlabel('epoch')
        plt.ylabel('accuracy')
        plt.ylim(0,1)
        plt.legend(['Train', 'Validation'])
        plt.title('Train vs Validation Accuracy')
        plt.savefig(save_path + args.model_name + '_train_val_acc.png')

        plot2 = plt.figure(2)
        plt.plot(train_loss, '-o')
        plt.plot(val_loss, '-o')
        plt.xlabel('epoch')
        plt.ylabel('loss')
        plt.ylim(0, 1)
        plt.legend(['Train', 'Validation'])
        plt.title('Train vs Validation Loss')
        plt.savefig(save_path + args.model_name + '_train_val_loss.png')


    def train_loop(self,
                   epochs=50,
                   model=None,
                   train_data=None,
                   val_data=None,
                   test_data=None,
                   lr=0.001,
                   model_path=None):

        train_epochs_loss,val_epochs_loss = [],[]
        train_epochs_acc,val_epochs_acc = [],[]

        best_val_loss = float('inf')

        optimizer = optim.Adam(model.parameters(), lr=lr)

        for epoch in range(1, epochs + 1):

            start_time = time.time()

            train_loss, train_acc = self.train_step(model=model, data_iterator=train_data, optimizer=optimizer)
            valid_loss, valid_acc = self.evaluate_step(model, val_data)

            train_epochs_loss.append(train_loss)
            train_epochs_acc.append(train_acc)
            val_epochs_loss.append(valid_loss)
            val_epochs_acc.append(valid_acc)


            end_time = time.time()

            epoch_mins, epoch_secs = self.epoch_time(start_time, end_time)

            ## save checkpoint when get best val loss
            if valid_loss < best_val_loss:
                best_val_loss = valid_loss
                torch.save(model.state_dict(), model_path)
                print(f'Checkpoint saved at: {model_path}')
                if epoch > 1:
                    with open(args.log_file_name,'a') as f:
                        print(f'Checkpoint saved at: {model_path} when val_loss: {best_val_loss}',file=f)

            ## ajust lr based on different epoches
            if args.adjust_lr_flag == 'True' or args.adjust_lr_flag==True:
                lr_adjust = {
                    5: 5e-4, 10: 1e-4, 15: 5e-5,
                    20: 1e-5, 25: 5e-6, 35: 1e-6,
                    40:5e-4,
                }
                if epoch in lr_adjust.keys():
                    lr = lr_adjust[epoch]
                    for param_group in optimizer.param_groups:
                        param_group['lr'] = lr
                    print(f'Updating learning rate to {lr}')

            ## output results of each epoch
            print(f'Epoch: {epoch:02} | Epoch Time: {epoch_mins}m {epoch_secs}s | Train Loss: {train_loss:.3f} | Train Acc: {train_acc:.3f} | Val. Loss: {valid_loss:.3f} | Val. Acc: {valid_acc:.3f}')

            ## save the training results
            with open(args.log_file_name, 'a') as f:
                if epoch == 1:
                    print('-'*20,'Training results','-'*20,file=f)
                print(f'Epoch: {epoch:02} | Epoch Time: {epoch_mins}m {epoch_secs}s | Train Loss: {train_loss:.3f} | Train Acc: {train_acc:.3f} | Val. Loss: {valid_loss:.3f} | Val. Acc: {valid_acc:.3f}', file=f)

        ## plot loss and acc figure and save
        self.plot_loss_acc(train_loss=train_epochs_loss,
                           val_loss=val_epochs_loss,
                           train_acc=train_epochs_acc,
                           val_acc=val_epochs_acc)

        ## test trained model on test data
        test_loss, test_acc = self.evaluate_step(model, test_data)
        print(f'Test Loss: {test_loss}, Test Acc: {test_acc}')
        with open(args.log_file_name,'a') as f:
            print('\n', file=f)
            print('-'*20,'Testing results','-'*20,file=f)
            print(f'Test Loss: {test_loss}, Test Acc: {test_acc}',file=f)
            print('\n',file=f)


    def main(self,image_formal_loading=False):
        print(f'CUDA AVAILABLE: {torch.cuda.is_available()}')

        ## load data
        if image_formal_loading:
            ## load image for API and perform transformations
            trainloader = self.load_data(data_path=args.train_data_path,
                                    batch_size=args.batch_size,
                                    shuffle=True,
                                    num_workers=2,
                                    training_data=True)

            testloader = self.load_data(data_path=args.test_data_path,
                                   batch_size=args.batch_size,
                                   shuffle=False,
                                   num_workers=2,
                                   training_data=False)

            valloader = self.load_data(data_path=args.val_data_path,
                                        batch_size=args.batch_size,
                                        shuffle=False,
                                        num_workers=2,
                                        training_data=False)
        else:
            ## load image with customized method, no transformations applied
            trainloader = self.load_data_1(data_label_table_path='../../data/train_data_label.csv',
                                           data_path='../../data/image/',
                                           batch_size=args.batch_size,
                                           shuffle=True,
                                           num_workers=0)

            testloader = self.load_data_1(data_label_table_path='../../data/test_data_label.csv',
                                          data_path='../../data/image/',
                                          batch_size=args.batch_size,
                                          shuffle=False,
                                          num_workers=0)

            valloader = self.load_data_1(data_label_table_path='../../data/val_data_label.csv',
                                         data_path='../../data/image/',
                                         batch_size=args.batch_size,
                                         shuffle=False,
                                         num_workers=0)


        ## save statis of dataset into log file
        with open(args.log_file_name,'a') as f:
            print('-' * 20, 'Input file Statistics', '-' * 20, file=f)
            print(f'Train data size {len(trainloader) * args.batch_size}',file=f)
            print(f'Test data size {len(testloader) * args.batch_size}',file=f)
            print(f'Validation data size {len(valloader) * args.batch_size}',file=f)
            print('\n',file=f)

        ## load model
        if args.model_name == 'ImageNet':
            model = ImageNet()
        elif args.model_name == 'AlexNet':
            model = AlexNet(1,2)
        elif args.model_name == 'ResNet18':
            model = ResNet18(1,2)
        elif args.model_name == 'Xception':
            model = Xception(1,2)
        self.train_loop(epochs=args.epochs,
                        model=model,
                        train_data=trainloader,
                        val_data=valloader,
                        test_data=testloader,
                        lr=args.lr,
                        model_path=args.model_save_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='train image based malware detector',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--log_file_name',default=None,type=str, help='txt file save results')
    parser.add_argument('--train_data_path',default=None,type=str,
                        help='train data parent folder includes mal & benign two folders')
    parser.add_argument('--test_data_path', default=None, type=str,
                        help='test data parent folder includes mal & benign two folders')
    parser.add_argument('--val_data_path', default=None, type=str,
                        help='val data parent folder includes mal & benign two folders')
    parser.add_argument('--model_save_path', default=None, type=str,
                        help='path for saving trained models')
    parser.add_argument('--model_name', default='AlexNet', type=str, help='name of model')
    parser.add_argument('--first_n_byte', default=102400, type=int, help='input size')
    parser.add_argument('--epochs', default=50, type=int, help='num of training epochs')
    parser.add_argument('--batch_size', default=16, type=int, help='batch size')
    parser.add_argument('--lr', default=0.001, type=float, help='learning rate')
    parser.add_argument('--image_resolution', default=224, type=int, help='image resolution that load in model')
    parser.add_argument('--resize_value', default=255, type=int, help='resize value must large than resolution,'
                        'as crop (based on resolution) image will be selected from resized image')
    parser.add_argument('--adjust_lr_flag', default=True, type=str, help='whether adjust lr')

    args = parser.parse_args()
    print('\n',args,'\n')

    ## modify log file name
    log_file_split = args.log_file_name.split('.')
    args.log_file_name = ('.').join(log_file_split[:-1]) + args.model_name + '.txt'
    if os.path.exists(args.log_file_name):
        os.remove(args.log_file_name)
    with open(args.log_file_name,'a') as f:
        print('-'*20,'Parameters','-'*20,file=f)
        print(args,file=f)
        print('\n',file=f)

    ## create folder if not exist
    log_file_split = args.log_file_name.split('/')
    folder_path = ('/').join(log_file_split[:-1]) + '/'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    model_path_split = args.model_save_path.split('/')
    model_path = ('/').join(model_path_split[:-1]) + '/'
    if not os.path.exists(model_path):
        os.makedirs(model_path)

    ## modify model save name
    model_name_split = args.model_save_path.split('.')
    args.model_save_path = ('.').join(model_name_split[:-1]) + args.model_name + '.pth'

    ## training
    start = time.time()
    train_model = train_imageNet()
    train_model.main(image_formal_loading=False)

    ## run time
    elapsed_time = time.time() - start
    elapsed_mins = int(elapsed_time / 60)
    elapsed_secs = int(elapsed_time - (elapsed_mins * 60))
    print(f'running time {elapsed_mins}m{elapsed_secs}s')
    with open(args.log_file_name,'a') as f:
        print('\n',file=f)
        print(f'running time {elapsed_mins}m{elapsed_secs}s',file=f)

