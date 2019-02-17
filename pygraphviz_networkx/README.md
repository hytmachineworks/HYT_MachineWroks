# Pygraphviz NetworkX Example

![Font Network image](./readme_img.png "Font network")

Build DiGraph by [networkx](https://networkx.github.io/), 
draw svg file by [PyGraphviz](https://pygraphviz.github.io/).  
And svg file convert to png file by [CairoSVG](https://cairosvg.org/)

Network source is already installed font names. 
Its name index and header words are key of network, 
and connect to all font names.

Often on multibyte word environment difficult to change font on Graphviz.

I found easy way to draw svg file and convert to png file.
But when draw svg, Graphviz does not accept multibyte font name (メイリオ,etc).
So I need to Know its english font names.

[9bic](https://github.com/9bic) develop [getenfont.ps1](https://gist.github.com/9bic/5a3ecc2c9f2e4ef38065)
it gives font's Japanese and English both names. 
I modified [gentenfont.ps1](https://gist.github.com/hytmachineworks/ec5ed480af010a897373535a55800525)
add a function separete string given by argment. Using its output and separete strings,
get font name dictionary.

So I can freely use Graphviz on Multibyte word environment.

## Usage

Try command beleow

> python font_graph.py

After that you get png and svg file on ./output/ directory.

---
### FYI.

You can get conda env YAML file, pgv_nx.yml . 
Try command below, you can create same environment on me.

>conda env create -n pgv_nx -f pgv_nx.yml
