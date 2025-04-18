﻿# Agri-in-Smart Imitation Control System
## System Architecture

### File Structure
```
ª   extensions.py
ª   main.py
ª   models.py
ª   README.md
ª   requirements.txt
ª   __init__.py
ª   
+---blueprints
ª   +---auth
ª   ª   ª   auth.py
ª   ª   ª   forms.py
ª   ª   ª   routes.py
ª   ª   ª   __init__.py
ª   ª   ª   
ª   ª   +---static
ª   ª   ª       forms.css
ª   ª   ª       
ª   ª   +---templates
ª   ª   ª   +---auth
ª   ª   ª           login.html
ª   ª   ª           register.html
ª   ª   ª           reset_password.html
ª   ª   ª           
ª   +---dashboard
ª   ª   ª   dash.py
ª   ª   ª   __init__.py
ª   ª   ª   
ª   ª   +---templates
ª   ª   ª   +---dashboard
ª   ª   ª           dash.html
ª   ª   ª                    
ª   +---shop
ª       ª   routes.py
ª       ª   shop.py
ª       ª   __init__.py
ª       ª   
ª       +---templates
+---static
ª       style.css
ª       
+---templates
ª       base.html
ª       index.html    
```
![image](https://github.com/user-attachments/assets/6c6ea2e2-3b58-4d22-bf8b-633f596b45c6)

## Technology Stack

- Flask
- MongoDb

### Mail Functionality
 - Flask Mail
 - Gmail smtp Engine

### UI
- Bootstrap


## Running the App

 1. git clone ```github.com/WayneCarlW/ic-app.git```
 2. cd to the directory
 3. ```pip install -r requirements.txt```
 4. ```python main.py```
 5. Begin your journey!
