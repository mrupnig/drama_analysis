from __future__ import annotations

from pathlib import Path

from drama_graph.dracor_reader import parse_dracor_tei
from drama_graph.graph_builder import build_character_graph
from drama_graph.visualize import render_graph_png
from drama_graph.report import write_speaker_counts_csv, write_graph_gexf

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_XML = PROJECT_ROOT / "data" / "drama.xml"
DEFAULT_OUT = PROJECT_ROOT / "output"
DEFAULT_TITLE = "DraCor-TEI Character Graph"


def run(xml_path: Path = DEFAULT_XML, out_dir: Path = DEFAULT_OUT, title: str = DEFAULT_TITLE) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) TEI einlesen
    id_to_name, scene_speakers, speaker_counts = parse_dracor_tei(xml_path)

    # 2) Graph bauen
    res = build_character_graph(
        scene_speakers=scene_speakers,
        sp_cnt=speaker_counts,
        id_to_name=id_to_name,
    )

    # WICHTIG: nicht len(result), sondern explizit:
    print(f"Parsed: {res.num_characters} characters, {res.num_edges} edges")

    # 3) Reports/Exports
    csv_path = out_dir / "character_speech_counts.csv"
    gexf_path = out_dir / "character_graph.gexf"
    png_path = out_dir / "character_graph.png"

    write_speaker_counts_csv(csv_path, res)
    write_graph_gexf(gexf_path, res)

    # 4) Visualisierung
    render_graph_png(png_path, res.graph, title=title)

    print(f"Wrote: {csv_path}")
    print(f"Wrote: {gexf_path}")
    print(f"Wrote: {png_path}")


if __name__ == "__main__":
    run()
