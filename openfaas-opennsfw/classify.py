#!/usr/bin/env python
import sys
import os
import json
import urllib2
import caffe
import contextlib
import numpy as np
import classify_nsfw



def make_transformer(nsfw_net):
    # Note that the parameters are hard-coded for best results
    transformer = caffe.io.Transformer({'data': nsfw_net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2, 0, 1))  # move image channels to outermost
    transformer.set_mean('data', np.array([104, 117, 123]))  # subtract the dataset-mean value in each channel
    transformer.set_raw_scale('data', 255)  # rescale from [0, 1] to [0, 255]
    transformer.set_channel_swap('data', (2, 1, 0))  # swap channels from RGB to BGR

    return transformer


nsfw_net = caffe.Net(
    "/opt/open_nsfw/nsfw_model/deploy.prototxt",
    "/opt/open_nsfw/nsfw_model/resnet_50_1by2_nsfw.caffemodel",
    caffe.TEST
)
caffe_transformer = make_transformer(nsfw_net)


def classify_from_url(image_entry, nsfw_net):
    headers = {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'}
    result = {}
    try:
        req = urllib2.Request(image_entry, None, headers)
        with contextlib.closing(urllib2.urlopen(req)) as stream:
            score = classify(stream.read(), nsfw_net)
            result = {'sfw_score': score[0], 'nsfw_score': score[1]}

    except urllib2.HTTPError as e:
        result = {'error_reason': e.reason}

    except urllib2.URLError as e:
        result = {'error_reason': str(e.reason)}

    except Exception as e:
        result = {'error_reason': str(e)}

    print(result)


def classify(image_data, nsfw_net):

    # disable stdout
    null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
    save = os.dup(1), os.dup(2)
    os.dup2(null_fds[0], 1)
    os.dup2(null_fds[1], 2)

    scores = classify_nsfw.caffe_preprocess_and_compute(
        image_data,
        caffe_transformer=caffe_transformer,
        caffe_net=nsfw_net,
        output_layers=['prob']
    )

    # enable stdout
    os.dup2(save[0], 1)
    os.dup2(save[1], 2)
    os.close(null_fds[0])
    os.close(null_fds[1])

    return scores


def main(argv):
    url = sys.argv[1]
    classify_from_url(url, nsfw_net)


if __name__ == "__main__":
    main(sys.argv)
