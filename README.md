# Ubuntu_Server_Setting

## Ubuntu_Desktop GUI install
```bash
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install ubuntu-desktop ssh -y
```

## Install Usefull library
```bash
sudo python3 -m pip install --upgrade pip&&
sudo python3 -m pip install -U numpy &&
sudo python3 -m pip install -U matplotlib&&
sudo python3 -m pip install -U pandas&&
sudo python3 -m pip install -U scipy&&
sudo python3 -m pip install -U scikit-learn&&
sudo python3 -m pip install -U jupyter&&
sudo python3 -m pip install -U cython
```

## Install Usefull Utility
```bash
sudo apt-get install python-pip python3-pip  python-dev python3-dev python3-numpy python-numpy git vim curl wget cmake build-essential tmux htop unzip locales
```

## Install NVIDIA_Driver
```bash
# Add graphic driver repository
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update -y

# Check available driver version
apt-cache search nvidia

# Install driver
sudo apt-get install nvidia-driver-<version>
sudo reboot

# Checking installed driver
nvidia-smi
```

## Install CUDA
1. Install from https://developer.nvidia.com/cuda-downloads
2. Add CUDA PATH in ~/.profile and /etc/environment
- ~/.profile
```bash
# set PATH for CUDA installation
if [ -d "/usr/local/cuda/bin/" ]; then
    export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
    export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
fi
```
- /etc/environment
```bash
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/local/cuda/bin"
```
3. Apply changes
```bash
source ~/.profile
source /etc/environment

# or
sudo reboot
```
## Install CUDNN
1. Install from https://developer.nvidia.com/cudnn

## Setting Jupyter_Notebook
1. Install Jupyter_Notebook
```bash
sudo pip3 install jupyter
```
2. Generate Config file
```bash
jupyter notebook --generate-config
```
3. Modify Config file
```bash
vim ~/.jupyter/jupyter_notebook_config.py
# c.NotebookApp.ip
# c.NotebookApp.open_browser
# c.NotebookApp.password
# c.NotebookApp.port
```
4. Add scripts in /etc/rc.local
-/etc/rc.local
```bash
su <username> -c "jupyter notebook --config=/location/of/your/config/file/.jupyter/jupyter_notebook_config.py --no-browser --notebook-dir=/location/of/yournotebooks" &
```

## Install Jupyter_HUB
1. Install Jupyter_HUB
```bash
curl https://raw.githubusercontent.com/jupyterhub/the-littlest-jupyterhub/master/bootstrap/bootstrap.py | sudo -E python3 - --admin \<admin-user-name>
```
2. Additional information of Jupyter_HUB https://github.com/jupyterhub/the-littlest-jupyterhub

## Mounting hard disk
1. Check UUID
```bash
sudo blkid
```
2. Add directory for mounting
```bash
sudo mkdir -p /<name of directory>
```
3. Add information in /etc/fstab
```bash
sudo vim /etc/fstab
```
- /etc/fstab
```bash
UUID=<UUID of hard disk> <directory for mounting> <file system> <options> <dump setting> <file confirm option>
# Example
UUID=f5a90ae5-f49d-4d7d-8ab7-d1050ef911e9 /hdd1 ext4 defaults 0 0
```
4. Mount hard disk
```bash
sudo mount -a
```
5. Checking mounted hard disk lists
```bash
df -h
```

## Useful commands
- Checking share of CPU and DRAM
```bash
htop
```
- Checking storage of disks
```bash
df -h
```
- Checking OS information
```bash
lsb_release -a
```
- Checking CPU model information
```bash
cat /proc/cpuinfo | grep CPU | head -1
```
- Checking CPU core numbers
```bash
cat /proc/cpuinfo | grep CPU | wc -l
```
- Checking Network information
```bash
ifconfig
```

## Server Stress test
- CPU
```bash
sudo apt-get install stress-ng stress -y
stress -c <number of cores> --io 4 --hdd 1 --hdd-bytes 1024m -t 36000m --vm-bytes $(awk '/MemFree/{printf "%d\n", $2 * 0.097;}' < /proc/meminfo)k --vm-keep -m 10
```
- GPU
```bash
CUDA_VISIBLE_DEVICES=0 python3 gpu_test.py &
CUDA_VISIBLE_DEVICES=1 python3 gpu_test.py &
CUDA_VISIBLE_DEVICES=2 python3 gpu_test.py &
...
```

