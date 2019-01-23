# Orchid_SIOT

This project contains the Orchid SIOT code
============

Some relevant links: 

Presentation URL : https://youtu.be/R0cGr9C_vuw

Code and Data : https://github.com/Bealln/Orchid_SIOT

Website : https://bealln.github.io/Orchid_SIOT/Webapp_orchid/index.html (Please not graphics on the website dont show until one of the headers is selected) 

Note the code runs in Python 3.X and uses multiple libraries which should be imported for a correct functioning of the code.

Please note that you might have to install anaconda if you are not working from a UNIX-based system. You can install all of these with the following command: pip3 install numpy scipy matplotlib jupyter

Contents
----------
The webb app is formed of three files, the home page(index.htlm), the about page(generic.html) and an elements file (elements.html) for future development of the app. It also includes the credits and license for the template from TEMPLATED, which was used for tha basic html and css of the website.  

[Data treatment](https://github.com/Bealln/Orchid_SIOT/tree/master/Webapp_orchid/Data_treatment) Containt the relevant documentation for sensing, collection and treatment of the data. It also contains the jupyter notebook(Data_treatment.ipynb) with the data treatment procedure. 


[Data sensing](https://github.com/Bealln/Orchid_SIOT/tree/master/Webapp_orchid/Data_treatment/Data_sensing)     This folder constains the python file(data_to_drive.py) to run the sensing code, which allows to obtain the sensing data and Weather API data.

[Data collected](https://github.com/Bealln/Orchid_SIOT/tree/master/Webapp_orchid/Data_treatment/Data_collected)    This folder contains the python file to download the data from drive to a csv(Download_data_fromdrive.py) as well as the raw cloud and local data. 

[Data treated](https://github.com/Bealln/Orchid_SIOT/tree/master/Webapp_orchid/Data_treatment/Data_treated) This folder constains the treated csv filed needed for visualization both in the jupyter notebook and the web app. 
