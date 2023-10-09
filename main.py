from fastapi import FastAPI


app = FastAPI(docs_url='/')


@app.get('/hello')
async def hello_test():
    return {'message': 'Hello'}




