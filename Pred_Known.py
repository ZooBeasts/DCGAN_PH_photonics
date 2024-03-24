import torch
from torch import nn
import cv2
from Dataloader import MMIDataset
import numpy as np

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# load the saved trained Generator info
#model_path = r'C:/Users/Administrator/Desktop/pythonProject/pr1/logs/WGAN77/netG230.pt'
model_path = r'E:/newline1/netG10.pt'

# Load the dataset
dataset = MMIDataset(img_size=64,
                     z_dim=250,
                     points_path=r'C:/Users/Administrator/Desktop/pythonProject/pr1/2000test.csv',
                     img_folder=r'C:/Users/Administrator/Desktop/pythonProject/pr1/Training_Data/image/new',
                     )

# Output the results path & load the data into Generator
results_folder = r'C:\Users\Administrator\Desktop\pythonProject\pr1'
gen = torch.load(model_path)
gen = gen.to(device)
gen = gen.eval()

# Generate the image array from given dataset
def predict(net: nn.Module, points):
    return net(points).squeeze(0).squeeze(0).cpu().detach().numpy()

# Generate the desired number of results and save to path
# 0 means to data 1st row
# 40000 means last row in dataset
stop_p = 100
i = 0

for p in dataset:
    if i >= stop_p:
        break
    data = p[0].to(device, dtype=torch.float).unsqueeze(0)
    img_out = predict(gen, data)
    img = (img_out + 1) / 2
    img = np.round(255 * img)
    img = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

    cv2.imwrite(results_folder + '\\' + 'map200_' + str(i + 1) + '.png', img)
    # cv2.imwrite(results_folder + '\\' + str(i) + '-test.png', img)
    i += 1

