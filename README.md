# 3D-Scene Reconstruction using Deep Learning
Given a set of images of a crime scene, we plan on reconstructing the scene in 3D. This is done by Utilising multiple views of a scene to generate a 3D rendering of the same. We will also be looking into further optimizing the baseline output by the neural net with a GCN.

## Team Details:

| Name        |      SRN      | Email                   |
| ----------- | ------------- | ----------------------  |
| Dhruval PB  | PES1UG19CS313 | dhruvalpb@pesu.pes.edu  |
| Sai Mihir J | PES1UG19CS418 | saimihir.j@gmail.com    |
|Akash Mehta  | PES1UG19CS040 | akashmehta556@gmail.com |
			

## Directory Structure
## 1. GCNDepth: 
This folder contains the implementation of a Graph Convolution Neural Network that performs Monocular Depth Estimation. 
### Setup

#### Requirements:
- PyTorch1.2+, Python3.5+, Cuda10.0+
- mmcv==0.4.4

```bash
# This creates a new conda enviroment to run the model
conda create --name gcndepth python=3.7
conda activate gcndepth

# This installs the right pip and dependencies for the fresh python
conda install ipython
conda install pip

# Install required packages from requirements.txt
pip install -r requirements.txt
```

### Running the Code:
```bash
conda activate gcndepth
cd ./GCNDepth
python3 infer.py
```
This will generate depth maps which will be stored in the ```GCNDepth/assets/Outputs/Grayscale``` folder.
We've written scripts that back project these disparity maps into point clouds and save them as npy files in ```3DRenders/PointClouds``` folder.

## 2. CameraOrientation: 
This folder contains an implementation of a Monocular SLAM algorithm which we use to estimate camera position and orientation.

### Setup
#### Docker:
```bash
xhost +local:docker
sudo apt install nvidia-docker2
sudo systemctl daemon-reload
sudo systemctl restart docker
docker build -t twitchslam .
```
### Running the code:
```bash
chmod +x ./Run.sh
./Run.sh      # This will start the docker container
cd twitchslam # Once the container is up and running, go to the twitchslam directory
chmod +x ./Predict.py
./Predict.py  # This generates the camera orientation predictions on the dataset we've used
```

## 3. 3DRender: 
This folder contains the code for plotting the point clouds in 3D using pyQt.
### Setup:
```bash
pip install numpy pyqtgraph
```

### Running the Code:
```bash
python3 Plotter.py
```
