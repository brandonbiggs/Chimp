from plotly import tools
import plotly as py
import plotly.graph_objs as go

chimp_line_color = "blue"
chimp_line_colors = ["#3086FF", "#2C7AE8", "#286ED1", "#2362BA", "#1F56A3", "#1B4A8C", "#163D74"]
markov_line_color = "orange"
markov_line_colors = ["#FF4544", "#E83F3E", "#D13938", "#BA3332", "#A32C2C", "#8C2626", "#74201F"]

# Generated sentences of length 4
sentence_length_four_chimp = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    y=[3212, 52726, 66077, 75057, 80266],
    line=dict(color=chimp_line_colors[0]),
    name="CHiMP 4",line_shape='spline'
)
sentence_length_four_markov = go.Scatter(
    # x=[2500, 25000, 250000],
    x=[25, 250, 2500, 25000, 250000],
    # y=[41, 1412, 5267],
    y=[0, 0.03, 41, 1412, 5267],
    line=dict(color=markov_line_colors[0]),
    name="CoMP 4",line_shape='spline'
)
# Generated Sentences of length 6
sentence_length_six_chimp = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    y=[11398, 76595, 89444, 93077, 94649],
    line=dict(color=chimp_line_colors[1]),name="CHiMP 6",
    line_shape='spline'
)
sentence_length_six_markov = go.Scatter(
    # x=[2500, 25000, 250000],
    x=[25, 250, 2500, 25000, 250000],
    # y=[258, 4436, 3854],
    y=[0, 0.3, 258, 4436, 3854],
    line=dict(color=markov_line_colors[1]), name="CoMP 6",
    line_shape='spline'
)
# Generated Sentences of length 8
sentence_length_eight_chimp = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    y=[45582, 86715, 95705, 97385, 98053],
    line=dict(color=chimp_line_colors[2]),
    line_shape='spline' ,name="CHiMP 8"
)
sentence_length_eight_markov = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    # x=[2500, 25000, 250000],
    # y=[473, 7612, 2639],
    y=[0, 1.8, 473, 7612, 2639],
    line=dict(color=markov_line_colors[2]), name="CoMP 8",
    line_shape='spline'
)

# Generated Sentences of length 10
sentence_length_ten_chimp = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    y=[52547, 90422, 96093, 99143, 98998],
    line=dict(color=chimp_line_colors[3]),
    line_shape='spline',name="CHiMP 10"
)
sentence_length_ten_markov = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    # x=[2500, 25000, 250000],
    # y=[1457, 12936, 4132],
    y=[0, 0.69, 1457, 12936, 4132],
    line=dict(color=markov_line_colors[3]),
    line_shape='spline' , name="CoMP 10",
)

# Generated Sentences of length 12
sentence_length_twelve_chimp = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    y=[57810, 92141, 94732, 99481, 99528],
    line=dict(color=chimp_line_colors[4]),
    line_shape='spline',name="CHiMP 12"
)
sentence_length_twelve_markov = go.Scatter(
    # x=[2500, 25000, 250000],
    x=[25, 250, 2500, 25000, 250000],
    # y=[2258, 16751, 10403],
    y=[0, 0, 2258, 16751, 10403],
    line=dict(color=markov_line_colors[4]),
    line_shape='spline', name="CoMP 12",
)

# Generated Sentences of length 14
sentence_length_fourteen_chimp = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    y=[60698, 92236, 96153, 99715, 99750],
    line=dict(color=chimp_line_colors[5]),
    line_shape='spline',name="CHiMP 14"
)
sentence_length_fourteen_markov = go.Scatter(
    x=[25, 250, 2500, 25000, 250000],
    # x=[2500, 25000, 250000],
    y=[0, 4.76, 4802, 27119, 4219],
    # y=[4802, 27119, 4219],
    line=dict(color=markov_line_colors[5]),
    line_shape='spline', name="CoMP 14",
)

