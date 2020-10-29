# README #

This is the repository for the GUI that monitors and assists to the experiments

### What is this repository for? ###

* Quick summary
* Version 0.1

### How do I get set up? ###

* Requires:

* python 2.7

* Cython 0.23 - pip install cython==0.23

* kivy

* kivy garden
```bash
pip install kivy-garden

* matplotlib kivy backend
```bash
garden install matplotlib

## How to commit ##
```bash
#Set up new workspace (folder)
mkdir folderName
git clone https://USERNAME@bitbucket.org/epiclab/gui.git
#Everytime you want to edit anything
git pull origin master
#*edit any file*
git add *
git commit -m "MESSAGE"
git pull origin master
git push origin master

```


### Contribution guidelines ###

* Start by creating basic classes:
* Generic subscriber
* Particular ubscriber to each custom message

### Who do I talk to? ###

* Jonathan Camargo <jon-cama@gatech.edu>
