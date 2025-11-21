from sanic import Sanic, html
from datastar_py.sanic import datastar_response, ServerSentEventGenerator as SSE

import asyncio
import logging
from uuid import uuid4

from faker import Faker
import psutil


app = Sanic(__name__)
app.static('/static/', './static/')
app.static('/', './templates/index.html', name="index")
# app.update_config({'RESPONSE_TIMEOUT': 60*5})

fake = Faker()

logging.basicConfig(filename='perso.log', encoding='utf-8', level=logging.INFO)
logger = logging.getLogger(__name__)

async def wassup_psutil():
    while True:
        load_avg = psutil.getloadavg()
        memory = psutil.virtual_memory()
        app.ctx.db.update({
            'load_avg': str(load_avg),
            'mem_tot': f"{memory.total / (1024**2):.2f} MB",
            'mem_free':f"{memory.available / (1024**2):.2f} MB",
        })
        await asyncio.sleep(1)

app.add_task(wassup_psutil)

@app.before_server_start
async def open_connections(app):
    app.ctx.db = {'bot': "nope"}

@app.on_response
async def cookie(request, response):
    if not request.cookies.get("user_id"):
        user_id = uuid4().hex

@app.get("/blinking")
@datastar_response
async def blinking(request):
    while True:
        html = f'''
<body>
<section>
    <p>Load average: <span>{app.ctx.db['load_avg']}</span></p>
    <p>Free mem: <span>{app.ctx.db['mem_free']}</span></p>
    <p>Total mem: <span>{app.ctx.db['mem_tot']}</span></p>
</section>
</body>
'''
        yield SSE.patch_elements(html)
        await asyncio.sleep(1)

@app.post("/bot")
async def bot(request):
    app.ctx.db['bot'] = "OMG"
