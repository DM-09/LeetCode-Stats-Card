from flask import Flask, Response
import requests as req
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'max-age=1800'
    return response


@app.route("/v1/<string:name>", methods=['GET'])
def Create_V1_Badge(name):
    URL = f'https://leetcode-stats-api.herokuapp.com/{name}'
    try:
        get = req.get(URL).json()
        if len(name) > 13: name = name[:13] + '...'

        SVG = '''
            <svg xmlns="http://www.w3.org/2000/svg" width="350" height="170">
              <style>
              @import url('https://fonts.googleapis.com/css2?family=Jost');
                .bg {{ fill:#5b5b56 }}
                .Solved {{fill: white; font-size:1.6em; font-family: 'Jost', sans-serif;}}
    
                .sf {{font-size:1em; font-family: 'Jost', sans-serif;}}
                .bf {{font-size:1.3em; font-family: 'Jost', sans-serif;}}
              </style>
    
    
              <rect width="350" height="170" class="bg" rx="7" ry="7"/>
    
    
    
              <text id="User" x="20" y="45" font-weight="bold" class="bf" fill="white">{User}</text>
              <text id="EZ" x="20" y="80" class="sf" fill="white">Easy <tspan x="94.5">{EZ}</tspan></text>
              <text id="Med" x="20" y="100" class="sf" fill="white">Medium <tspan x="94.5">{Med}</tspan></text>
              <text id="Med" x="20" y="120" class="sf" fill="white">Hard <tspan x="94.5">{Hard}</tspan></text>
              <circle cx="269" cy="80" r="43" class="bg" stroke="white" stroke-width="3"></circle>
    
              <text id="Soved" class="Solved" x="268.5" y="90" text-anchor="middle" font-weight="bold">{Solved}</text>
            </svg>'''.format(User=name, EZ=get['easySolved'], Med=get['mediumSolved'], Hard=get['hardSolved'],
                             Solved=get['totalSolved'])

    except: return Response('error'), 404
    return Response(SVG, mimetype='image/svg+xml'), 200
