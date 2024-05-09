# put back later
# python3 -m pip install -r requirements.txt

# OSTYPE=$(if [[ $OSTYPE == "linux-gnu"* ]]; then echo "linux"; else echo "macos"; fi)

# python3 install.py --os $OSTYPE
python3 install.py --os linux --remote localhost --user testuser --password pass --port 2222