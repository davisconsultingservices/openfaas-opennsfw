# openfaas-opennsfw
An OpenFaaS function that is a fork of [EugenCepoi/nsfw_api](https://github.com/EugenCepoi/nsfw_api) and runs [Yahoo's Open NSFW model](https://github.com/yahoo/open_nsfw).

```bash

# deploy
faas-cli deploy -y stack.yml


# invoke
echo "https://github.com/servernull/openfaas-exif/raw/master/image.jpg &> /dev/null && cat output.json" | faas-cli invoke openfaas-opennsfw
