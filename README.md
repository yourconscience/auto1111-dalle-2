# auto1111-dalle-2
Generating DALLE-2 images via openai API in stable-diffusion-webui.

## Setup
1. Copy OPENAI_API_KEY from https://beta.openai.com/account/api-keys to .env
2. Activate .env: `source .env`
3. Put `dalle.py` into `stable-diffusion-webui/scripts`

## Usage 
Only for text-to-image tab.
Set number of images to generate via openai API. 
Each image will be saved to same folder as stable diffusion output images.
It will be shown in same window as SD outputs, after last SD image (but not in images thumbnail).