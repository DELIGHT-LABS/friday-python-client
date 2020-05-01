.PHONY: setup test

setup: go.sum
	bash ./scripts/install_friday.sh
	cd friday && make install
