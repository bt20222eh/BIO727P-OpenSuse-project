# BIO727P-OpenSuse-SOFTWARE-DEVELOPMENT-PROJECT
HUMAN POPULATION GENETIC ANALYSIS WEB APPLICATION
1. To use this configuration, python must be installed locally. This can be done with Homebrew by passing the following command from your command line locally:
   /bin/bash -c "$(curl - 
   fsSLhttps://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
2. Then, install Python by running:
   brew install python
3. Download pip and run the script to install pip:
   curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
4. Install the virtual enviroment package:
   python3 -m pip install virtualenv
5. create a virtual enviroment in your main flask app directory
   python3 -m venv myenv
6. Activate the virtual enviroment:
   source myenv/bin/activate
7. Lastly, ensure all packages required for the web app configuration are installed into your python enviroment using:
   pip install Flask SQLAlchemy matplotlib pandas numpy seaborn
   
