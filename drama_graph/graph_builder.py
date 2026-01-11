from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Dict, Iterable, List, Set, Tuple

import networkx as nx


@dataclass(frozen=True)
class DramaGraphResult:
    """
    Ergebnisobjekt für den Figuren-Graphen.

    - graph: NetworkX Graph, Knoten = Figuren-IDs, Kanten = Ko-Okkurrenz (z.B. gemeinsame Szene)
    - speaker_counts: Anzahl der <sp>-Vorkommen pro Figur (Speaker turns)
    - id_to_name: Mapping von Figuren-ID (xml:id) zu Anzeigename (persName)
    """
    graph: nx.Graph
    speaker_cnts: Dict[str, int]
    id_to_name: Dict[str, str]

    @property
    def NumCharacters(self) -> int:
        return self.graph.number_of_nodes()

    @property
    def NumEdges(self) -> int:
        return self.graph.number_of_edges()

    def __len__(self) -> int:
        """
        Damit len(result) nicht mehr crasht:
        Definiert als Anzahl Figuren (Graph-Knoten).
        """
        return self.NumCharacters


def build_character_graph(
    scene_speakers: Iterable[Set[str]],
    sp_cnt: Dict[str, int],
    id_to_name: Dict[str, str],
) -> DramaGraphResult:
    """
    Baut einen gewichteten Ko-Okkurrenz-Graphen:
    Für jede Szene wird für alle Figurenpaare in dieser Szene das Kantengewicht erhöht.

    scene_speakers: iterierbar über Sets von Figuren-IDs pro Szene.
    speaker_counts: dict[figuren_id] -> #<sp> (Sprecherauftritte)
    id_to_name: dict[figuren_id] -> Name
    """
    G = nx.Graph()

    # Knoten anlegen (auch Figuren ohne Kanten sollen drin sein)
    for char_id in id_to_name.keys():
        G.add_node(char_id, label=id_to_name.get(char_id, char_id))

    # Kanten/Weights pro Szene
    for speakers_in_scene in scene_speakers:
        ids = sorted(speakers_in_scene)
        for a, b in combinations(ids, 2):
            if G.has_edge(a, b):
                G[a][b]["weight"] += 1
            else:
                G.add_edge(a, b, weight=1)

    # Speaker counts als Node-Attribut speichern (praktisch für Gephi)
    for char_id, cnt in sp_cnt.items():
        if char_id in G:
            G.nodes[char_id]["speech_count"] = cnt

    return DramaGraphResult(graph=G, speaker_cnts=sp_cnt, id_to_name=id_to_name)
