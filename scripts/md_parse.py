"""
Small, purpose-built Markdown parser for book/manuscript.md -> a flat list
of typed blocks that build_manual.py renders into PDF (reportlab) and DOCX
(python-docx). Not a general Markdown parser -- it only supports the subset
manuscript.md actually uses: ATX headings, fenced code blocks, blockquotes,
pipe tables, bullet/numbered lists, horizontal rules, paragraphs, and the
two custom directives <!-- diagram: NAME --> and
<!-- callout:TYPE -->...<!-- /callout -->.
"""
import re

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
FENCE_RE = re.compile(r"^```(\w*)\s*$")
TABLE_ROW_RE = re.compile(r"^\|(.+)\|\s*$")
TABLE_SEP_RE = re.compile(r"^\|[\s:|-]+\|\s*$")
UL_RE = re.compile(r"^(\s*)[-*]\s+(.*)$")
OL_RE = re.compile(r"^(\s*)\d+\.\s+(.*)$")
DIAGRAM_RE = re.compile(r"^<!--\s*diagram:\s*([\w-]+)\s*-->\s*$")
CALLOUT_START_RE = re.compile(r"^<!--\s*callout:(\w+)\s*-->\s*$")
CALLOUT_END_RE = re.compile(r"^<!--\s*/callout\s*-->\s*$")


def parse(text: str) -> list:
    lines = text.split("\n")
    blocks, _ = _parse_lines(lines, 0, len(lines), stop_at_callout_end=False)
    return blocks


def _parse_lines(lines, i, n, stop_at_callout_end: bool):
    blocks = []
    para_buf = []

    def flush_para():
        if para_buf:
            joined = " ".join(l.strip() for l in para_buf if l.strip())
            if joined:
                blocks.append(("p", joined))
            para_buf.clear()

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if stop_at_callout_end and CALLOUT_END_RE.match(stripped):
            flush_para()
            return blocks, i + 1

        if not stripped:
            flush_para()
            i += 1
            continue

        m = CALLOUT_START_RE.match(stripped)
        if m:
            flush_para()
            ctype = m.group(1).lower()
            inner, i = _parse_lines(lines, i + 1, n, stop_at_callout_end=True)
            blocks.append(("callout", ctype, inner))
            continue

        m = DIAGRAM_RE.match(stripped)
        if m:
            flush_para()
            blocks.append(("diagram", m.group(1)))
            i += 1
            continue

        m = HEADING_RE.match(stripped)
        if m:
            flush_para()
            level = len(m.group(1))
            blocks.append((f"h{level}", m.group(2).strip()))
            i += 1
            continue

        if stripped in ("---", "***", "___"):
            flush_para()
            blocks.append(("hr",))
            i += 1
            continue

        m = FENCE_RE.match(stripped)
        if m:
            flush_para()
            lang = m.group(1)
            code_lines = []
            i += 1
            while i < n and not FENCE_RE.match(lines[i].strip()):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            blocks.append(("code", lang, "\n".join(code_lines)))
            continue

        if stripped.startswith(">"):
            flush_para()
            quote_lines = []
            while i < n and lines[i].strip().startswith(">"):
                quote_lines.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            blocks.append(("blockquote", "\n".join(quote_lines).strip()))
            continue

        if TABLE_ROW_RE.match(stripped):
            flush_para()
            table_lines = []
            while i < n and TABLE_ROW_RE.match(lines[i].strip()):
                table_lines.append(lines[i].strip())
                i += 1
            rows = [
                [c.strip() for c in TABLE_ROW_RE.match(l).group(1).split("|")]
                for l in table_lines
                if not TABLE_SEP_RE.match(l)
            ]
            if rows:
                blocks.append(("table", rows[0], rows[1:]))
            continue

        m = UL_RE.match(line)
        if m and not OL_RE.match(line):
            flush_para()
            items = []
            while i < n:
                mm = UL_RE.match(lines[i])
                if not mm:
                    break
                items.append(mm.group(2))
                i += 1
            blocks.append(("ul", items))
            continue

        m = OL_RE.match(line)
        if m:
            flush_para()
            items = []
            while i < n:
                mm = OL_RE.match(lines[i])
                if not mm:
                    break
                items.append(mm.group(2))
                i += 1
            blocks.append(("ol", items))
            continue

        para_buf.append(line)
        i += 1

    flush_para()
    return blocks, i


# ── Inline markdown -> reportlab-mini-HTML / plain runs ────────────────────

_INLINE_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def inline_to_reportlab(text: str) -> str:
    """Convert **bold**, *italic*, `code`, [text](url) into reportlab's
    Paragraph mini-HTML. Escapes real angle brackets/ampersands first."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = _LINK.sub(r'<link href="\2" color="#4F46E5">\1</link>', text)
    text = _INLINE_CODE.sub(r'<font face="Courier" color="#7C3AED">\1</font>', text)
    text = _BOLD.sub(r"<b>\1</b>", text)
    text = _ITALIC.sub(r"<i>\1</i>", text)
    return text


def strip_inline(text: str) -> str:
    """Plain-text version of inline markdown, for DOCX runs (styled separately)."""
    text = _LINK.sub(r"\1", text)
    text = _INLINE_CODE.sub(r"\1", text)
    text = _BOLD.sub(r"\1", text)
    text = _ITALIC.sub(r"\1", text)
    return text
