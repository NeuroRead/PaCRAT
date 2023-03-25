#    ___       ________  ___ ______          .---.
#   / _ \___ _/ ___/ _ \/ _ /_  __/     (\./)     \.......-
#  / ___/ _ `/ /__/ , _/ __ |/ /        >' '<  (__.'""""BP
# /_/   \_,_/\___/_/|_/_/ |_/_/         " ` " "
#
# Pa(ragraph) C(omplexity) (and) R(arity) A(nalysis) T(ool)
# Authors: Griffin Pitts, Harris Sarfaraz, Sohal Sudheer

#-------------#
#   IMPORTS   #
#-------------#

from flask import Flask
from flask_restful import Resource, Api, reqparse

#---------------------------------#
#   INITIALIZE FLASK APP AND API  #
#---------------------------------#

app = Flask(__name__)                               # Creates Flask application
api = Api(app)                                      # Initializes the API

#-------------------------#
#   CONVERSION ENDPOINT   #
#-------------------------#

class Analyze(Resource):                            # Analysis Endpoint Class
    def post(self):                                 # POST method
        parser = reqparse.RequestParser()           # Initialize Parser
        parser.add_argument('text', required=True)  # Expects Argument with Text For Analysis
        args = parser.parse_args()                  # Parse Arguments to Dictionary
        return {'formatted': args['text']}          # Return Formatted Text
api.add_resource(Analyze, '/analyze')               # Adds endpoint to Flask API

#------------------------#
#   RUNS THE FLASK APP   #
#------------------------#

if __name__ == '__main__': app.run()                # Dunder