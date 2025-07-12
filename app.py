from sanic import Sanic, html

from faker import Faker

import asyncio


app = Sanic(__name__)

fake = Faker()

@app.get("/")
@app.ext.template("index.html")
async def index(request):
    return {}

@app.get("/update")
async def update(request):
    await asyncio.sleep(1)
    return html(f'''<span id="replace_me">{fake.name()}</span>''')
