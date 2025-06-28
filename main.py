import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from helper import helper
import logging

app = FastAPI()

@app.post("/get_answer")
async def get_answer(request: Request):
    body = await request.json()
    query = body.get('query')
    print("Sending to generate the answer")
    answers = helper.generate(query)
    # for answer in answers:
    #     answer.pretty_print()
    print(answers)
    print("Sending response")
    return JSONResponse(content={'answer': answers[-1].content}, status_code=200)

if __name__=="__main__":
    uvicorn.run(app, host="localhost", port=2911)