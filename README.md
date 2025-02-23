## Setting up a virtual environment (venv) in Python

1. Install the virtual environment package: This is usually pre-installed with Python 3. If not, you can install it with pip:
    $pip install virtualenv

2. Create a virtual environment: Navigate to your project directory and run the following command to create a new virtual environment. Replace myenv with the name you want to give to your virtual environment.
    $python -m venv myenv
    
3. Activate the virtual environment: The command to activate the virtual environment depends on your operating system:
    On Windows:
    .\myenv\Scripts\activate

    On Unix or MacOS:
    source myenv/bin/activate

4. Install packages: Now that your virtual environment is activated, you can install packages for your project with pip. These packages will be installed in the virtual environment, not globally.
    $pip install package-name

5. Deactivate the virtual environment: When you're done working in the virtual environment, you can deactivate it with the following command:
    $deactivate


### Backend
- cd backend
- pip install sqlalchemy
- pip install fastapi uvicorn mysql-connector-python
- pip install pymysql
- pip install bcrypt
- python -m uvicorn main:app --reload  