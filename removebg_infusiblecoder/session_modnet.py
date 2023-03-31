from typing import List

import numpy as np
import cv2
from PIL import Image
from PIL.Image import Image as PILImage

from .session_base import BaseSession
import onnxruntime

def get_scale_factor(im_h, im_w, ref_size):

    if max(im_h, im_w) < ref_size or min(im_h, im_w) > ref_size:
        if im_w >= im_h:
            im_rh = ref_size
            im_rw = int(im_w / im_h * ref_size)
        elif im_w < im_h:
            im_rw = ref_size
            im_rh = int(im_h / im_w * ref_size)
    else:
        im_rh = im_h
        im_rw = im_w

    im_rw = im_rw - im_rw % 32
    im_rh = im_rh - im_rh % 32

    x_scale_factor = im_rw / im_w
    y_scale_factor = im_rh / im_h

    return x_scale_factor, y_scale_factor


class ModNetSession(BaseSession):

    def predict(self, img: PILImage) -> List[PILImage]:

        ##############################################
        #  Main Inference part
        ##############################################
        ref_size = 512
        # read image
        # im = cv2.imread(args.image_path)
        im = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

        # unify image channels to 3
        if len(im.shape) == 2:
            im = im[:, :, None]
        if im.shape[2] == 1:
            im = np.repeat(im, 3, axis=2)
        elif im.shape[2] == 4:
            im = im[:, :, 0:3]

        # normalize values to scale it between -1 to 1
        im = (im - 127.5) / 127.5   

        im_h, im_w, im_c = im.shape
        x, y = get_scale_factor(im_h, im_w, ref_size) 

        # resize image
        im = cv2.resize(im, None, fx = x, fy = y, interpolation = cv2.INTER_AREA)

        # prepare input shape
        im = np.transpose(im)
        im = np.swapaxes(im, 1, 2)
        im = np.expand_dims(im, axis = 0).astype('float32')

        # Initialize session and get prediction
        session = self.inner_session
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name
        ort_outs = session.run([output_name], {input_name: im})


        pred = ort_outs[0][:, 0, :, :]

        ma = np.max(pred)
        mi = np.min(pred)

        pred = (pred - mi) / (ma - mi)
        pred = np.squeeze(pred)

        mask = Image.fromarray((pred * 255).astype("uint8"), mode="L")
        mask = mask.resize(img.size, Image.LANCZOS)

        return [mask]
    
