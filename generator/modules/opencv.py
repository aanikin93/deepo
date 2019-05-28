# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source, version
from .tools import Tools
from .boost import Boost
from .python import Python


@dependency(Tools, Python, Boost)
# @source('git')
@source('pip')
@version('latest')
class Opencv(Module):
    def __init__(self, manager, **args):
        super(self.__class__, self).__init__(manager, **args)
        
    def build(self):
        if self.version == 'latest':
            opencv_version = "opencv-python"
        else:
            opencv_version = "opencv-python==%s" % (self.version)
        print("OpenCV version: %s" % opencv_version)
        return r'''
            $PIP_INSTALL \
                %s \
                && \
        ''' % opencv_version
        
    def build_from_source(self):
        return r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                libatlas-base-dev \
                libgflags-dev \
                libgoogle-glog-dev \
                libhdf5-serial-dev \
                libleveldb-dev \
                liblmdb-dev \
                libprotobuf-dev \
                libsnappy-dev \
                protobuf-compiler \
                && \

            $GIT_CLONE --branch %s https://github.com/opencv/opencv ~/opencv && \
            mkdir -p ~/opencv/build && cd ~/opencv/build && \
            cmake -D CMAKE_BUILD_TYPE=RELEASE \
                  -D CMAKE_INSTALL_PREFIX=/usr/local \
                  -D WITH_IPP=OFF \
                  -D WITH_CUDA=OFF \
                  -D WITH_OPENCL=OFF \
                  -D BUILD_TESTS=OFF \
                  -D BUILD_PERF_TESTS=OFF \
                  .. && \
            make -j"$(nproc)" install && \
            ln -s /usr/local/include/opencv4/opencv2 /usr/local/include/opencv2 && \
        ''' % self.version
