# removebg_infusiblecoder
[![PyPI](https://img.shields.io/pypi/v/removebg_infusiblecoder)](https://pypi.org/project/removebg-infusiblecoder/)
[![Downloads](https://pepy.tech/badge/removebg-infusiblecoder)](https://pypi.org/project/removebg-infusiblecoder/)
[![Downloads](https://pepy.tech/badge/removebg-infusiblecoder/month)](https://pypi.org/project/removebg-infusiblecoder/)
[![Downloads](https://pepy.tech/badge/removebg-infusiblecoder/week)](https://pypi.org/project/removebg-infusiblecoder/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://img.shields.io/badge/License-MIT-blue.svg)

removebg_infusiblecoder is a tool to remove images background.

<p style="display: flex;align-items: center;justify-content: center;">
  <img src="https://raw.githubusercontent.com/syedusama5556/removebg_infusiblecoder/master/examples/car-1.jpg" width="100" />
  <img src="https://raw.githubusercontent.com/syedusama5556/removebg_infusiblecoder/master/examples/car-1.out.png" width="100" />
</p>

<p style="display: flex;align-items: center;justify-content: center;">
  <img src="https://raw.githubusercontent.com/syedusama5556/removebg_infusiblecoder/master/examples/animal-1.jpg" width="100" />
  <img src="https://raw.githubusercontent.com/syedusama5556/removebg_infusiblecoder/master/examples/animal-1.out.png" width="100" />
</p>

<p style="display: flex;align-items: center;justify-content: center;">
  <img src="https://raw.githubusercontent.com/syedusama5556/removebg_infusiblecoder/master/examples/girl-1.jpg" width="100" />
  <img src="https://raw.githubusercontent.com/syedusama5556/removebg_infusiblecoder/master/examples/girl-1.out.png" width="100" />
</p>

**If this project has helped you, please consider making a [donation](https://www.buymeacoffee.com/syedusama56).**

## Requirements

```
python: >3.7, <3.11
```

## Installation

CPU support:

```bash
pip install removebg-infusiblecoder # for library
pip install removebg-infusiblecoder[cli] # for library + cli
```

GPU support:


```bash
pip install removebg-infusiblecoder[gpu] # for library
pip install removebg-infusiblecoder[gpu,cli] # for library + cli

```
## Usage as a cli

After the installation step you can use removebg_infusiblecoder just typing `removebg_infusiblecoder` in your terminal window.

The `removebg_infusiblecoder` command has 4 subcommands, one for each input type:
- `i` for files
- `p` for folders
- `s` for http server
- `b` for RGB24 pixel binary stream

You can get help about the main command using:

```
removebg_infusiblecoder --help
```

As well, about all the subcommands using:

```
removebg_infusiblecoder <COMMAND> --help
```

### removebg_infusiblecoder `i`

Used when input and output are files.

Remove the background from a remote image

```
curl -s http://input.png | removebg_infusiblecoder i > output.png
```

Remove the background from a local file

```
removebg_infusiblecoder i path/to/input.png path/to/output.png
```

Remove the background specifying a model

```
removebg_infusiblecoder -m u2netp i path/to/input.png path/to/output.png
```

Remove the background returning only the mask

```
removebg_infusiblecoder -om i path/to/input.png path/to/output.png
```


Remove the background applying an alpha matting

```
removebg_infusiblecoder i -a path/to/input.png path/to/output.png
```

Passing extras parameters

```
SAM example

removebg_infusiblecoder i -m sam -x '{ "sam_prompt": [{"type": "point", "data": [724, 740], "label": 1}] }' examples/plants-1.jpg examples/plants-1.out.png
```

```
Custom model example

removebg_infusiblecoder i -m u2net_custom -x '{"model_path": "~/.u2net/u2net.onnx"}' path/to/input.png path/to/output.png
```


### removebg_infusiblecoder `p`

Used when input and output are folders.

Remove the background from all images in a folder

```
removebg_infusiblecoder p path/to/input path/to/output
```

Same as before, but watching for new/changed files to process

```
removebg_infusiblecoder p -w path/to/input path/to/output
```

### removebg_infusiblecoder `s`

Used to start http server.

```
removebg_infusiblecoder s --host 0.0.0.0 --port 5000 --log_level info
```

To see the complete endpoints documentation, go to: `http://localhost:5000/api`.

Remove the background from an image url

```
curl -s "http://localhost:5000/api/remove?url=http://input.png" -o output.png
```

Remove the background from an uploaded image

```
curl -s -F file=@/path/to/input.jpg "http://localhost:5000/api/remove"  -o output.png
```

### removebg_infusiblecoder `b`

Process a sequence of RGB24 images from stdin. This is intended to be used with another program, such as FFMPEG, that outputs RGB24 pixel data to stdout, which is piped into the stdin of this program, although nothing prevents you from manually typing in images at stdin.

```
removebg_infusiblecoder b image_width image_height -o output_specifier
```

Arguments:

- image_width : width of input image(s)
- image_height : height of input image(s)
- output_specifier: printf-style specifier for output filenames, for example if `output-%03u.png`, then output files will be named `output-000.png`, `output-001.png`, `output-002.png`, etc. Output files will be saved in PNG format regardless of the extension specified. You can omit it to write results to stdout.

Example usage with FFMPEG:

```
ffmpeg -i input.mp4 -ss 10 -an -f rawvideo -pix_fmt rgb24 pipe:1 | removebg_infusiblecoder b 1280 720 -o folder/output-%03u.png
```

The width and height values must match the dimension of output images from FFMPEG. Note for FFMPEG, the "`-an -f rawvideo -pix_fmt rgb24 pipe:1`" part is required for the whole thing to work.


## Usage as a library

Input and output as bytes

```python
from removebg_infusiblecoder import remove

input_path = 'input.png'
output_path = 'output.png'

with open(input_path, 'rb') as i:
    with open(output_path, 'wb') as o:
        input = i.read()
        output = remove(input)
        o.write(output)
```

Input and output as a PIL image

```python
from removebg_infusiblecoder import remove
from PIL import Image

input_path = 'input.png'
output_path = 'output.png'

input = Image.open(input_path)
output = remove(input)
output.save(output_path)
```

Input and output as a numpy array

```python
from removebg_infusiblecoder import remove
import cv2

input_path = 'input.png'
output_path = 'output.png'

input = cv2.imread(input_path)
output = remove(input)
cv2.imwrite(output_path, output)
```

How to iterate over files in a performatic way

```python
from pathlib import Path
from removebg_infusiblecoder import remove, new_session

session = new_session()

for file in Path('path/to/folder').glob('*.png'):
    input_path = str(file)
    output_path = str(file.parent / (file.stem + ".out.png"))

    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input = i.read()
            output = remove(input, session=session)
            o.write(output)
```

## Usage as a docker

Just replace the `removebg_infusiblecoder` command for `docker run syedusama5556/removebg_infusiblecoder`.

Try this:

```
docker run syedusama5556/removebg_infusiblecoder i path/to/input.png path/to/output.png
```

## Models

All models are downloaded and saved in the user home folder in the `.u2net` directory.

The available models are:

-   modnet ([download](https://github.com/syedusama5556/removebg_infusiblecoder/releases/download/v0.0.0/modnet_photographic_portrait_matting.onnx), [source](https://github.com/xuebinqin/U-2-Net)): A pre-trained model for general use cases modnet.
-   isnet-general-use ([download](https://github.com/syedusama5556/removebg_infusiblecoder/releases/download/v0.0.0/isnet-general-use.onnx), [source](https://github.com/xuebinqin/U-2-Net)): A pre-trained model for general use cases isnet-general-use.
-   u2net ([download](https://github.com/syedusama5556/removebg_infusiblecoder/releases/download/v0.0.0/u2net.onnx), [source](https://github.com/xuebinqin/U-2-Net)): A pre-trained model for general use cases.
-   u2netp ([download](https://github.com/syedusama5556/removebg_infusiblecoder/releases/download/v0.0.0/u2netp.onnx), [source](https://github.com/xuebinqin/U-2-Net)): A lightweight version of u2net model.
-   u2net_human_seg ([download](https://github.com/syedusama5556/removebg_infusiblecoder/releases/download/v0.0.0/u2net_human_seg.onnx), [source](https://github.com/xuebinqin/U-2-Net)): A pre-trained model for human segmentation.
-   u2net_cloth_seg ([download](https://github.com/syedusama5556/removebg_infusiblecoder/releases/download/v0.0.0/u2net_cloth_seg.onnx), [source](https://github.com/levindabhi/cloth-segmentation)): A pre-trained model for Cloths Parsing from human portrait. Here clothes are parsed into 3 category: Upper body, Lower body and Full body.
-   silueta ([download](https://github.com/syedusama5556/removebg_infusiblecoder/releases/download/v0.0.0/silueta.onnx), [source](https://github.com/xuebinqin/U-2-Net/issues/295)): Same as u2net but the size is reduced to 43Mb.

-   isnet-general-use ([download](https://github.com/syedusama5556/removebg_infusiblecoder/releases/download/v0.0.0/isnet-general-use.onnx), [source](https://github.com/xuebinqin/DIS)): A new pre-trained model for general use cases.
-   isnet-anime ([download](https://github.com/syedusama5556/removebg_infusiblecoder/releases/download/v0.0.0/isnet-anime.onnx), [source](https://github.com/SkyTNT/anime-segmentation)): A high-accuracy segmentation for anime character.
-   sam ([download encoder](https://github.com/syedusama5556/removebg_infusiblecoder/releases/download/v0.0.0/vit_b-encoder-quant.onnx), [download decoder](https://github.com/syedusama5556/removebg_infusiblecoder/releases/download/v0.0.0/vit_b-decoder-quant.onnx), [source](https://github.com/facebookresearch/segment-anything)): A pre-trained model for any use cases.



### How to train your own model

If You need more fine tunned models try this:
https://github.com/syedusama5556/removebg_infusiblecoder/issues/193#issuecomment-1055534289


## Some video tutorials

- https://www.youtube.com/watch?v=3xqwpXjxyMQ
- https://www.youtube.com/watch?v=dFKRGXdkGJU
- https://www.youtube.com/watch?v=Ai-BS_T7yjE
- https://www.youtube.com/watch?v=dFKRGXdkGJU
- https://www.youtube.com/watch?v=D7W-C0urVcQ

## References

- https://arxiv.org/pdf/2005.09007.pdf
- https://github.com/NathanUA/U-2-Net
- https://github.com/pymatting/pymatting

## Buy me a coffee

Liked some of my work? Buy me a coffee (or more likely a beer)

<a href="https://www.buymeacoffee.com/syedusama56" target="_blank"><img src="https://bmc-cdn.nyc3.digitaloceanspaces.com/BMC-button-images/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;"></a>

## License

Copyright (c) 2024-present [Syed Usama Ahmad](https://github.com/syedusama5556)

Licensed under [MIT License](./LICENSE.txt)