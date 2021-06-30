# UEFA Refereeing Assistance Program Viewer
With the the requirement of the (paid) Mulppy application to view the 2020 versions (and possibly future versions) of UEFA's Refereeing Assistance Program, I have created a simple GUI in Python to view the clips and associated technical decision (and if applicable, UEFA's explanation of the decision).


## Installation
Python version used: `Python 3.7`
Use the package manager pip to install the below packages
```bash
pip install PySimpleGUI
pip install Pillow
pip install vlc	
```

## Usage

Using the application is very similar to using previous versions of UEFA's Referee Assistance Programs. However, when the application is first launched, the user must specify the location of the *Resource* folder. Below is the file structure of the 2020-1 version. Hence the filepath you must navigate to in the pop up window will be `...\UEFA-2020-1\UEFA-2020-1\Resource`.


``` bash
UEFA-2020-1/
├─ UEFA-2020-1/
│  ├─ Resource/
│  │  ├─ medias/
│  │  │  ├─ clips/
│  │  │  ├─ images/
│  │  │  │  ├─ explanations/
│  │  │  │  ├─ decisions/
│  │  │  ├─ th/
│  │  ├─ en/
│  ├─ ReadmeMulppyESP.pdf
│  ├─ ReadmeMulppyENG.pdf
│  ├─ UEFA-2020-1.mpp
```