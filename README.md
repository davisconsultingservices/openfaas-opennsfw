# OpenFaaS OpenNSFW
An [OpenFaaS](https://www.openfaas.com/) function that is a fork of [EugenCepoi/nsfw_api](https://github.com/EugenCepoi/nsfw_api) and runs [Yahoo's Open NSFW model](https://github.com/yahoo/open_nsfw).  It scores 'safe for work' and 'not safe for work' between 0 to 1 based on the nudity in the image.

```bash

# deploy
faas-cli deploy -y stack.yml


# invoke
echo https://github.com/davisconsultingservices/openfaas-opennsfw/raw/master/puppy.jpg | faas-cli invoke openfaas-opennsfw | jq

{
  "sfw_score": 0.9973425269126892,
  "nsfw_score": 0.0026575096417218447
}

echo https://github.com/davisconsultingservices/openfaas-opennsfw/raw/master/eve.jpg | faas-cli invoke openfaas-opennsfw | jq

{
  "sfw_score": 0.12137062847614288,
  "nsfw_score": 0.8786293268203735
}

```
