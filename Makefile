NO_COLOR    = \x1b[0m
COMPILE_COLOR    = \x1b[32;01m
LINK_COLOR    = \x1b[31;01m

	

all: build
	@echo -e '$(LINK_COLOR)* Copying SVGS [$@]$(NO_COLOR)'
	cp svg/*.png install-files/usr/share/banners/lliurex-neu/

build:
	@echo -e '$(LINK_COLOR)* Rendering SVGS [$@]$(NO_COLOR)'
	@$(MAKE) -C svg/ -j2

clean:
	@echo -e '$(LINK_COLOR)* Cleaning [$@]$(NO_COLOR)'
	@$(MAKE) -C svg/ $@
	
.PHONY: all clean	