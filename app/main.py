# This is a sample Python script.
import uvicorn
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


from fastapi import FastAPI

from app.src.models import AnswerRequest

app = FastAPI()

@app.post("/answer")
async def read_root(request: AnswerRequest):
    return {"answer": f'Ответ на {request.question}'}


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
