from http.client import HTTPException
from fastapi import FastAPI
import sys
sys.path.append("..")
from index.main import HtmlParser
from api.models import UserUrlSubmission, Term
from db import Database, CONNECTION_URL
app = FastAPI()


@app.post("/api/submit/url")
async def submit_url(submission: UserUrlSubmission):
    parser = await HtmlParser(submission.url).request()
    structure = parser.scrap_website()
    try:
        await structure.save()
    except:
        return HTTPException(status_code=404, detail="Something went wrong.")
    return structure

@app.post("/results")
async def search(term: Term):
    database = await Database(CONNECTION_URL).connect()
    data = await database.get_results(term.search_term)
    return data

