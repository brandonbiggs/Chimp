import plotly as py
import plotly.graph_objs as go

chimp_generated_sentences_y = [693.7692308, 4872.384615, 7153.846154,
                               8239.115385, 8826.384615, 9071.807692,
                               9168.5, 9207.269231]
markov_generated_sentences_y = [3.423076923, 1.230769231, 0.7692307692,
                                0.7692307692, 0.7692307692, 0.7692307692,
                                0.7692307692, 0.7692307692]
sentence_length_x = [2, 4, 6, 8, 10, 12, 14, 16]

# Create a trace
chimp = go.Scatter(
    x=sentence_length_x,
    y=chimp_generated_sentences_y,
    name="Chimp"
)

markov = go.Scatter(
    x=sentence_length_x,
    y=markov_generated_sentences_y,
    name="Markov Model"
)

data = [chimp, markov]
layout = go.Layout(
    title='Sentence Length vs # of Sentences',
    xaxis=dict(
        title='Sentence Length',
        titlefont=dict(
        family='Courier New, monospace',
        size=18,
        color='#7f7f7f'
        )
    ),
    font=dict(
        size=20,
        family="Times"
    ),
    yaxis=dict(
        title='Number of Generated Sentenced',
        type="log",
    ),
    # legend=dict(
    #     orientation="h",
    #     xanchor='center',
    #     x=0.5,
    #     y=-0.35
    #     # xanchor="center",
    # ),
)

fig = go.Figure(data=data, layout=layout)
py.offline.plot(fig, filename='graphs/sentence_length_solutions.html')
