BINARY_NAME=AutoDownloader
APP_ID=com.rgdev.autodownloader
GOBIN=$(HOME)/go/bin
RELEASE_DIR=Releases

.PHONY: all clean install-deps build-mac build-windows build-linux

all: build-mac build-windows build-linux

install-deps:
	go install fyne.io/fyne/v2/cmd/fyne@latest
	go install github.com/fyne-io/fyne-cross@latest

build-mac:
	@echo "Building for macOS..."
	mkdir -p $(RELEASE_DIR)/mac
	$(GOBIN)/fyne package -os darwin -name "$(BINARY_NAME)" -appID $(APP_ID) -icon Icon.png
	mv "$(BINARY_NAME).app" $(RELEASE_DIR)/mac/
	# Also creating a zip for distribution
	cd $(RELEASE_DIR)/mac && zip -r $(BINARY_NAME)-mac.zip "$(BINARY_NAME).app"

build-windows:
	@echo "Building for Windows (requires Docker)..."
	mkdir -p $(RELEASE_DIR)/windows
	$(GOBIN)/fyne-cross windows -arch=amd64 -app-id $(APP_ID) -icon Icon.png
	cp -r fyne-cross/dist/windows-amd64/* $(RELEASE_DIR)/windows/

build-linux:
	@echo "Building for Linux (requires Docker)..."
	mkdir -p $(RELEASE_DIR)/linux
	$(GOBIN)/fyne-cross linux -arch=amd64 -app-id $(APP_ID) -icon Icon.png
	cp -r fyne-cross/dist/linux-amd64/* $(RELEASE_DIR)/linux/

clean:
	rm -f $(BINARY_NAME)
	rm -rf fyne-cross
	rm -rf $(RELEASE_DIR)
	rm -f *.app
