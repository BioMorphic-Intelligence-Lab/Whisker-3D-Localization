import torch
import torch.nn as nn
import numpy as np
from utils import *
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
import time

def train_model(model, train_loader, criterion, optimizer):
    model.train()
    total_loss_error = 0.0
    loss1_metric = 0.0
    loss2_metric = 0.0
    loss3_metric = 0.0
    total_loss1_metric = 0.0
    total_loss2_metric = 0.0
    total_loss3_metric = 0.0
    total_loss_val = 0.0
    loss_val=0.0
    # task_losses = [0.0] * 3  # Initialize a list to store losses for each task

    weight1 = 1  # Set the weight for task 1
    weight2 = 1  # Set the weight for task 2
    weight3 = 1  # Set the weight for task 3

    for inputs, targets in train_loader:
        targets_rad = torch.deg2rad(targets[:, 2])
        cos_values = torch.cos(targets_rad)
        sin_values = torch.sin(targets_rad)
        targets_2d = torch.stack((cos_values, sin_values), dim=1)
        inputs, targets, targets_2d = inputs.to(device), targets.to(device), targets_2d.to(device)

        optimizer.zero_grad()
        # output1, output2, output3 = model(inputs)
        output1,output2,output3 = model(inputs)
        #a<r<b
        r = torch.norm(output3, dim=1)
        r_clipped = torch.clamp(r, 0, 0.8)
        output3_scaled = (output3.transpose(0, 1) * (r_clipped / r)).transpose(0, 1)

        loss1_error = criterion(output1.squeeze(), targets[:, 0])
        loss2_error = criterion(output2.squeeze(), targets[:, 1])

        # r = torch.norm(combined_output,dim=1)
        # r_clipped = torch.clamp(r, 0, 0.8)
        # output3_scaled = (combined_output.transpose(0, 1) * (r_clipped / r)).transpose(0, 1)
        # output3_normalized = output3 / torch.norm(output3, p=1, dim=1, keepdim=True)
        # Calculate task-specific losses
        # loss1 = criterion(output1, targets[:, 0].unsqueeze(1))
        # loss2 = criterion(output2, targets[:, 1].unsqueeze(1))
        loss3_error = nn.MSELoss()(output3_scaled.squeeze(), targets_2d)
        # Apply weights to the losses
        # loss1 = loss1 * weight1
        # loss2 = loss2 * weight2
        loss1_error = loss1_error * weight1
        loss2_error = loss2_error * weight2
        loss3_error = loss3_error * weight3

        loss_sum = loss1_error + loss2_error + loss3_error
        loss_sum.backward()
        optimizer.step()

        loss1_metric = loss1_error.item()*100
        loss2_metric = loss2_error.item()*100
        loss3_metric = custom_periodic_l1_loss(output3_scaled.squeeze(), targets[:,2]).item()
        loss_val = loss1_error.item()+loss2_error.item()+loss3_metric/360
        # Backpropagate and optimize

        
        # Accumulate losses for each task
        # task_losses[0] += loss1.item()
        # task_losses[1] += loss2.item()
        # task_losses[2] += loss3.item()
        total_loss_error += loss_sum.item()
        total_loss1_metric += loss1_metric
        total_loss2_metric += loss2_metric
        total_loss3_metric += loss3_metric
        total_loss_val += loss_val
        # total_loss_metric += loss3_metric.item()
    avg_total_loss_error = total_loss_error / len(train_loader)
    avg_total_loss1_metric = total_loss1_metric / len(train_loader)
    avg_total_loss2_metric = total_loss2_metric / len(train_loader)
    avg_total_loss3_metric = total_loss3_metric / len(train_loader)
    avg_total_loss_val = total_loss_val / len(train_loader)
    # avg_task_losses = [task_loss / len(train_loader) for task_loss in task_losses]

    # return avg_total_loss, avg_task_losses[0], avg_task_losses[1], avg_task_losses[2]
    return avg_total_loss_error,avg_total_loss_val, avg_total_loss1_metric, avg_total_loss2_metric, avg_total_loss3_metric

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

