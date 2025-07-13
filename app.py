from sanic import Sanic, html

from faker import Faker

import asyncio


app = Sanic(__name__)
app.static('/static/', './static/')
app.static('/', './templates/index.html', name="index")

fake = Faker()


@app.get("/update")
async def update(request):
    await asyncio.sleep(1)
    return html(f'''<span id="replace_me">{fake.name()}</span>''')
