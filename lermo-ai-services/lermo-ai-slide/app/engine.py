from llama_index.llms import LlamaCPP
from llama_index.llms.llama_utils import messages_to_prompt, completion_to_prompt

from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS

from app.api import config

MODEL_LLAMA = None
FAISS_INSTANCE = None

def init_model():
  global MODEL_LLAMA
  if not MODEL_LLAMA:
    print("Initializing model...")
    MODEL_LLAMA = LlamaCPP(
        model_path=config.MODEL_PATH,
        temperature=0.2,
        max_new_tokens=3072,
        # llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
        context_window=3072,
        # kwargs to pass to __call__()
        generate_kwargs={},
        # set to at least 1 to use GPU
        # model_kwargs={"n_gpu_layers": 1},
        # transform inputs into Llama2 format
        messages_to_prompt=messages_to_prompt,
        completion_to_prompt=completion_to_prompt,
        verbose=True,
    )
    print("Model initialized")


def init_faiss():
  global FAISS_INSTANCE
  if not FAISS_INSTANCE:
      hf_embedding = HuggingFaceInstructEmbeddings()
      FAISS_INSTANCE = FAISS.load_local(config.DB_PATH, embeddings=hf_embedding)