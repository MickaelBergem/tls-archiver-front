all: build-image

build-image:
	docker build -t tlsarchiver/front .

upload-image: build-image
	docker push tlsarchiver/front
