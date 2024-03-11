import os
from typing import List

import numpy as np
import pooch
from PIL import Image
from PIL.Image import Image as PILImage

import torch
from carvekit.api.high import HiInterface

from .base import BaseSession

import tempfile


class CarveKitSession(BaseSession):
    """
    This class represents a session using the CarveKit API's HiInterface for processing images.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize HiInterface here
        self.interface = HiInterface(
            object_type="object",  # Can be "object" or "hairs-like".
            batch_size_seg=5,
            batch_size_matting=1,
            device="cuda" if torch.cuda.is_available() else "cpu",
            seg_mask_size=640,  # Use 640 for Tracer B7 and 320 for U2Net
            matting_mask_size=2048,
            trimap_prob_threshold=231,
            trimap_dilation=30,
            trimap_erosion_iters=5,
            fp16=False,
        )

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
        fname = f"{cls.name(*args, **kwargs)}.onnx"
        pooch.retrieve(
            "https://github.com/syedusama5556/removebg_infusiblecoder/releases/download/v0.0.0/u2netp.onnx",
            (
                None
                if cls.checksum_disabled(*args, **kwargs)
                else "md5:60024c5c889badc19c04ad937298a77b"
            ),
            fname=fname,
            path=cls.u2net_home(*args, **kwargs),
            progressbar=True,
        )

        return os.path.join(cls.u2net_home(*args, **kwargs), fname)

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
