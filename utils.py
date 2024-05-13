import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset
import csv
import os
import pandas as pd
import re
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def extract_hyperparameters_from_filename(filename):
    match = re.match(r"best_model_ts_(\d+)_bs_(\d+)_lr_(\d+\.\d+)_reg_(\d+)_do_(\d+\.\d+)_loss_\d+\.\d+", filename)
    if match:
        ts = int(match.group(1))
        bs = int(match.group(2))
        lr = float(match.group(3))
        reg = float(match.group(4))
        do = float(match.group(5))
        return ts, bs, lr, reg, do
    else:
        return None
    
def load_trial_data(data_folder, trial_name):
    data = []
    file_path = os.path.join(data_folder, f"{trial_name}.csv")
    with open(file_path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        next(reader)
        for row in reader:
            data.append([float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5])])
    return data

def load_data(data_folder):
    train_data = []
    val_data = []
    test_data = []
    test_trial_sizes=[]
    val_trial_sizes=[]
    train_trial_sizes=[]

    for A in range(0, 360, 45):
        for B in range(0, 11):
            trial_name_train = f"{A}d-{B}x-10y-1cms-train"
            trial_name_val = f"{A}d-{B}x-10y-1cms-val"
            trial_name_test = f"{A}d-{B}x-10y-1cms-test"
            train_trial_data = load_trial_data(data_folder, trial_name_train)
            val_trial_data = load_trial_data(data_folder, trial_name_val)
            test_trial_data = load_trial_data(data_folder, trial_name_test)
            train_data.extend(train_trial_data)
            val_data.extend(val_trial_data)
            test_data.extend(test_trial_data)
            train_trial_sizes.append(len(train_trial_data))
            val_trial_sizes.append(len(val_trial_data))
            test_trial_sizes.append(len(test_trial_data))


    return train_data, val_data, test_data, train_trial_sizes,val_trial_sizes,test_trial_sizes
        
def dataset( data, targets, sequence_length, trial_sizes):
        data = data
        targets = targets
        sequence_length = sequence_length
        trial_sizes = trial_sizes
        output_pair=[]
        for i in range (len(trial_sizes)):
            trial_size = trial_sizes[i]
            start_idx = sum(trial_sizes[:i])
            end_idx = start_idx + trial_size - sequence_length + 1
            for j in range(start_idx, end_idx, 1):
                input_data = data[j:j + sequence_length]
                target_data = targets[j + sequence_length - 1]
                input_data = torch.tensor(input_data, dtype=torch.float32)
                target_data = torch.tensor(target_data, dtype=torch.float32)
                output_pair.append((input_data,target_data))
        return output_pair  

def save_loss_image(train_losses, val_losses, output_file):
    epochs = len(train_losses)
    plt.plot(range(1, epochs + 1), train_losses, label='Train Loss')
    plt.plot(range(1, epochs + 1), val_losses, label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig(output_file)
    plt.close()

def min_max_normalization(data):
    min_val = np.min(data, axis=0)
    max_val = np.max(data, axis=0)
    normalized_data = (data - min_val) / (max_val - min_val)
    return normalized_data

def squared_circular_mean_squared_error(pred, target):
    loss = (1 - torch.cos(pred - target)) ** 2
    return torch.mean(loss)



def custom_periodic_l1_loss(predictions, targets):

    predicted_rad = torch.atan2(predictions[:, 1], predictions[:, 0])
    is_negative = predictions[:, 1] < 0
    predicted_rad = torch.where(is_negative, 2*torch.pi + predicted_rad, predicted_rad)
    predicted_deg = torch.rad2deg(predicted_rad)
    diff = torch.abs(predicted_deg - targets)
    loss = torch.where(diff <= 180, diff , (360 - diff) )
    
    return loss.mean()

def custom_periodic_l2_loss(predictions, targets):

    predicted_rad = torch.atan2(predictions[:, 1], predictions[:, 0])
    is_negative = predictions[:, 1] < 0
    predicted_rad = torch.where(is_negative, 2*torch.pi + predicted_rad, predicted_rad)
    predicted_deg = torch.rad2deg(predicted_rad)
    diff = torch.abs(predicted_deg - targets)
    loss = torch.where(diff <= 180, diff**2 , (360 - diff)**2 )
    
    return loss.mean()

def mean_angular_error(predictions, targets):

        l1=nn.L1Loss(predictions, targets)
        loss_rad = torch.asin(l1/2.0)
        loss_deg = torch.rad2deg(loss_rad)
        
        return loss_deg.mean()

def save_output_images(model, data_loader, output_file_prefix,sampling_rate):
    model.eval()
    all_outputs1 = []
    all_outputs2 = []
    all_outputs3 = []
    all_labels1 = []
    all_labels2 = []
    all_labels3 = []
    
    with torch.no_grad():
        for inputs, labels in data_loader:
            inputs = inputs.to(device)

            output1,output2,output3 = model(inputs)
            predicted_rad = torch.atan2(output3[:, 1], output3[:, 0])
            is_negative = output3[:, 1] < 0
            predicted_rad = torch.where(is_negative, 2*torch.pi + predicted_rad, predicted_rad)
            predicted_deg = torch.rad2deg(predicted_rad)
            all_outputs1.append(output1.cpu().numpy())
            all_outputs2.append(output2.cpu().numpy())
            all_outputs3.append(predicted_deg.cpu().numpy())

            all_labels1.append(labels[:, 0].cpu().numpy())
            all_labels2.append(labels[:, 1].cpu().numpy())
            all_labels3.append(labels[:, 2].cpu().numpy())

    all_outputs1 = np.concatenate(all_outputs1, axis=0)
    all_outputs2 = np.concatenate(all_outputs2, axis=0)
    all_outputs3 = np.concatenate(all_outputs3, axis=0)
    all_labels1 = np.concatenate(all_labels1, axis=0)
    all_labels2 = np.concatenate(all_labels2, axis=0)
    all_labels3 = np.concatenate(all_labels3, axis=0)

    for i, (label, color) in enumerate(zip(["Label 1", "Label 2", "Label 3"], ["blue", "green", "red"])):
        plt.figure(figsize=(10, 6))
        
        # downsampling
        sampled_indices = range(0, len(all_outputs1), sampling_rate)
        plt.scatter(sampled_indices, all_outputs1[sampled_indices] if i == 0 else all_outputs2[sampled_indices] if i == 1 else all_outputs3[sampled_indices], 
                    label='Predicted', color=color, s=0.5)
        plt.scatter(sampled_indices, all_labels1[sampled_indices] if i == 0 else all_labels2[sampled_indices] if i == 1 else all_labels3[sampled_indices], 
                    label=label + ' (Ground Truth)', color='black', marker='x', s=0.5)
        
        plt.legend()
        plt.xlabel('Sample Index')
        plt.ylabel('Output')
        plt.title(f'Output {i+1}')
        output_file = f'{output_file_prefix}_output_{i+1}.png'
        plt.savefig(output_file)
        plt.close()