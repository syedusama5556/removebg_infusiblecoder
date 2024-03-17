import os
from typing import List

import numpy as np
import pooch
from PIL import Image
from PIL.Image import Image as PILImage

import torch
from carvekit.api.high import HiInterface


from carvekit.web.schemas.config import MLConfig
from carvekit.web.utils.init_utils import init_interface


from carvekit.api.interface import Interface
from carvekit.ml.wrap.fba_matting import FBAMatting
from carvekit.ml.wrap.tracer_b7 import TracerUniversalB7
from carvekit.pipelines.postprocessing import MattingMethod
from carvekit.pipelines.preprocessing import PreprocessingStub
from carvekit.trimap.generator import TrimapGenerator
from pathlib import Path



from .base import BaseSession

import tempfile


class CarveKitSession():
    """
    This class represents a session using the CarveKit API's HiInterface for processing images.
    """

    def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        self.inner_session = None
        DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

        model_path_is = str(self.__class__.download_models(*args, **kwargs))

        # Initialize HiInterface here
        # self.interface = HiInterface(
        #     object_type="object",  # Can be "object" or "hairs-like".
        #     batch_size_seg=5,
        #     batch_size_matting=1,
        #     device=DEVICE,
        #     seg_mask_size=640,  # Use 640 for Tracer B7 and 320 for U2Net
        #     matting_mask_size=2048,
        #     trimap_prob_threshold=231,
        #     trimap_dilation=30,
        #     trimap_erosion_iters=5,
        #     fp16=False,
        # )
        # Initialize the interface
        seg_net = TracerUniversalB7(device=DEVICE, batch_size=1, load_pretrained=True, model_path=Path(model_path_is))
        fba = FBAMatting(device=DEVICE, input_tensor_size=2048, batch_size=1)
        trimap = TrimapGenerator()
        preprocessing = PreprocessingStub()
        postprocessing = MattingMethod(matting_module=fba, trimap_generator=trimap, device=DEVICE)
        self.interface = Interface(pre_pipe=preprocessing, post_pipe=postprocessing, seg_pipe=seg_net)


    def predict(self, img: PILImage, *args, **kwargs) -> List[PILImage]:
        """
        Predicts the output images for the input PILImage using the HiInterface.

        Parameters:
            img (PILImage): The input PIL Image object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            List[PILImage]: The list containing the processed image without background.
        """
        # Save the PILImage to a temporary file
        with tempfile.NamedTemporaryFile(
            suffix=".png", mode="w+b", delete=False
        ) as tmp:
            img.save(tmp, format="PNG")
            tmp_path = tmp.name

        try:
            # Process the image through the interface
            images_without_background = self.interface([tmp_path])

            # Load the processed image(s) as PILImage
            # processed_images = [Image.open(image_path).convert('RGB') for image_path in images_without_background]

            # Cleanup the temporary file

            # cat_wo_bg =  images_without_background[0]
            # cat_wo_bg.save('2.png')

            # print(img)
            # print(cat_wo_bg)
            # Assuming the interface returns a list of images,
            images_without_bg = images_without_background[0].resize(
                img.size, Image.LANCZOS
            )

        finally:
            # Cleanup the temporary file
            os.unlink(tmp_path)

        return [images_without_bg]

        # mask = Image.open(images_without_background[0])
        # mask = mask.resize(img.size, Image.LANCZOS)

        # return [mask]

        # # return images_without_background

    @classmethod
    def download_models(cls, *args, **kwargs):
        """
        Downloads the U2net model file from a specific URL and saves it.

        Parameters:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The path to the downloaded model file.
        """
        fname = f"{cls.name(*args, **kwargs)}.pth"
        pooch.retrieve(
        "https://github.com/syedusama5556/removebg_infusiblecoder/releases/download/v0.0.0/carvekit.pth",
        None,
        fname=fname,
        path=cls.u2net_home(*args, **kwargs),
        progressbar=True,
        )


        return os.path.join(cls.u2net_home(*args, **kwargs), fname)


    def u2net_home(cls, *args, **kwargs):
        return os.path.expanduser(
            os.getenv(
                "U2NET_HOME", os.path.join(os.getenv("XDG_DATA_HOME", "~"), ".u2net")
            )
        )

    @classmethod
    def name(cls, *args, **kwargs):
        """
        Returns the name of the U2net session.

        Parameters:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The name of the session.
        """
        return "carvekit"
