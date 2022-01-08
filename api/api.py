from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#from crypto_prediction.utils import reshape_data_for_prediction, reshape_predicted_data, get_prediction
#from crypto_prediction.gcp import download_model, download_prediction_data
#from crypto_prediction.data import prediction_ready_df, coin_history, coin_history_gbq
#from crypto_prediction.model import data_cleaning


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"checking": "basic api works"}

@app.get("/ping")
def pingpong():
    return 'pong'

@app.get("/get/coin_history")
def get_coin_history(tickerlist, hoursback):
    """
    input:
        tickerlist      - ticker names seperated by comma: samo,doge,shib ..
        hoursback       - how many hours to look back (could take dates, too, not yet connected)

    output:
        dict
    """
    # we should sanitize here since its unknown input
    # ...

    tickerlist = tickerlist.split(',')

    return tickerlist

#if __name__ == '__main__':
#
#    output = predict_endpoint()
#    print(output)
