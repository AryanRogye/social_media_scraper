# Steps to get things working

## Platform Specific Commands
### Linux/Mac:
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
### Windows (CMD):
```bash
venv\Scripts\activate`
```

### Windows (PowerShell):
```bash
.\venv\Scripts\Activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```
```bash
cd frontend
npm install
deactivate
cd src-tauri
python3 -m venv venv
source venv/bin/activate # Whatever Your OS is

pip install -r requirements.txt
deactivate
cd ..
cd ..
./runp # Parser
./rung # Gui
```
