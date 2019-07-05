# MANGA-MINER
A terminal programme which searches for manga series and downloads your choice of chapters.

## Setting up
You should be having python3, virtualenv and pip3 to use this application.
If you are on ubuntu
```bash
sudo apt install python3 virtualenv python3-pip
```
Also you need a few pip packages
```bash
source venv/bin/activate
pip3 install -r requirements.txt
```

## Usage
go the home directory and enter
```bash
source venv/bin/activate
python3 app.py
```
or simply
```bash
./start.sh
```
Enter the required fields when prompted on the terminal. The mimanga tool accordingly decides the manga and downloads from [mangareader.net](https://www.mangareader.net)

You will now find your manga in the Downloads directory. Happy Manging! :D

## License
[MIT](https://choosealicense.com/licenses/mit/)