# How to run dump1090
Run the following to install dump1090:
```
chmod +x install_dump1090_fa.sh
./install_dump1090_fa.sh
./dump1090/dump1090 --net --fix --fix --modeac --gain 49.6
```

In a second Terminal run:
```
python3 beast_reader.py
```
