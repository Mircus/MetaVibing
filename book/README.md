# The Book Pipeline

**Current canonical source:** [`manuscript.md`](manuscript.md). If you're reading the manual, this is the file — everything else in `book/` is either an old edition kept for reference or a future build output that doesn't exist yet.

```
book/
├── manuscript.md          ← canonical current source (Markdown)
├── README.md              ← this file
├── assets/                ← logo + diagrams used by the built PDF/DOCX (generated, but committed)
└── archive/
    ├── v1/                ← the prior packaged edition (.md, .docx, .pdf) — superseded in content by manuscript.md
    └── original/          ← the original unexpanded manuscript (.docx) and its direct Markdown conversion, predating MetaVibing's expansion

dist/                      ← packaged releases, built from manuscript.md:
├── MetaVibing-Field-Manual-v0.1.pdf    ← the public reading artifact
└── MetaVibing-Field-Manual-v0.1.docx   ← secondary; optimized for PDF first
```

## Why this shape

Before this reorganization, `book/` held five different manuscript-shaped files at once (two packaged editions, a direct-conversion draft, and the original source docx), and the top-level README had to explain which one was "current" in prose. One canonical source removes the ambiguity structurally instead of by convention.

`archive/` exists so history isn't lost — the prior edition and the original manuscript are legitimate artifacts, just not the current one. They stay archived, not deleted, and are never edited after being moved here; if you need to know what v1 said, read `archive/v1/`, don't reconstruct it from memory.

## Building a release

```bash
python scripts/gen_assets.py     # regenerate the logo + 4 diagrams (only needed if these change)
python scripts/build_manual.py   # rebuild dist/MetaVibing-Field-Manual-v0.1.{pdf,docx} from manuscript.md
```

Requires `reportlab`, `python-docx`, `matplotlib`, and `Pillow` (all pure-Python, no native dependencies beyond what pip installs). Do not hand-edit anything under `dist/` — regenerate it from `manuscript.md` instead, or the two will drift.

The build is a small custom Markdown parser (`scripts/md_parse.py`) plus two renderers, not a general-purpose tool — it supports exactly what `manuscript.md` uses: headings, code fences, blockquotes, tables, lists, and two custom directives: `<!-- diagram: NAME -->` (renders one of the four `book/assets/diagram-*.png` files) and `<!-- callout:TYPE -->...<!-- /callout -->` (PRINCIPLE / PRACTICE / WARNING / EVIDENCE colored boxes). Both directives are HTML comments, so they render as nothing when the manuscript is read as plain Markdown on GitHub.
