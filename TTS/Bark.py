from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
#from IPython.display import Audio
import torch

# Save the original torch.load function
_original_torch_load = torch.load

# Define a new function that forces weights_only=False
def custom_torch_load(*args, **kwargs):
    if "weights_only" not in kwargs:
        kwargs["weights_only"] = False
    return _original_torch_load(*args, **kwargs)

# Override torch.load globally
torch.load = custom_torch_load

# download and load all models
preload_models()

# generate audio from text
text_prompt = """
     Hello, my name is Saul. I am here to provide you with accurate responses to your questions.
    I also have other interests such as the art behind me, so please ask me anything.
"""
audio_array = generate_audio(text_prompt)

# save audio to disk
write_wav("bark_generation.wav", SAMPLE_RATE, audio_array)
  
# play text in notebook
#Audio(audio_array, rate=SAMPLE_RATE)