KBUILD_OPTIONS+=KBUILD_EXTMOD_DTS=.

all: dtbs

clean:
	$(MAKE) -C $(KERNEL_SRC) M=$(M) clean

dtbs:
	python3 display/dtsi_check.py display && $(MAKE) -C $(KERNEL_SRC) M=$(M) dtbs $(KBUILD_OPTIONS)

%:
	$(MAKE) -C $(KERNEL_SRC) M=$(M) $@ $(KBUILD_OPTIONS)
