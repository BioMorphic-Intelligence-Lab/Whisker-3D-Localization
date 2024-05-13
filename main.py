import torch
import torch.nn as nn
import os
from torch.utils.data import DataLoader
from train import *
from model import *
from utils import *
from sklearn.model_selection import ParameterGrid
import copy
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Argument Parser")
    parser.add_argument("--time_sequence", type=int, nargs="+", default=[40], help="Time sequence number")
    parser.add_argument("--batch_sizes", type=int, nargs="+", default=[32], help="Batch sizes")
    parser.add_argument("--learning_rates", type=float, nargs="+", default=[0.0001], help="Learning rates")
    parser.add_argument("--regularization_values", type=float, nargs="+", default=[0.0], help="Regularization values")
    parser.add_argument("--dropout_values", type=float, nargs="+", default=[0.0], help="Dropout values")
    parser.add_argument("-train", action="store_true", help="Train the model")
    parser.add_argument("-test", action="store_true", help="Test the model")
    parser.add_argument("--model_file", type=str, default=None, help="Path to the model file for testing")
    return parser.parse_args()

def main():
    # load data
    data_folder = "./dataset/"
    train_data, val_data, test_data,train_trial_sizes,val_trial_sizes,test_trial_sizes = load_data(data_folder)

    train_data = np.array(train_data)
    val_data = np.array(val_data)
    test_data = np.array(test_data)

    train_input= train_data[:, (0, 1,2)]
    val_input= val_data[:, (0, 1,2)]
    test_input= test_data[:, (0, 1,2)]

    train_output = min_max_normalization(train_data[:, 3: 5])
    train_output = np.hstack((train_output, train_data[:, 5].reshape(-1, 1)))
    val_output = min_max_normalization(val_data[:, 3: 5])
    val_output = np.hstack((val_output, val_data[:, 5].reshape(-1, 1)))
    test_output = min_max_normalization(test_data[:, 3: 5])
    test_output = np.hstack((test_output, test_data[:, 5].reshape(-1, 1)))

    num_epochs = 30
    input_size = 3
    num_layers = 3
    hidden_size = 32

    criterion = nn.L1Loss()    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    if args.train:
        best_loss = float('inf')
        best_model = None
        best_params = None

        for params in ParameterGrid({
            'time_sequence': time_sequence_values,
            'batch_size': batch_sizes,
            'lr': learning_rates,
            'regularization': regularization_values,
            'dropout': dropout_values,
        }):
            best_epoch_model = None
            best_epoch_loss = float('inf')

            # create data loader, model, and optimizer
            train_loader = DataLoader(dataset(train_input, train_output, params['time_sequence'],train_trial_sizes), batch_size=params['batch_size'], shuffle=True)
            val_loader = DataLoader(dataset(val_input, val_output, params['time_sequence'],val_trial_sizes), batch_size=params['batch_size'], shuffle=False)
            model = ThreeLayerLSTM(input_size, hidden_size, num_layers, params['dropout']).to(device)
            optimizer = torch.optim.Adam(model.parameters(), lr=params['lr'], weight_decay=params['regularization'])

            # save training and validation loss
            train_losses = []
            val_losses = []
            # train_each_losses_1 = []
            # val_each_losses_1 = []
            # train_each_losses_2 = []
            # val_each_losses_2 = []
            # train_each_losses_3 = []
            # val_each_losses_3 = []

            # training and validate the model
            for epoch in range(num_epochs):
                train_loss, save_loss_train, train_each_loss_1,train_each_loss_2,train_each_loss_3= train_model(model, train_loader, criterion, optimizer)
                val_loss, save_loss_val, val_each_loss_1,val_each_loss_2,val_each_loss_3,l2_val = test_model(model, val_loader,criterion)
                print(f"Epoch [{epoch+1}/{num_epochs}], train_loss: {train_loss:.4f},save_loss_train: {save_loss_train:.4f}, train_each_loss_1: {train_each_loss_1:.4f},train_each_loss_2: {train_each_loss_2:.4f},train_each_loss_3: {train_each_loss_3:.4f}, val_loss: {val_loss:.4f},save_loss_val: {save_loss_val:.4f}, val_each_loss_1: {val_each_loss_1:.4f},val_each_loss_2: {val_each_loss_2:.4f},val_each_loss_3: {val_each_loss_3:.4f},val_l2: {l2_val:.4f}")

                # save the model of best performance
                if save_loss_val < best_epoch_loss:
                    best_epoch_loss = save_loss_val
                    best_epoch_model = copy.deepcopy(model.state_dict())
            
                train_losses.append(save_loss_train)
                val_losses.append(save_loss_val)        
                # train_each_losses_1.append(train_each_loss_1)
                # val_each_losses_1.append(val_each_loss_1)  
                # train_each_losses_2.append(train_each_loss_2)
                # val_each_losses_2.append(val_each_loss_2)  
                # train_each_losses_3.append(train_each_loss_3)
                # val_each_losses_3.append(val_each_loss_3)  


            if best_epoch_loss < best_loss:
                best_loss = best_epoch_loss
                best_model = best_epoch_model
                best_params = params

            print(f' best loss for this hyperparameter setting : {best_epoch_loss:.4f}')
            val_model_folder = 'val_model_save'
            os.makedirs(val_model_folder, exist_ok=True)
            val_model_file_name = f'{val_model_folder}/val_model_ts_{params["time_sequence"]}_bs_{params["batch_size"]}_lr_{params["lr"]}_reg_{params["regularization"]}_do_{params["dropout"]}_loss_{best_epoch_loss:.4f}.pt'
            torch.save(best_epoch_model, val_model_file_name)

            model.load_state_dict(best_epoch_model)
            val_loss, save_loss_val, val_each_loss_1,val_each_loss_2,val_each_loss_3,l2_val = test_model(model, val_loader,criterion)

            # val_image_folder = 'val_image_save'
            # os.makedirs(val_image_folder, exist_ok=True)
            # val_output_image_file = f'{val_image_folder}/val_output_images_ts_{params["time_sequence"]}_bs_{params["batch_size"]}_lr_{params["lr"]}_reg_{params["regularization"]}_do_{params["dropout"]}_loss_{best_epoch_loss:.4f}.png'
            # save_output_image(model, val_loader, val_output_image_file,1)

            # val_loss_image_file = f'{val_image_folder}/val_loss_image_ts_{params["time_sequence"]}_bs_{params["batch_size"]}_lr_{params["lr"]}_reg_{params["regularization"]}_do_{params["dropout"]}_loss_{best_epoch_loss:.4f}.png'
            # save_loss_image(train_losses,val_losses, val_loss_image_file)

            print(f"Model with params {params} saved.")
        
        print(f"Best Parameters:")
        print(f"Time Sequence: {best_params['time_sequence']}")
        print(f"Batch Size: {best_params['batch_size']}")
        print(f"Learning Rate: {best_params['lr']}")
        print(f"Regularization: {best_params['regularization']}")
        print(f"Dropout: {best_params['dropout']}")

        # save best model
        best_model_folder = 'best_model_save'
        os.makedirs(best_model_folder, exist_ok=True)   
        best_model_file_name = f'{best_model_folder}/best_model_ts_{best_params["time_sequence"]}_bs_{best_params["batch_size"]}_lr_{best_params["lr"]}_reg_{best_params["regularization"]}_do_{best_params["dropout"]}_save_loss_test_{save_loss_test:.4f}.pt'
        torch.save(best_model, best_model_file_name)
        print(f"The best model is saved as {best_model_file_name}.")
    
    if args.test:
        # use best hyper-parameters setting to test
        ts_test, bs_test, _, _, do_test = extract_hyperparameters_from_filename(args.model_file)
        test_loader = DataLoader(dataset(test_input, test_output, ts_test, test_trial_sizes), batch_size = bs_test, shuffle=False)
        model = ThreeLayerLSTM(input_size, hidden_size, num_layers, do_test).to(device)
        best_model_state_dict = torch.load('best_model_save/' + args.model_file)
        model.load_state_dict(best_model_state_dict)
        test_loss, normalized_test_loss, test_each_loss_1 ,test_each_loss_2,test_each_loss_3, l2_test = test_model(model, test_loader,criterion)
    
        print(f"Test result:")
        print(f"\ntest_loss: {test_loss:.4f}, normalized test loss: {normalized_test_loss:.4f}")
        print(f"\nTest mean MAE loss R: {test_each_loss_1:.4f}")
        print(f"\nTest mean MAE Loss H: {test_each_loss_2:.4f}")
        print(f"\nTest mean MSE Loss O: {test_each_loss_3:.4f}")
        print(f"\nTest L2: {l2_test:.4f}")
        # print(f"RMSE: {rmse:.4f}")
        # print(f"Each RMSE_X: {each_rmse_1:.4f}")
        # print(f"Each RMSE_Y: {each_rmse_2:.4f}")
        # print(f"Each RMSE_Z: {each_rmse_3:.4f}")

    # save output image
    # test_image_folder = 'test_image_save'
    # os.makedirs(test_image_folder, exist_ok=True)
    # test_image_file = f'{test_image_folder}/test_output_images_ts_{best_params["time_sequence"]}_bs_{best_params["batch_size"]}_lr_{best_params["lr"]}_reg_{best_params["regularization"]}_do_{best_params["dropout"]}_save_loss_test_{save_loss_test:.4f}.png'
    # save_output_image(model, test_loader, test_image_file,1)

    print("Best model saved.")

if __name__ == '__main__':
    # Setting hyperparameters
    args = get_args()
    time_sequence_values = args.time_sequence
    batch_sizes = args.batch_sizes
    learning_rates = args.learning_rates
    regularization_values = args.regularization_values
    dropout_values = args.dropout_values
    main()