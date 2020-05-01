.PHONY: setup test

setup:
	bash ./scripts/install_friday.sh
	cd friday && make install
