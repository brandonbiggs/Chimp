from plotly import tools
import plotly as py
import plotly.graph_objs as go

# Generated sentences of length 4
sentence_length_four_chimp = go.Scatter(
    x=[1, 4, 10, 25, 50, 100, 500],
    y=[0.1153846154, 13.88461538, 159.9230769,
        1755.923077, 3580.384615, 4883.538462,
        6933.346154]
)
sentence_length_four_markov = go.Scatter(
    x=[1, 4, 10, 25, 50, 100, 500],
    y=[0, 0, 0, 0, 0.1153846154, 1.230769231, 41.03846154]
    # y=[1, 1, 1, 1, 0.1153846154, 1.230769231, 41.03846154]
)
# Generated Sentences of length 6
sentence_length_six_chimp = go.Scatter(
    x=[1, 4, 10, 25, 50, 100, 500],
    y=[0.1153846154, 96.42307692, 819.5, 4194.730769, 6224.807692,
       7150.346154, 8736.346154]
)
sentence_length_six_markov = go.Scatter(
    x=[1, 4, 10, 25, 50, 100, 500],
    y=[0, 0, 0, 0, 0, 0.7692307692, 120.0384615]
    # y=[1, 1, 1, 1, 1, 0.7692307692, 120.0384615]
)
# Generated Sentences of length 8
sentence_length_eight_chimp = go.Scatter(
    x=[1, 4, 10, 25, 50, 100, 500],
    y=[0.1153846154, 300.3076923, 1756.192308, 4194.730769, 7237.038462,
       8239.730769, 9157.153846]
)
sentence_length_eight_markov = go.Scatter(
    x=[1, 4, 10, 25, 50, 100, 500],
    y=[0, 0, 0, 0, 0, 0.7692307692, 240.9615385]
    # y=[1, 1, 1, 1, 1, 0.7692307692, 240.9615385]
)

# Generated Sentences of length 10
sentence_length_ten_chimp = go.Scatter(
    x=[1, 4, 10, 25, 50, 100, 500],
    y=[0.1153846154, 494.2692308, 2554.230769, 6492.461538, 7635.807692,
       8830.730769, 9223.461538]
)
sentence_length_ten_markov = go.Scatter(
    x=[1, 4, 10, 25, 50, 100, 500],
    y=[0, 0, 0, 0, 0, 0.7692307692, 358.3076923]
    # y=[1, 1, 1, 1, 1, 0.7692307692, 358.3076923]
)

# Setup plot
fig = tools.make_subplots(rows=2,
                          cols=2,
                          subplot_titles=('Sentence Length 4',
                                          'Sentence Length 6',
                                          'Sentence Length 8',
                                          'Sentence Length 10'),
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

x_axis_label = "# of Training Sentences"
y_axis_label = "Average Number of Generated Sentences"
fig['layout']['xaxis1'].update(type='log')
fig['layout']['xaxis2'].update(type='log')
fig['layout']['xaxis3'].update(title=x_axis_label, type='log')
fig['layout']['xaxis4'].update(title=x_axis_label, type='log')

fig['layout']['yaxis1'].update(type='log',
        autorange=True)
fig['layout']['yaxis2'].update(type='log',
        autorange=True)
fig['layout']['yaxis3'].update(title=y_axis_label, type='log',
        autorange=True)
fig['layout']['yaxis4'].update(title=y_axis_label, type='log',
        autorange=True)


fig['layout'].update(title='Generated Sentences Based on Training Sentences')
py.offline.plot(fig, filename='graphs/training_generated_solutions.html')
