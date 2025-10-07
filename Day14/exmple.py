from diffusers import StableDiffusionPipeline
import torch

# Load the Stable Diffusion model
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)

# Use GPU if available
pipe = pipe.to("cuda")

# Text prompt
prompt = "a futuristic city floating in the sky, ultra realistic, sunset lighting"

# Generate image
image = pipe(prompt).images[0]

# Save the image
image.save("generated_image.png")

print("✅ Image saved as generated_image.png")
