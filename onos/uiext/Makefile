mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
curr_dir := $(patsubst %/,%,$(dir $(mkfile_path)))

include util/docker/Makefile.vars

onos_url := http://localhost:8181/onos
onos_curl := curl --fail -sSL --user onos:rocks --noproxy localhost
app_name := org.foo.app

NGSDN_TUTORIAL_SUDO ?=

clean:
	-$(NGSDN_TUTORIAL_SUDO) rm -rf foo-app/target

_copy_out:
	$(info *** Copying p4c outputs to app resources...)
	@mkdir -p foo-app/src/main/resources
	cp -f util/mn-cmd foo-app/src/main/resources/
	cp -f mininet/send.py foo-app/src/main/resources/

_mvn_package:
	$(info *** Building ONOS app...)
	@mkdir -p app/target
	@docker run --rm -v ${curr_dir}/foo-app:/mvn-src -w /mvn-src ${MVN_IMG} mvn clean install

app-build: _mvn_package _copy_out
	$(info *** ONOS app .oar package created succesfully)
	@ls -1 foo-app/target/*.oar

app-install:
	$(info *** Installing and activating app in ONOS...)
	${onos_curl} -X POST -HContent-Type:application/octet-stream \
		'${onos_url}/v1/applications?activate=true' \
		--data-binary @foo-app/target/foo-app-1.0-SNAPSHOT.oar
	@echo

app-uninstall:
	$(info *** Uninstalling app from ONOS (if present)...)
	-${onos_curl} -X DELETE ${onos_url}/v1/applications/${app_name}
	@echo

app-reload: app-uninstall app-install

