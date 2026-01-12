from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import networkx as nx


def node_colors_by_speech_count(graph: nx.Graph):
    return "#6baed6"

def render_graph_png(
    output_path: Path,
    graph: nx.Graph,
    title: Optional[str] = None,
) -> None:
    """
    Rendert einen NetworkX-Graphen als PNG.

    - Knotengröße ∝ speech_count (falls vorhanden)
    - Kantendicke ∝ weight
    """
    if graph.number_of_nodes() == 0:
        raise ValueError("Graph has no nodes – nothing to render.")

    plt.figure(figsize=(14, 14))

    # Layout (reproduzierbar)
    pos = nx.spring_layout(graph, seed=42)

    # Knotengrößen
    sizes = []
    for n in graph.nodes:
        sizes.append(300 + 40 * graph.nodes[n].get("speech_count", 1))

    # Kantengewichte
    weights = [graph[u][v].get("weight", 1) for u, v in graph.edges]

    nx.draw_networkx_nodes(
        graph,
        pos,
        node_size=sizes,
        node_color=node_colors_by_speech_count(graph),
        alpha=0.9,
    )

    nx.draw_networkx_edges(
        graph,
        pos,
        width=weights,
        alpha=0.5,
    )

    nx.draw_networkx_labels(
        graph,
        pos,
        labels={
            n: graph.nodes[n].get("label", n)
            for n in graph.nodes
        },
        font_size=9,
    )

    if title:
        plt.title(title)

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.show()
    plt.close()
