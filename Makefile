.PHONY = all clean

# mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
# current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
# OUTPUT_PATH = $(CURDIR)/models/reduced//RandomForestClassifier/

all:
	./make.sh

clean:
	@rm predict_platform