fig = go.Figure()
fig.update_xaxes(
    type="log", title="Number of Training Sentences",
    dtick = 1,
    titlefont = dict(size=21),
    showgrid = True, gridwidth = 0.5, gridcolor = 'grey',
    showline = True, linewidth = 1, linecolor = 'black',  # mirror=True
)
# range here is 10^5
fig.update_yaxes(
    type="log", title="Avg # of Unique Sequences", range=(0, 5),
    dtick=1,
    titlefont=dict(size=21),
    showgrid=True, gridwidth=0.5, gridcolor='grey',
    showline=True, linewidth=1, linecolor='black',  # mirror=True


)
fig.add_trace(sentence_length_four_chimp)
fig.add_trace(sentence_length_four_markov)
fig.add_trace(sentence_length_six_chimp)
fig.add_trace(sentence_length_six_markov)
fig.add_trace(sentence_length_eight_chimp)
fig.add_trace(sentence_length_eight_markov)
fig.add_trace(sentence_length_ten_chimp)
fig.add_trace(sentence_length_ten_markov)
fig.add_trace(sentence_length_twelve_chimp)
fig.add_trace(sentence_length_twelve_markov)
fig.add_trace(sentence_length_fourteen_chimp)
fig.add_trace(sentence_length_fourteen_markov)

# # Setup plot
# fig = tools.make_subplots(
#     rows=3,
#     cols=2,
#     subplot_titles=(
#         "Sentence Length 4",
#         "Sentence Length 6",
#         "Sentence Length 8",
#         "Sentence Length 10",
#         "Sentence Length 12",
#         "Sentence Length 14",
#     ),
# )
#
# # Sentence Length 4
# fig.append_trace(sentence_length_four_chimp, 1, 1)
# fig.append_trace(sentence_length_four_markov, 1, 1)
#
# # Sentence Length 6
# fig.append_trace(sentence_length_six_chimp, 1, 2)
# fig.append_trace(sentence_length_six_markov, 1, 2)
#
# # Sentence Length 8
# fig.append_trace(sentence_length_eight_chimp, 2, 1)
# fig.append_trace(sentence_length_eight_markov, 2, 1)
#
# # Sentence Length 10
# fig.append_trace(sentence_length_ten_chimp, 2, 2)
# fig.append_trace(sentence_length_ten_markov, 2, 2)
#
# # Sentence Length 12
# fig.append_trace(sentence_length_twelve_chimp, 3, 1)
# fig.append_trace(sentence_length_twelve_markov, 3, 1)
#
# # Sentence Length 14
# fig.append_trace(sentence_length_fourteen_chimp, 3, 2)
# fig.append_trace(sentence_length_fourteen_markov, 3, 2)
#
# x_axis_label = "# of Training Sentences"
# y_axis_label = "Average Number of Generated Sentences"
# fig["layout"]["xaxis1"].update(type="log")
# fig["layout"]["xaxis2"].update(type="log")
# fig["layout"]["xaxis3"].update(type="log")
# fig["layout"]["xaxis4"].update(type="log")
# fig["layout"]["xaxis5"].update(title=x_axis_label, type="log")
# fig["layout"]["xaxis6"].update(title=x_axis_label, type="log")
#
# fig["layout"]["yaxis1"].update(type="log", autorange=True, tickvals=[0, 10000, 100000])
# fig["layout"]["yaxis2"].update(type="log", autorange=True, tickvals=[0, 10000, 100000])
# # fig["layout"]["yaxis2"].update(type="log", autorange=True)
# fig["layout"]["yaxis3"].update(title=y_axis_label, type="log", autorange=True, tickvals=[0, 10000, 100000])
# fig["layout"]["yaxis4"].update(type="log", autorange=True, tickvals=[0, 10000, 100000])
# fig["layout"]["yaxis5"].update(type="log", autorange=True, tickvals=[0, 10000, 100000])
# fig["layout"]["yaxis6"].update(type="log", autorange=True, tickvals=[0, 10000, 100000])
# # fig.update_yaxes(range=[0, 100000])


fig["layout"].update(plot_bgcolor="white")
py.offline.plot(fig, filename="graphs/batch_generated_solutions_combined.html")
