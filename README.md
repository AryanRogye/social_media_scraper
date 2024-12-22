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
deactivate
```

### For frontend
```bash
cd frontend
npm install
cd src-tauri
python3 -m venv venv
source venv/bin/activate # Whatever Your OS is
pip install -r requirements.txt
deactivate
```

### Go Back
```bash
cd ..
cd ..
./runp # Parser enter -u with username in "" for first time after itll look at your logs for repeats
./rung # Gui
```