def test_model(model, test_loader, criterion):
    model.eval()
    total_loss_error = 0.0
    loss1_metric = 0.0
    loss2_metric = 0.0
    loss3_metric = 0.0
    total_loss1_metric = 0.0
    total_loss2_metric = 0.0
    total_loss3_metric = 0.0
    total_loss_val = 0.0
    loss_val=0.0
    euclidean_distances = 0.0
    total_samples = 0
    with torch.no_grad():
        for inputs, targets in test_loader:
            targets=targets.to(device)
            targets_rad = torch.deg2rad(targets[:, 2])
            cos_values = torch.cos(targets_rad)
            sin_values = torch.sin(targets_rad)
            targets_2d = torch.stack((cos_values, sin_values), dim=1)
            inputs, targets, targets_2d = inputs.to(device), targets.to(device), targets_2d.to(device)
            output1,output2,output3 = model(inputs)
            x1 = targets[:, 0] * torch.cos(targets_rad) *100
            y1 = targets[:, 0] * torch.sin(targets_rad) *100
            z1 = targets[:, 1] * 100 + 50
            r = torch.norm(output3, dim=1)
            r_clipped = torch.clamp(r, 0, 0.8)
            output3_scaled = (output3.transpose(0, 1) * (r_clipped / r)).transpose(0, 1)
            output_rad = torch.atan2(output3_scaled[:, 1], output3_scaled[:, 0])
            is_negative = output3[:, 1] < 0
            output_rad = torch.where(is_negative, 2*torch.pi + output_rad, output_rad)
            x2 = output1.squeeze() * torch.cos(output_rad) *100
            y2 = output1.squeeze() * torch.sin(output_rad) *100
            z2 = output2.squeeze() * 100
            euclidean_distance = torch.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
            euclidean_distances += euclidean_distance.sum().item()
            total_samples += len(inputs)
            #a<r<b
            loss1_error = criterion(output1.squeeze(), targets[:, 0])
            loss2_error = criterion(output2.squeeze(), targets[:, 1])
            # r = torch.norm(combined_output,dim=1)
            # r_clipped = torch.clamp(r, 0, 0.8)
            # output3_scaled = (combined_output.transpose(0, 1) * (r_clipped / r)).transpose(0, 1)
            # output3_normalized = output3 / torch.norm(output3, p=1, dim=1, keepdim=True)
            # Calculate task-specific losses
            # loss1 = criterion(output1, targets[:, 0].unsqueeze(1))
            # loss2 = criterion(output2, targets[:, 1].unsqueeze(1))
            loss3_error = nn.MSELoss()(output3_scaled.squeeze(), targets_2d)
            loss_sum =  loss1_error + loss2_error + loss3_error
            loss1_metric = loss1_error.item()*100
            loss2_metric = loss2_error.item()*100
            loss3_metric = custom_periodic_l2_loss(output3_scaled.squeeze(), targets[:,2]).item()
            loss_val = loss1_error.item() + loss2_error.item() + loss3_metric / 360
            # Accumulate losses for each task
            # task_losses[0] += loss1.item()
            # task_losses[1] += loss2.item()
            # task_losses[2] += loss3.item()
            total_loss1_metric += loss1_metric
            total_loss2_metric += loss2_metric
            total_loss3_metric += loss3_metric
            total_loss_val += loss_val
            total_loss_error += loss_sum.item()
             
        avg_euclidean_distance = euclidean_distances/ total_samples
        avg_total_loss_error = total_loss_error / len(test_loader)
        avg_total_loss1_metric = total_loss1_metric / len(test_loader)
        avg_total_loss2_metric = total_loss2_metric / len(test_loader)
        avg_total_loss3_metric = total_loss3_metric / len(test_loader)
        avg_total_loss_val = total_loss_val / len(test_loader)
        return avg_total_loss_error, avg_total_loss_val, avg_total_loss1_metric, avg_total_loss2_metric, avg_total_loss3_metric,avg_euclidean_distance