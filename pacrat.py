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

from typing import Annotated
from fastapi import Body,FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aenigma import analyzer

#------------------------#
#   INITIALIZE FastAPI   #
#------------------------#

app = FastAPI()                                     # Creates FastAPI App
origins = ["*"]
analyzer.initialize_nltk()                          # Downloads tokenizer for Aenigma 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#---------------------------#
#   SANITY CHECK ENDPOINT   #
#---------------------------#

@app.get("/sanitycheck")                            # Sanity check endpoint to ensure server is accessible
async def sanity_check():
    return {"message": "Get request successful"}

#-------------------------#
#   CONVERSION ENDPOINT   #
#-------------------------#

@app.post("/analyze")                               # Text Processing Endpoint
async def analyze(text: Annotated[str, Body(embed=True)]):
    return {"formatted": format_complexity(text)}   # Returns results of format_complexity()

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