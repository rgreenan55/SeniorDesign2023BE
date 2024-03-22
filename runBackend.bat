cd backend
.\venv\Scripts\activate
pip3 install -r ../requirements.txt --target=".\venv\Lib\site-packages" --upgrade
cd src
python app.py