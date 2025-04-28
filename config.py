from dotenv import load_dotenv
import os

load_dotenv()

""" Server.py Config """
SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))

# Endpoints to Create, Default Modality, Specified Handler
ENDPOINTS = [
    {"name": "textual", "modality": "textual"},
    {"name": "audio", "modality": "audio"},
    #{"name": "visual", "modality": "visual"},
    {"name": "physical", "modality": "physical"},
    {"name": "custom", "modality": "textual", "handler": "custom"}
]

# Modalities to Trigger GET requests to
GET_MODALITIES = [
    "audio",
    "physical"
]

NCHANNELS = 2 # Number of channels (i.e. Monoaudio)
SAMPWIDTH = 2 # Number of bytes per sample
FRAMERATE = 48000 # Rate of play
VISUAL_INTERVAL = 3 # Rate (seconds) of Visual Data instances
PHYSICAL_INTERVAL = 3 # Rate (seconds) of Physical Data instances

""" Processors.py Config """
MAX_VISUAL_HISTORY = 10 # Max Visual Data instances
MAX_PHYSICAL_HISTORY = 10 # Max Physical Data instances

""" Text-to-Speech Config"""
PLAYHT_USER_ID = os.getenv("PLAYHT_USER_ID").strip()
PLAYHT_API_KEY = os.getenv("PLAYHT_API_KEY").strip()

""" Speech-to-Text Config """
SPEECHFLOW_API_KEY = os.getenv("SPEECHFLOW_API_KEY").strip()
SPEECHFLOW_SECRET_KEY = os.getenv("SPEECHFLOW_SECRET_KEY").strip()

""" DB Config """
MONGO_URI = os.getenv("MONGO_URI").strip()