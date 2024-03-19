import numpy as np
from PIL import Image
from cog import BasePredictor, Input, Path as CogPath

from typing import Optional, Tuple, Any, Union

from removebg_infusiblecoder import new_session, remove ,download_models ,remove_return_base64

# Import BaseSession as necessary

class Predictor(BasePredictor):
    def setup(self):
        """Load the model into memory to make predictions faster"""
        # self.sessions = {}  # Assuming sessions is a dict mapping model names to session objects
        # download_models()

    def predict(
        self,
        input: CogPath = Input(description="The input file to process."),
        model: str = Input(description="Model name.", default="u2net",choices=["u2net","isnet-anime","carvekit","isnet-general-use","silueta","u2net_cloth_seg","u2net_human_seg","u2netp"]),
        alpha_matting: bool = Input(description="Use alpha matting.", default=False),
        alpha_matting_foreground_threshold: int = Input(
            description="Trimap fg threshold.", default=240
        ),
        alpha_matting_background_threshold: int = Input(
            description="Trimap bg threshold.", default=10
        ),
        alpha_matting_erode_size: int = Input(description="Erode size.", default=10),
        only_mask: bool = Input(description="Output only the mask.", default=False),
        # base64_image: bool = Input(description="Output will be in base64", default=False),
        post_process_mask: bool = Input(description="Post process the mask.", default=False),
        bgcolor: str = Input(
            description="Background color (R,G,B,A) to replace the removed background with.", default="0,0,0,0"
        ),
    ) -> CogPath:
        """Run a single prediction on the model"""
        # Convert bgcolor string to tuple
        bgcolor_tuple = tuple(map(int, bgcolor.split(','))) if bgcolor else None

        # Load the image
        image = Image.open(input)
        image_data = np.array(image)

        print(model, bgcolor_tuple, alpha_matting, alpha_matting_foreground_threshold, alpha_matting_background_threshold, alpha_matting_erode_size, only_mask, post_process_mask)
        # Get or create the session

        # if base64_image:
        #     # Call the remove function
        #     result = remove_return_base64(
        #         data=image_data,
        #         alpha_matting=alpha_matting,
        #         alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
        #         alpha_matting_background_threshold=alpha_matting_background_threshold,
        #         alpha_matting_erode_size=alpha_matting_erode_size,
        #         session=new_session(model),
        #         only_mask=only_mask,
        #         post_process_mask=post_process_mask,
        #         bgcolor=bgcolor_tuple
        #     )

        #     return result
        # else:
            # Call the remove function
        result = remove(
            data=image_data,
            alpha_matting=alpha_matting,
            alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
            alpha_matting_background_threshold=alpha_matting_background_threshold,
            alpha_matting_erode_size=alpha_matting_erode_size,
            session=new_session(model),
            only_mask=only_mask,
            post_process_mask=post_process_mask,
            bgcolor=bgcolor_tuple
        )

        # Assuming the result is an np.ndarray, convert it back to an image
        result_image = Image.fromarray(result.astype('uint8'))

        # Write the result image to a temporary file and return the path
        output_path = CogPath("/tmp/output.png")  # Adjust as necessary
        result_image.save(output_path)

        return output_path
