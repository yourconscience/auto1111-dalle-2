import modules.scripts as scripts
import gradio as gr
import logging
import openai
import os
from PIL import Image
import requests
import shutil

from modules import images
from modules.processing import process_images, Processed
from modules.processing import Processed
from modules.shared import opts, cmd_opts, state


def create_dalle(prompt: str, n: int = 1, size: str = '1024x1024'):
    assert os.environ['OPENAI_API_KEY'] is not None,\
        'Set OPENAI_API_KEY environment variable first: https://beta.openai.com/account/api-keys'
    response = openai.Image.create(prompt=prompt, n=n, size=size)
    return response


def get_urls(dalle_response: dict) -> list[str]:
    return [resp['url'] for resp in dalle_response['data']]


def save_image_from_url(url: str, filename: str):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        logging.info(f'Image saved to {filename}')


def save_dalle_images(dalle_response: dict, file_prefix: str):
    urls = get_urls(dalle_response)
    for i, url in enumerate(urls):
        save_image_from_url(url, file_prefix + f'{i+1}.png')


class Script(scripts.Script):  
    def title(self):
        return 'DALLE-2 text-to-image generation via API'

    def show(self, is_img2img):
        return not is_img2img

    def ui(self, is_img2img):
        if not is_img2img:
            n_images = gr.Slider(minimum=1, maximum=16, step=1, label='Number of images to generate')
            return [n_images]
        return

    def run(self, p, n_images):
        prompt = p.prompt
        size = f'{p.width}x{p.height}'
        dalle_response = create_dalle(prompt, n_images, size)
        
        processed = process_images(p)
        
        urls = get_urls(dalle_response)
        for i, url in enumerate(urls):
            tmp_filename = os.path.join(p.outpath_samples, f'dalle_{i}.png')
            save_image_from_url(url, tmp_filename)
            image = Image.open(tmp_filename)
            processed.images.append(image)
            images.save_image(image, p.outpath_samples, basename="", seed=processed.seed, prompt=processed.prompt,
                              extension=opts.samples_format, info=processed.info, p=p)
        return processed