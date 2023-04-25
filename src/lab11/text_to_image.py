from diffusers import StableDiffusionPipeline
import torch

def create_image(prompt, image_path):

    # Identifies the model 
    model = "runwayml/stable-diffusion-v1-5"

    # Gets the model
    pipe = StableDiffusionPipeline.from_pretrained(model, torch_dtype=torch.float32)

    # Generates the image
    image = pipe(prompt).images[0]  
    
    # Saves the image
    image.save(image_path)