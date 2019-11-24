install:
	sudo ./install.sh

install-no-model:
	sudo ./install.sh --no-model

pip-install:
	sudo pip3 install .

pip-uninstall:
	sudo python3 setup.py --uninstall


dev-install:
	sudo ./install-dev.sh

dev-install-no-model:
	sudo ./install-dev.sh --no-model

dev-pip-install:
	sudo pip3 install -e .

dev-pip-uninstall:
	sudo python3 setup.py develop --uninstall


docker-pull:
	docker pull dragoncomputer/dragonfire

docker-run:
	docker run dragonfire


build-ext-inplace:
	python3 setup.py build_ext --inplace

clean:
	sudo rm -rf *.out *.bin *.exe *.o *.a *.so build *.egg-info *.db .pytest_cache
