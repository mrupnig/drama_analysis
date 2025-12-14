from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, Tuple

import networkx as nx

from .graph_builder import DramaGraphResult


def write_speaker_counts_csv(output_path: Path, result: DramaGraphResult) -> None:
    """
    Schreibt eine CSV-Tabelle: Figur, #Sprechauftritte (<sp>), optional Name.

    Spalten:
    - character_id
    - character_name
    - speech_count
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for char_id, count in result.speaker_cnts.items():
        rows.append(
            (
                char_id,
                result.id_to_name.get(char_id, char_id),
                int(count),
            )
        )

    # Sortierung: häufigste zuerst, dann Name
    rows.sort(key=lambda r: (-r[2], r[1].lower()))

    with output_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["character_id", "character_name", "speech_count"])
        w.writerows(rows)


def write_graph_gexf(output_path: Path, result: DramaGraphResult) -> None:
    """
    Exportiert den Graphen als GEXF (z.B. für Gephi).

    Schreibt Node-Attribute:
    - label (Name)
    - speech_count (falls vorhanden)
    Edge-Attribute:
    - weight
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Sicherstellen, dass label/speech_count als Attribute vorhanden sind
    G = result.graph.copy()

    for n in G.nodes:
        G.nodes[n]["label"] = G.nodes[n].get("label", result.id_to_name.get(n, n))
        if "speech_count" not in G.nodes[n]:
            G.nodes[n]["speech_count"] = int(result.speaker_cnts.get(n, 0))

    for u, v in G.edges:
        G[u][v]["weight"] = int(G[u][v].get("weight", 1))

    nx.write_gexf(G, str(output_path))
