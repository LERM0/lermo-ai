import uvicorn
from contextlib import asynccontextmanager
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
from fastapi import APIRouter, HTTPException, Path, Request
from langchain import PromptTemplate, LLMChain
from app import engine, db

from app.api import config
import json

from llama_index.llms import LlamaCPP
from llama_index.llms.llama_utils import messages_to_prompt, completion_to_prompt

router = APIRouter()

@router.get("/test")
async def test():
    return db.get_all()

@router.get("/flush")
async def flush():
    db.flushdb_all()
    print(db.get_all())
    return "ok"

@router.post("/slide")
async def slide(request: Request) -> StreamingResponse:
  params = await request.json()
  prompt = params.get("prompt")
  # Split prompt to array
  # [Create, voice1, male, hello world]
  # Array 0: Create, Update
  # Array 1: File Path
  # Array 2: Voice Category
  # Array 3: TTS

  prompt_array = prompt.split(", ")[:4] 
  action = prompt_array[0]
  slide_name = prompt_array[1]
  keyword = prompt_array[2]
  task = prompt_array.slice(", ", 3)

  FAISS_INSTANCE = engine.FAISS_INSTANCE
  search = FAISS_INSTANCE.similarity_search(keyword, k=2)
  template = '''
  Context: {context}

  task: Create, RevealJS Slide Section, {task}
  Output code snippet only, don't need an explaination, don't need an other infomation, do not use general knowledge to answer.
  '''

  prompt = PromptTemplate(input_variables=["task", "context"], template=template)
  final_prompt = prompt.format(task=task, context=search)
  print(final_prompt)

  result = run_llm(final_prompt)

  slideJson = {
    slide_name: result
  }

  db.set(slide_name, json.dumps(slideJson))
  print(db.get(slide_name))

  return { "html": result}
  # return StreamingResponse(run_llm(final_prompt), media_type="text/event-stream")


@router.post("/public")
async def slide(request: Request) -> StreamingResponse:
  slide_context = db.get_all()
  context1 = f'''
    { slide_context }
  '''

  task = '''
  1 List slides from context1
  2 Sort from context1 based on slide name and number
  3 Put slide into 'Put Code Here' and create full html based on context2
  '''

  context2 = '''
  <!doctype html>
  <html lang="en">

  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

    <title> { Title } </title>

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.1.2/dist/reset.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.1.2/dist/reveal.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.1.2/dist/theme/white.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.1.2/plugin/highlight/monokai.css">

  </head>

  <body>
    <div class="reveal">
      <div class="slides">
        Put Code Here
      </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.1.2/dist/reveal.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.1.2/plugin/notes/notes.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.1.2/plugin/markdown/markdown.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.1.2/plugin/highlight/highlight.js"></script>
    <script>
      Reveal.initialize({
        autoSlide: 5000,
        hash: true,
        controls: false,
        plugins: [RevealMarkdown, RevealHighlight, RevealNotes]
      });
    </script>
  </body>
  </html>
  '''


  template = '''
  Context1: {context1}
  Context2: {context2}

  task: {task}
  '''

  prompt = PromptTemplate(input_variables=["task", "context1", "context2"], template=template)
  final_prompt = prompt.format(task=task, context1=context1, context2=context2)
  print(final_prompt)
  result = run_llm(final_prompt)
  print(result)
  return { "html": result}
  # return StreamingResponse(run_llm(final_prompt), media_type="text/event-stream")
# def run_llm(question: str) -> AsyncGenerator:
#     llm : LlamaCPP = engine.MODEL_LLAMA
#     response_iter = llm.stream_complete(question)
#     for response in response_iter:
#         yield f"{response.delta}"


def run_llm(question: str) -> str:
    llm : LlamaCPP = engine.MODEL_LLAMA
    response_iter = llm.complete(question)
    return response_iter.text


def run_llm_stream(question: str) -> str:
    llm : LlamaCPP = engine.MODEL_LLAMA
    response_iter = llm.stream_complete(question)
    return response_iter.text

# def run_llm(question: str) -> str:
#     llm: LlamaCPP = engine.MODEL_LLAMA
#     responses = llm.complete(question)
    # response_dicts = [dataclasses.asdict(response) for response in responses]
    # full_text = ''.join(response_dict['text'] for response_dict in response_dicts)
    # return full_text