if [ ! -d "/usr/local/n" ]; then
	echo "n module not found, so installing..."
	cd; git clone https://github.com/tj/n
	cd n; sudo make install
	cd n/bin; sudo ./n
fi

set -e

n 8.11.3

cd ~/hello-world

npm install