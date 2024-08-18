from IPython.display import display, Image


def display_graph(graph):


    png_data = graph.get_graph().draw_png()


    image = Image(data=png_data, width=300, height=300)

    display(image)