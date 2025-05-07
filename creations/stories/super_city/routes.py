from pilot.qmd.app import qmd_sub_app

app, rt = qmd_sub_app(__file__)

@app.route('/{city}')
def get(city:str=None):
    if city:
        return city + "!!!"
    else:
        return 'Hello!!!!!!'

@app.route('/something/waits')
def get():
    return 'Hello world!'



