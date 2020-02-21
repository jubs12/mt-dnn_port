sudo apt update
sudo apt upgrade
sudo apt install unzip python3-pip python-pip git
pip3 install --upgrade pip
pip3 install -r requirements.txt
git clone -b v0.1 https://github.com/namisan/mt-dnn.git
cd mt-dnn/
sh download.sh
