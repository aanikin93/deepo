# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source, version
from .python import Python


@dependency(Python)
@source('pip')
@version('latest')
class Pytorch(Module):
    def __init__(self, manager, **args):
        super(self.__class__, self).__init__(manager, **args)
        
    def build(self):
        if self.version == 'latest':
            return self.build_latest
        else:
            return r'''
                $PIP_INSTALL \
                    future \
                    numpy \
                    protobuf \
                    enum34 \
                    pyyaml \
                    typing \
                    torchvision \
                    torch==%s \
                    && \
            ''' % (self.version)
            
    def build_latest(self):
        cuver = 'cpu' if self.composer.cuda_ver is None else 'cu%d' % (
            float(self.composer.cuda_ver) * 10)
        
        
        return r'''
            $PIP_INSTALL \
                future \
                numpy \
                protobuf \
                enum34 \
                pyyaml \
                typing \
            	torchvision_nightly \
                && \
            $PIP_INSTALL \
                torch_nightly -f \
                https://download.pytorch.org/whl/nightly/%s/torch_nightly.html \
                && \
        ''' % cuver
