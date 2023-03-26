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
from aenigma import analyzer

#-------------------------------------------#
#   INITIALIZE FLASK APP, API, AND AENIGMA  #
#-------------------------------------------#

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
        formatted = format_complexity(args['text']) # Call format_complexity to add complexity stratification
        return {'formatted': formatted}             # Return Formatted Text
api.add_resource(Analyze, '/analyze')               # Adds endpoint to Flask API

#--------------------#
#   HELPER METHODS   #
#--------------------#

def format_complexity(text: str) -> str:            # Sentence Complexity Formatting Helper
    rcs_vals = analyzer.generate_rcs_list(text)     # Calls Aenigma to get RCS scores of sentences
    for (item, rcs) in rcs_vals:                    # Iterate through original text and add spans (preserves whitespace)
        lvl = int((1-rcs)*6)                        # Level 1 is most emphasized/complex, 6 is least
        text = text.replace(                        # Replace sentence in text with formatted sentence
            item,
            f"<span class='level{lvl}'>{item}</span>"
            )
    return text                                     # Return formatted text

#------------------------#
#   RUNS THE FLASK APP   #
#------------------------#

if __name__ == '__main__':
    analyzer.initialize_nltk()                      # Downloads tokenizer for Aenigma 
    app.run('0.0.0.0')                                       # Runs Flask app