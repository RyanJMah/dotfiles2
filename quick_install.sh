python3 -m pip install -r requirements.txt

OSTYPE=$(if [[ $OSTYPE == "linux-gnu"* ]]; then echo "linux"; else echo "macos"; fi)

python3 install.py --os $OSTYPE
