# BIO727P-OpenSuse-SOFTWARE-DEVELOPMENT-PROJECT
**HUMAN POPULATION GENETIC ANALYSIS WEB APPLICATION:**

This repository contains the configuration and instructions necessary to set up and run a web application for human population genetic analysis. Follow these steps carefully to ensure a smooth setup and execution of the web application on your system.

**Prerequisites:**
1. Install Homebrew (macOS Package Manager) if it's not already installed. Open your terminal and run the following command:
``` /bin/bash -c "$(curl - fsSLhttps://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)```
2. Install Python using Homebrew by executing the command below in your terminal:
   ```brew install python```
3. Download and Install pip (Python Package Installer) by running these commands in your terminal:
   ```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
   python3 get-pip.py```
4. Install virtualenv (Virtual Environment) package to create isolated Python environments:
   ```python3 -m pip install virtualenv```
5. Create a virtual enviroment in your main flask app directory:
   ```python3 -m venv myenv```
6. Activate the Virtual Environment with the command:
   ```source myenv/bin/activate```
7. Install Required Python Packages for the web application. Ensure you are in the Flask app directory and your virtual environment is activated, then run:
   ```pip install Flask SQLAlchemy matplotlib pandas numpy seaborn```
   
**Construct the database:**
1. Download DB Browser for SQLite - For macOS, download the latest version (.dmg file) from the official website and drag the application to your Applications folder.
2. Create a New Database:
- Open DB Browser for SQLite and click "New Database". Name it "analysis.db" and save it in your Flask app's parent directory.
3. Create the Database Schema:
-  Navigate to the "Execute SQL" tab and paste the SQL commands from your "schema.sql" file into the SQL terminal.
-  Execute the commands to create your database schema.
4. Verify Database Schema:
- Navigate to the "Database Schema" tab to ensure all tables are visible and correctly reference all primary and foreign keys.
5. Import Data from TSV Files:
- For each table, go to File > Import > Table from CSV file.
- Ensure the table name before import matches the schema name to avoid duplicate tables.
- Select and import each .tsv file located in "main/web_app/tables" according to the specified order: SNPData, SampleData, SamplePopulation, ClusteringAnalysis, AdmixtureAnalysis. This order helps avoid foreign key constraints and mismatches.
6. To enhance the performance of your application by optimising database queries, index the most used database tables and columns:
- Execute the "index.sql" commands in the "Execute SQL" tab
  *Creating indexes on frequently accessed data can significantly improve query performance, especially for large datasets.*
7. Save the Populated Database:
- Save the database file with the populated tables to your Flask app's parent directory.

**Final steps:**
*After setting up the Python environment and constructing the database, your application is ready to run. Follow the specific instructions provided in your Flask app documentation to start the web server and access the application*
- execute ```export FLASK_APP=web_app/app``` from your flask parent directory

**Troubleshooting:**
*If you encounter any issues during setup, please ensure you have followed all steps correctly and in order. For specific errors, refer to the documentation or help forums for the tools and libraries you're using (Python, Flask, SQLAlchemy, etc.).*
