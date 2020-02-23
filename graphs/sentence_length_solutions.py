import plotly as py
import plotly.graph_objs as go

chimp_generated_sentences_y = [
    693.7692308,
    4872.384615,
    7153.846154,
    8239.115385,
    8826.384615,
    9071.807692,
    9168.5,
    9207.269231,
]
markov_generated_sentences_y = [
    3.423076923,
    1.230769231,
    0.7692307692,
    0.7692307692,
    0.7692307692,
    0.7692307692,
    0.7692307692,
    0.7692307692,
]
sentence_length_x = [2, 4, 6, 8, 10, 12, 14, 16]

# Create a trace
chimp = go.Scatter(
    x=sentence_length_x, y=chimp_generated_sentences_y, name="CHiMP", line=dict(color="#3086FF"),
    )

markov = go.Scatter(
    x=sentence_length_x, y=markov_generated_sentences_y, name="CoMP", line=dict(color='#FF4544'),
)

data = [chimp, markov]
layout = go.Layout(
    # title="Sentence Length vs # of Sentences",
    xaxis=dict(
        title="Sentence Length",
        titlefont=dict(size=21),
        showgrid=True, gridwidth=0.5, gridcolor='grey',
        showline=True, linewidth=1, linecolor='black', #mirror=True
    ),
    plot_bgcolor="white",
    # font=dict(size=17.5),
    yaxis=dict(
        title="Avg # of Unique Sequences",
        type="log",
        dtick=1,
        titlefont=dict(size=21),
        showgrid=True, gridwidth=0.5, gridcolor='grey',
        showline=True, linewidth=1, linecolor='black', #mirror=True
    ),
)

fig = go.Figure(data=data, layout=layout)
py.offline.plot(fig, filename="graphs/sentence_length_solutions.html")
