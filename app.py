from sanic import Sanic, html

from faker import Faker

import asyncio


app = Sanic(__name__)
app.static('/static/', './static/')
app.static('/', './templates/index.html', name="index")

fake = Faker()


@app.put("/activate")
async def activate(request):
    return html('''
<tr id="row1">
    <td>John</td>
    <td id="row1-status" active>Active</td>
</tr>
''')

@app.put("/deactivate")
async def deactivate(request):
    return html('''
<tr id="row1">
    <td>John</td>
    <td id="row1-status" inactive>Inactive</td>
</tr>
''')

@app.get("/load_more/<n>")
async def load_more(request, n):
    '''i think there's something in sanic for checking n'''
    try:
        n = int(n)
    except ValueError:
        return html("", status=204)
    if n > 7:
        return html("", status=204)
    raw_html = f'''
<div id="list">
    {"".join(f"<div>Item {i}</div>" for i in range(1, n + 1))}
    <button data-on-click="@get('/load_more/{n+1}')">Load more</button>
</div>
'''
    return html(raw_html)

@app.get("/redirect")
async def redirect(request):
    return html('''
<div id="indicator" 
data-signals-seconds=3
data-on-interval="
$seconds -= 1;
$seconds = Math.max($seconds, 0);
$seconds == 0 ? setTimeout(() => window.location.href = 'https://www.google.fr') : null
">
Redirecting in 
<span data-text="$seconds"></span>
</div>
''')
