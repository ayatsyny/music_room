# Configure PyCharm Pro on linux

1. Create virtualenv with use python3 for example "musicroom".

2. Open project in PyCharm.

3. Open terminal, activate virtualenv and install python packages for project:

        # pip install -r deploy/requirements.txt  

4. Open File -> Settings -> Project -> Project Interpreter and set virtualenv in select box (use show all if
it doesn't exist in list).

5. Open File -> Settings -> Project -> Project Structure and set paths:

    **Source Folders:** src
    
    **Template Folders:** src/templates

6. Open File -> Settings -> Languages & Frameworks -> Django:

    **Enable Django Support:** On
    
    **Django project root:** /path/to/project/musicroom/src
    
    **Settings:** musicroom/settings.py
    
    **Manage script:** manage.py
    
    **Environment variables:** DJANGO_SETTINGS_MODULE=musicroom.settings
    
7. Open File -> Settings -> Build, Execution, Deployment -> Console -> Django console and set configs:

    **Environment variables:** DJANGO_SETTINGS_MODULE=musicroom.settings
    
    **Python Interpreter:** project's virtualenv
    
    **Working directory:** /path/to/project/musicroom/src
    
    **Add content roots to PYTHONPATH:** On
    
    **Add source roots to PYTHONPATH:** On
    
8. Open Run -> Edit configurations...; click "+" -> Django server and set configs:

    **Name:** musicroom
    
    **Host:** 0.0.0.0
    
    **Port:** 8000
    
    **Environment variables:** add DJANGO_SETTINGS_MODULE=musicroom.settings
    
    **Python Interpreter:** project's virtualenv
    
    **Working directory:** /path/to/project/musicroom/src
    
    **Add content roots to PYTHONPATH:** On
    
    **Add source roots to PYTHONPATH:** On
