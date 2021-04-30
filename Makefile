TOP_DIR = ../..
include $(TOP_DIR)/tools/Makefile.common

THIS_APP = $(shell basename $(shell pwd))

BUILD_VENV = $(shell pwd)/venv
TARGET_VENV = $(TARGET)/venv/$(THIS_APP)

TARGET ?= /kb/deployment
DEPLOY_RUNTIME ?= /kb/runtime

SRC_PYTHON = $(wildcard scripts/*.py)

# SRC_SERVICE_PYTHON = $(wildcard service-scripts/*.py)
# BIN_SERVICE_PYTHON = $(addprefix $(BIN_DIR)/,$(basename $(notdir $(SRC_SERVICE_PYTHON))))
# DEPLOY_SERVICE_PYTHON = $(addprefix $(SERVICE_DIR)/bin/,$(basename $(notdir $(SRC_SERVICE_PYTHON))))

all: bin

bin: $(BIN_PYTHON) # $(BIN_SERVICE_PYTHON)
# TARGET points to module directory. KB_TOP env variable in python. knows where the module is.
# neighbor directory in Python can be looked in.
# No implicit location of data files.
# Put location of model files in bash script that the make file creates. Explicit location is required.
.PHONY: venv
venv: venv/bin/platform

# venv/bin/platform:
# 	rm -rf platform venv
# 	python3 -m venv $(BUILD_VENV)
# 	cd platform; . $(BUILD_VENV)/bin/activate; python3 setup.py install
# 	mkdir $(BUILD_VENV)/app-bin
# 	ln -s ../bin/tpp ../bin/transit $(BUILD_VENV)/app-bin

deploy: deploy-client deploy-service
deploy-all: deploy-client deploy-service
deploy-client: deploy-scripts

deploy-service: deploy-libs deploy-scripts # deploy-venv

# deploy-venv:
# 	rm -rf transit-deploy $(TARGET_VENV)
# 	git clone $(TRANSIT_SRC) transit-deploy
# 	python3 -m venv $(TARGET_VENV)
# 	cd transit-deploy; . $(TARGET_VENV)/bin/activate; python3 setup.py install
# 	mkdir $(TARGET_VENV)/app-bin
# 	ln -s ../bin/tpp ../bin/transit $(TARGET_VENV)/app-bin

# deploy-service-scripts:
# 	export KB_TOP=$(TARGET); \
# 	export KB_RUNTIME=$(DEPLOY_RUNTIME); \
# 	export KB_PYTHON_PATH=$(TARGET)/lib ; \
# 	export PATH_ADDITIONS=$(TARGET_VENV)/app-bin; \
# 	for src in $(SRC_SERVICE_PYTHON) ; do \
# 	        basefile=`basename $$src`; \
# 	        base=`basename $$src .py`; \
# 	        echo install $$src $$base ; \
# 	        cp $$src $(TARGET)/pybin ; \
# 	        $(WRAP_PYTHON3_SCRIPT) "$(TARGET)/pybin/$$basefile" $(TARGET)/bin/$$base ; \
# 	done; \

# $(BIN_DIR)/%: service-scripts/%.sh $(TOP_DIR)/user-env.sh
# 	export PATH_ADDITIONS=$(BUILD_VENV)/app-bin; \
# 	$(WRAP_SH_SCRIPT) '$$KB_TOP/modules/$(CURRENT_DIR)/$<' $@

# $(BIN_DIR)/%: service-scripts/%.py $(TOP_DIR)/user-env.sh
# 	export PATH_ADDITIONS=$(BUILD_VENV)/app-bin; \
# 	$(WRAP_PYTHON3_SCRIPT) '$$KB_TOP/modules/$(CURRENT_DIR)/$<' $@

include $(TOP_DIR)/tools/Makefile.common.rules
