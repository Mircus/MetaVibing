# The Book Pipeline

**Current canonical source:** [`manuscript.md`](manuscript.md). If you're reading the manual, this is the file — everything else in `book/` is either an old edition kept for reference or a future build output that doesn't exist yet.

```
book/
├── manuscript.md          ← canonical current source (Markdown)
├── README.md              ← this file
└── archive/
    ├── v1/                ← the prior packaged edition (.md, .docx, .pdf) — superseded in content by manuscript.md
    └── original/          ← the original unexpanded manuscript (.docx) and its direct Markdown conversion, predating MetaVibing's expansion

dist/                      ← packaged releases (.pdf, .docx) — not built yet; a release step, not a source
```

## Why this shape

Before this reorganization, `book/` held five different manuscript-shaped files at once (two packaged editions, a direct-conversion draft, and the original source docx), and the top-level README had to explain which one was "current" in prose. One canonical source removes the ambiguity structurally instead of by convention.

`archive/` exists so history isn't lost — the prior edition and the original manuscript are legitimate artifacts, just not the current one. They stay archived, not deleted, and are never edited after being moved here; if you need to know what v1 said, read `archive/v1/`, don't reconstruct it from memory.

## Building a release

`dist/` will hold generated `.pdf`/`.docx` packages once one is built from `manuscript.md` — this hasn't happened yet for the current manuscript. Do not hand-edit anything under `dist/`; regenerate it from `manuscript.md` instead.
