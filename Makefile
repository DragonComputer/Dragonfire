install:
	./install.sh

install-no-model:
	./install.sh --no-model

pip-install:
	pip3 install .

pip-uninstall:
	python3 setup.py --uninstall


dev-install:
	./install.sh --dev --pip

dev-install-no-model:
	./install.sh --dev --pip --no-model

dev-pip-install:
	pip3 install -e .

dev-pip-uninstall:
	python3 setup.py develop --uninstall


docker-pull:
	docker pull dragoncomputer/dragonfire

docker-run:
	docker run dragonfire


build-ext-inplace:
	python3 setup.py build_ext --inplace

clean:
	rm -rf *.out *.bin *.exe *.o *.a *.so build *.egg-info *.db .pytest_cache
