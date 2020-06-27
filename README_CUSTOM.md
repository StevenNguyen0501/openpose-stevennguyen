# ADDITIONAL STEPS TO INSTALL OPENPOSE AND BUILD API DOCKER
These addtional steps aim to pass through some issues occur when installing [OpenPose project] to local machine.
**Keep in mind** that he installation process mainly use [original installation document].

**Prerequisites**: Assume that **NVIDIA driver (>= 410), CUDA (10.0), CuDNN (7.5) and OpenCV-Python** have been installed properly on the target machine (OS: Ubuntu 18.04).

# Run OpenPose on local machine
### Create a virtual environment (optional)
``` sh
$ sudo apt install -y python3-venv
$ mkdir environment_directory
$ cd environment_directory
$ python3 -m venv sample_environment
$ source sample_environment/bin/activate
```
### Caffe (for CUDA version)
Install:
``` sh
sudo apt install caffe-cuda
```
If failed, try to install [these packages] first and then do the above step again.
Double check if the *build/* folder has downloaded **caffe source** (refer to [this issue])

### CMake
CMake UI
``` sh
sudo apt-get -y install cmake
sudo apt-get -y install cmake-qt-gui
```
Create *build/* folder. Press **Configure** and **Generate** button and move to **Build step**.

If not succeed, try to do these following steps in the terminal:
- Fix [libboost issue]:
``` sh
sudo apt-get install libboost-all-dev
```
- The error may be because of the mismatch of Cmake version. To get over this issue, try to follow these steps 
in the *Install CMake through the Ubuntu Command Line* section on [this article] and run directly in the console using [the answer] 
of Basile Starynkevitch. Then execute the **Build step** (*CMake Command Line Configuration (Ubuntu Only)* in installation link)

Run an example to test. 

# Export Python API ([link setup])
- Remember to complile and enable BUILD_PYTHON. 

- Config PYTHON_PATH
``` sh
export PYTHONPATH=/path/to/build/python:/path/to/openpose
```

Feel free to contact stevennguyenusa19@gmail.com when you have troubles with the installation.

# Docker
 Link [Docker Hub]
 
 Link [Dockerfile]

[OpenPose Project]: <https://github.com/CMU-Perceptual-Computing-Lab/openpose>
[original installation document]: <https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation.md>
[this link]: <https://vitux.com/install-python3-on-ubuntu-and-set-up-a-virtual-programming-environment/>
[these packages]: <http://www.programmersought.com/article/2083763545/>
[this issue]: <https://github.com/CMU-Perceptual-Computing-Lab/openpose/issues/423>
[libboost issue]: <https://github.com/CMU-Perceptual-Computing-Lab/openpose/issues/1109>
[this article]: <https://vitux.com/how-to-install-cmake-on-ubuntu-18-04>
[the answer]: <https://stackoverflow.com/questions/7859623/how-do-i-use-cmake>
[link setup]: <https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/modules/python_module.md>
[Docker Hub]: <https://hub.docker.com/repository/docker/stevennguyen51/openpose>
[Dockerfile]:<https://github.com/StevenNguyen050196/openpose>