from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
from src.dashboard import Graphs

app = Flask(__name__)

@app.route('/')
def dashboard():
   df = pd.read_csv("src/dataset/final_dataset.csv")

   f_message_count         = Graphs.message_count(df, 'month')
   f_word_count            = Graphs.word_count(df, 'month')
   f_avg_words_per_message = Graphs.avg_words_per_message(df, 'month')

   graphs = [f_message_count, f_word_count, f_avg_words_per_message]
   graphJSON = [json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder) for graph in graphs]

   return render_template('index.html', graphJSON=graphJSON)

if __name__ == "__main__":
    app.run(debug=True)