# coding = utf-8
"""
create on : 2019/02/15
file name : font_graph 

draw graph by installed all font names

"""
import json
import subprocess
import re
import warnings

import networkx as nx

from cairosvg import svg2png

# ignore Graphviz warning messages
warnings.simplefilter('ignore', RuntimeWarning)

SYMBOL_FONT_KEY_WORD = ["Emoji", "Marlett", "MDL2", "Symbol", "dings"]
RE_PATTERN = "(" + "|".join(SYMBOL_FONT_KEY_WORD) + ")"

BASE_FONT = "ＭＳ Ｐゴシック"

INDEX_SIZE = 16
HEADER_SIZE = 12


def get_font_json():
    """ get installed font list by json file

    :return: font name {JP: EN} dict
    """
    separete = "★" * 10

    cmd = r'powershell .\getenfont.ps1 "{}"'.format(separete)

    result = subprocess.run(cmd,
                            shell=True,
                            check=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    def binary2str_list(binary):
        """ byte type output decode to str to split by separator string

        :param binary: binary output byte
        :return: font name list
        """
        return binary.decode("cp932").split(separete)

    font_dict = {binary2str_list(line)[0]: binary2str_list(line)[1]
                 for line in result.stdout.splitlines()}

    with open("./output/font.json", mode="w", encoding="utf-8") as f:
        json.dump(font_dict, f, ensure_ascii=False, sort_keys=True, indent=4)

    return font_dict


def draw_font_graph():
    """ draw graph by installed fonts

    :return: None
    """

    # create graph
    g = nx.DiGraph()

    font_dict = get_font_json()

    font_key_list = sorted(list(font_dict.keys()))

    font_initial_list = []
    font_header_list = []

    for node in font_key_list:

        # add a node font name jp
        if not re.search(RE_PATTERN, node):
            g.add_node(node, fontsize=8, fontname=font_dict[node])

        else:
            font_key_list.remove(node)
            continue

        font_initial = font_dict[node][0].upper()

        # add a node and edge font name initial
        if not font_initial_list:
            g.add_node(font_initial,
                       fontsize=INDEX_SIZE, fontname=font_dict[BASE_FONT],
                       fillcolor="gray", style="filled", penwidth=2)

            font_initial_list.append(font_initial)

        elif font_initial not in font_initial_list:
            g.add_node(font_initial,
                       fontsize=INDEX_SIZE, fontname=font_dict[BASE_FONT],
                       fillcolor="gray", style="filled", penwidth=2)

            g.add_edge(font_initial_list[-1], font_initial,
                       arrowhead="empty")

            font_initial_list.append(font_initial)

        split_font_key = node.split(" ")[0] + "-Family"

        # add a node and edge name header and font name
        if not font_header_list:
            g.add_node(split_font_key,
                       fontsize=HEADER_SIZE, fontname=font_dict[BASE_FONT],
                       peripheries=2)

            font_header_list.append(split_font_key)

            g.add_edge(font_initial, split_font_key,
                       arrowhead="open")

        elif split_font_key not in font_header_list:
            g.add_node(split_font_key,
                       fontsize=HEADER_SIZE, fontname=font_dict[BASE_FONT],
                       peripheries=2)

            font_header_list.append(split_font_key)

            g.add_edge(font_initial, split_font_key,
                       arrowhead="open")

        # add a edge name header and font name
        if split_font_key != node:
            g.add_edge(split_font_key, node)

    # networkx digraph convert to graphviz A graph
    a_graph = nx.nx_agraph.to_agraph(g)
    a_graph.graph_attr.update(K=0.4, splines=True)

    file_name = "./output/font_graph.{format}"

    # a graph save to svg
    file_format = "svg"
    svg_file_name = file_name.format(format=file_format)
    a_graph.draw(svg_file_name, prog="fdp", format=file_format)

    svg2png(url=svg_file_name, write_to=file_name.format(format="png"))


if __name__ == "__main__":
    draw_font_graph()
