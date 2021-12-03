pip install Pyinstaller
pip install pynput
pip install pyqt5
mkdir BUILD
mkdir VOCABULARY
pyinstaller --onefile --noconsol --distpath BUILD quiz.py
copy BUILD\quiz.exe POLIGLOT.exe
rmdir /Q /S BUILD
del quiz.spec