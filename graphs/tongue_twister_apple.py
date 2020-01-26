import plotly as py
import plotly.graph_objs as go

chimp_generated_sentences_y = [7, 8, 10, 14, 20, 32]
markov_generated_sentences_y = [4, 3, 2, 1, 0, 0]
sentence_length_x = [2, 3, 4, 5, 7, 9]

# Create a trace
chimp = go.Scatter(x=sentence_length_x, y=chimp_generated_sentences_y, name="Chimp")

markov = go.Scatter(
    x=sentence_length_x,
    y=markov_generated_sentences_y,
    name="Standard Markov Model Order 1",
)

data = [chimp, markov]
layout = go.Layout(
    title="Sentence Length vs # of Sentences",
    # annotations=[
    #     dict(
    #         x=0.5,
    #         y=-0.3,
    #         showarrow=False,
    #         text='Length of Mnemonic',
    #         xref='paper',
    #         yref='paper',
    #         font=dict(
    #             size=20,
    #             # color="#7f7f7f",
    #             family="Times",
    #         ),
    #     ),
    # ],
    xaxis=dict(
        title="Sentence Length",
        titlefont=dict(family="Courier New, monospace", size=18, color="#7f7f7f"),
    ),
    font=dict(size=20, family="Times"),
    yaxis=dict(
        title="Number of Generated Sentenced",
        type="linear",
        range=[0, 35],
        titlefont=dict(
            # family='Courier New, monospace',
            # size=18,
            # color='#7f7f7f'
        ),
    ),
    legend=dict(
        orientation="h",
        xanchor="center",
        x=0.5,
        y=-0.35
        # xanchor="center",
    ),
)

fig = go.Figure(data=data, layout=layout)
py.offline.plot(fig, filename="basic-line.html")
