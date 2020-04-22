# How to use virtual environment (venv) ? 

## What is a python virtual environment in python? 
When running a python script on your machine, there is a godo chance that you are going to use some pakcages or a specific python version. (python2 or python3 for example, or python 3.6 vs. python 3.7. ) Problem is when you send this project to a friend - and he tries to launch it from his computer, which has different version of python or the packages. 
To solve this problem - veritual environment, or "venv" in short was created. A python virtual environment allows you to run a virtual environment with a specific version of pytohn and specific packages (and specific versions, including old versions) , regardless of the ones installed on the computer. 


## How to install venv - 
```bash
python3 -m venv envname
```
this will create a directory named envname which will include a python3 version available from it. 


**To start the venv - **
cd to the directory where you installed the "venv". Inside you will find a folder called "env" . 
Type the command - 
```bash
source env/bin/activate 
```

This will start the virtual environment - and you will see an output like this - 
```bash
(env) idan@idan-X540LA:~/python/storage$
```
please note that on the side of the input line you will see "(env)" text. 

While the "venv" is working, when you will execute python scripts, it will be executed with the python binary installed in the "venv" and not in your computer. For example, if you have python2 installed on your machine, but your virtual environment has python3 in it, then all executed scripts will be executed with python3, as this is the binary installed in the "venv". 
To check that the python command refers to the version in the vitual environment - you can check the path where "python" command reffers too. In my example I use ```python3``` which will refer to the venv and not the binary installed on my machine. 
```bash
which python3 
will output a path for a binary at the venv - 
		(env) idan@idan-X540LA:~/python/storage$ which python
		/home/idan/python/storage/env/bin/python
```

To stop the venv - user ```deactivate``` command, which will dismiss the ```(env)``` text near the text input. 
```bash
$ deactivate
		(env) idan@idan-X540LA:~/python/storage$ deactivate
		idan@idan-X540LA:~/python/storage$ 
```



## Using packages in venv (virtual environment) - ( An introduction to pip)
How to manage packages? 
Inside the venv - you can use pip, in my case pip3 for python3 . Pip (said like "pay-pee") is a package manager for python. It allows you to install packages in python. A package in python is basically a module class which you cna use in your code. (In this project called "Storage System" for example I use Flask package which is used to create python web applications. ) 

You can use pip on your machine - but when using "venv" you can also use pip to install packages, regardless of the ones already installed on your machine. For example, let's say you want to run pyton code which requires a specific package but you don't later to keep it installed on your machine (And save volume space) - what should you do? You can install it in "venv" , and when stopping the venv, the package won't be used or loaded. Actually, the package will be installed in the ```env/``` directory - so by deleting it you will delete the "venv" with all of its package - and without effecting the others installed on your machine. 
Another example for using virtual environment (venv) and pip with it is when you need to run a legacy python applicaitno (Legacy application = an old application which uses old versions of python/pakcages/any other software) and you need to have old versions of packages in order to run this application. In such case, assuming you have a newer version of the packages on your machine - you will have to uninstall them and then install the old one just to run the application. However with virtual environment "venv" you can independently run old python version and old packages ONLY in the virtual environment ("venv") without effecting the ones already installed on your computer. 



## How to install a new package using pip? 
```bash
pip install packagename #Will install package named packagename
pip list #Will show packages list. 
pip uninstall packagename #Will un-install a package named packagename, assuming it is already installed. 
```

When running this command - make sure to see whether you are using the virtual environment ("venv") or not! If you will type these command without activating the "venv" then you will execute this function on your machine itself. On the contrary, when executing these command while activating the "venv" the installation will be available only in the "venv" itself and not effecting the python3 installation on your machine. 

### How to create requirement.txt file? 
a ```requirement.txt``` file is reffering to a file which includes all needed package to run a python software/application. You can use such a file to "easy" install the list of pakcages in the ```requirements.txt``` file. (This file name is commonly used, though other names can be given. ) 

To list the current package in you venv, type the following command. Note - if you are not using the venv, then it will show you the list on the installatino of your machine. 
```bash
$pip freeze
```

To create the ```requirements.txt``` file - just write the output to the file - 
```bash
$pip freez >> requirements.txt
```

to install the requirements in another machine or other venev - 
```bash
$pip intall -r requirements.txt
```

For my application - make sure to install it in the venv - so you won't effect other packages installations on your machine! 


## How to delete the virtual environment? 
Very simple - just delete the "env" directory. This will erase the python binary installed IN THE VENV. Also it will erase all pip packages in the venv. This will not effect any other installation on your machine - as the virtual environment is independent and not related to other installations on your machine. 


