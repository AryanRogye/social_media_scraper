python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd frontend
npm install
cd src-tauri
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..
cd ..
