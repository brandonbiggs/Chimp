from bllipparser import RerankingParser
from nltk.tree import Tree
from nltk.draw.tree import TreeView
import re
import os

sentence = "John likes the blue house at the end of the street"

rrp = RerankingParser.from_unified_model_dir('../nltk_data/models/WSJ-PTB3')
parsed_sentence = rrp.simple_parse(sentence)

print(parsed_sentence)
t = Tree.fromstring(parsed_sentence)
TreeView(t)._cframe.print_to_file('output.ps')
os.system('convert output.ps output.png')
