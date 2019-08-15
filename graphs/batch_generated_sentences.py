from plotly import tools
import plotly as py
import plotly.graph_objs as go

chimp_line_color = 'green'
markov_line_color = 'red'

# Generated sentences of length 4
sentence_length_four_chimp = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    y=[3212, 52726, 66077, 75057, 80266],
    line=dict(color=chimp_line_color),
    name='Chimp',
)
sentence_length_four_markov = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    y=[0, 0.03, 41, 1412, 5267],
    line=dict(color=markov_line_color),
    name="Markov"
)
# Generated Sentences of length 6
sentence_length_six_chimp = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    y=[11398, 76595, 89444, 93077, 94649],
    line=dict(color=chimp_line_color),
    showlegend=False,
)
sentence_length_six_markov = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    y=[0, 0.3, 258, 4436, 3854],
    line=dict(color=markov_line_color),
    showlegend=False,
)
# Generated Sentences of length 8
sentence_length_eight_chimp = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    y=[45582, 86715, 95705, 97385, 98053],
    line=dict(color=chimp_line_color),
    showlegend=False,
)
sentence_length_eight_markov = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    y=[0, 1.8, 473, 7612, 2639],
    line=dict(color=markov_line_color),
    showlegend=False,
)

# Generated Sentences of length 10
sentence_length_ten_chimp = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    y=[52547, 90422, 96093, 99143, 98998],
    line=dict(color=chimp_line_color),
    showlegend=False,
)
sentence_length_ten_markov = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    y=[0, 0.69, 1457, 12936, 4132],
    line=dict(color=markov_line_color),
    showlegend=False,
)

# Generated Sentences of length 12
sentence_length_twelve_chimp = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    y=[57810, 92141, 94732, 99481, 99528],
    line=dict(color=chimp_line_color),
    showlegend=False,
)
sentence_length_twelve_markov = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    y=[0, 0, 2258, 16751, 10403],
    line=dict(color=markov_line_color),
    showlegend=False,
)

# Generated Sentences of length 14
sentence_length_fourteen_chimp = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    y=[60698, 92236, 96153, 99715, 99750],
    line=dict(color=chimp_line_color),
    showlegend=False,
)
sentence_length_fourteen_markov = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    y=[0, 4.76, 4802, 27119, 4219],
    line=dict(color=markov_line_color),
    showlegend=False,
)

# Setup plot
fig = tools.make_subplots(rows=3,
                          cols=2,
                          subplot_titles=('Sentence Length 4',
                                          'Sentence Length 6',
                                          'Sentence Length 8',
                                          'Sentence Length 10',
                                          'Sentence Length 12',
                                          'Sentence Length 14'),
                          )

# Sentence Length 4
fig.append_trace(sentence_length_four_chimp, 1, 1)
fig.append_trace(sentence_length_four_markov, 1, 1)

# Sentence Length 6
fig.append_trace(sentence_length_six_chimp, 1, 2)
fig.append_trace(sentence_length_six_markov, 1, 2)

# Sentence Length 8
fig.append_trace(sentence_length_eight_chimp, 2, 1)
fig.append_trace(sentence_length_eight_markov, 2, 1)

# Sentence Length 10
fig.append_trace(sentence_length_ten_chimp, 2, 2)
fig.append_trace(sentence_length_ten_markov, 2, 2)

# Sentence Length 12
fig.append_trace(sentence_length_twelve_chimp, 3, 1)
fig.append_trace(sentence_length_twelve_markov, 3, 1)

# Sentence Length 14
fig.append_trace(sentence_length_fourteen_chimp, 3, 2)
fig.append_trace(sentence_length_fourteen_markov, 3, 2)

x_axis_label = "# of Training Sentences"
y_axis_label = "Average Number of Generated Sentences"
fig['layout']['xaxis1'].update(type='log')
fig['layout']['xaxis2'].update(type='log')
fig['layout']['xaxis3'].update(type='log')
fig['layout']['xaxis4'].update(type='log')
fig['layout']['xaxis5'].update(title=x_axis_label, type='log')
fig['layout']['xaxis6'].update(title=x_axis_label, type='log')

fig['layout']['yaxis1'].update(type='log',
        autorange=True)
fig['layout']['yaxis2'].update(type='log',
        autorange=True)
fig['layout']['yaxis3'].update(title=y_axis_label, type='log',
        autorange=True)
fig['layout']['yaxis4'].update(title=y_axis_label, type='log',
        autorange=True)
fig['layout']['yaxis5'].update(type='log',
        autorange=True)
fig['layout']['yaxis6'].update(type='log',
        autorange=True)


fig['layout'].update(title='Generated Sentences Based on Training Sentences')
py.offline.plot(fig, filename='graphs/batch_generated_solutions.html')
