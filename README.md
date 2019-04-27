# Ankita Paint
A well designed MS-Paint like paint program written in PyQt4

**Dependency**  
* python-qt4  

### Description
This paint program is aimed at ease of use, with many useful features.  
This is a MS-Paint or xpaint alternative for linux users. But to increase  
ease of use, it is single window program (unlike xpaint).

### Build
If can build the c++ extension lib for fast floodfill if you have a slow computer.  
Download libqt4-dev and then build by running this command...  
    `python setup.py compile`

### Installation
To Install this program open terminal inside ankita-master directory.  
And then run following command..  
    `sudo pip install .`  

To uninstall run..  
    `sudo pip uninstall ankita`


### Usage
To run after installing, type command..  
  `ankita`  
Or  
  `ankita image.jpg`  
If you want to run this program without/before installing, then  
Open terminal and change directory to ankita-master and run  
  `./run.sh`  
Or  
  `./run.sh image.jpg`  

