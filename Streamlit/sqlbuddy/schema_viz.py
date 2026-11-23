"""Turn a schema into Graphviz DOT, which Streamlit draws with st.graphviz_chart."""
from __future__ import annotations

from html import escape


def _id(name: str) -> str:
    return '"' + name.replace('"', '\\"') + '"'


def schema_to_dot(tables: dict, foreign_keys: list) -> str:
    lines = [
        "digraph schema {",
        "rankdir=LR;",
        'bgcolor="transparent";',
        'node [shape=plaintext fontname="Helvetica" fontsize=11];',
        'edge [color="#1D4ED8" fontname="Helvetica" fontsize=9];',
    ]
    for table, columns in tables.items():
        rows = "".join(
            f'<TR><TD ALIGN="LEFT">{"<B>" if pk else ""}{escape(name)}{"</B>" if pk else ""}</TD>'
            f'<TD ALIGN="LEFT"><I>{escape(ctype or "")}</I></TD></TR>'
            for name, ctype, pk in columns
        )
        lines.append(
            f'{_id(table)} [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'
            f'<TR><TD COLSPAN="2" BGCOLOR="#1D4ED8"><FONT COLOR="white"><B>{escape(table)}</B></FONT></TD></TR>'
            f"{rows}</TABLE>>];"
        )
    for src, col, dst, dst_col in foreign_keys:
        label = f"{col} → {dst_col}" if dst_col else col
        lines.append(f'{_id(src)} -> {_id(dst)} [label="{escape(label)}"];')
    lines.append("}")
    return "\n".join(lines)
