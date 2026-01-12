from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Dict, List, Set, Tuple

from lxml import etree

# tei namespace 
TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}


def ParseDracorTei(
    xml_path: Path,
) -> tuple[
    Dict[str, str],      # id_to_name
    List[Set[str]],      # scene_speakers
    Dict[str, int],      # speaker_counts
]:
    """
    Liest ein DraCor-TEI-Drama ein und extrahiert:

    - Figuren (xml:id -> Anzeigename)
    - Sprecher pro Szene (Set von Figuren-IDs)
    - Sprechhäufigkeiten (Anzahl <sp> pro Figur)
    """
    tree = etree.parse(str(xml_path))
    root = tree.getroot()

    # ------------------------------------------------------------
    # 1) Figurenliste
    # ------------------------------------------------------------
    id_to_name: Dict[str, str] = {}

    persons = root.xpath(
        ".//tei:teiHeader//tei:listPerson//tei:person",
        namespaces=TEI_NS,
    )

    for person in persons:
        pid = person.get("{http://www.w3.org/XML/1998/namespace}id")
        if not pid:
            continue

        name_el = person.find("tei:persName", namespaces=TEI_NS)
        name = (
            " ".join(name_el.itertext()).strip()
            if name_el is not None
            else pid
        )
        id_to_name[pid] = name

    # ------------------------------------------------------------
    # 2) Szenen → Sprecher
    # ------------------------------------------------------------
    scene_speakers: List[Set[str]] = []
    speaker_counter: Counter[str] = Counter()

    scenes = root.xpath(
        ".//tei:text//tei:div[@type='scene']",
        namespaces=TEI_NS,
    )

    for scene in scenes:
        speakers_in_scene: Set[str] = set()

        for sp in scene.xpath(".//tei:sp", namespaces=TEI_NS):
            who = sp.get("who")
            if not who:
                continue

            # who kann "#id1 #id2" sein
            for ref in who.split():
                char_id = ref.lstrip("#") #entfernt # am Anfang mit .lstrip
                speakers_in_scene.add(char_id)
                speaker_counter[char_id] += 1

        if speakers_in_scene:
            scene_speakers.append(speakers_in_scene)

    return id_to_name, scene_speakers, dict(speaker_counter)
