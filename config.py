""" Server.py Config """
# Endpoints to Create, Default Modality, Specified Handler
ENDPOINTS = [
    {"name": "textual", "modality": "textual"},
    {"name": "audio", "modality": "audio"},
    {"name": "visual", "modality": "visual"},
    {"name": "physical", "modality": "physical"},
    {"name": "custom", "modality": "textual", "handler": "custom"}
]

# Modalities to Trigger GET requests to
GET_MODALITIES = [
    "audio",
    "physical"
]

NCHANNELS = 8 # Number of channels (i.e. Monoaudio)
SAMPWIDTH = 2 # Number of bytes per sample
FRAMERATE = 48000 # Rate of play
VISUAL_INTERVAL = 3 # Rate (seconds) of Visual Data instances
PHYSICAL_INTERVAL = 3 # Rate (seconds) of Physical Data instances

""" Processors.py Config """
MAX_VISUAL_HISTORY = 10 # Max Visual Data instances
MAX_PHYSICAL_HISTORY = 10 # Max Physical Data instances