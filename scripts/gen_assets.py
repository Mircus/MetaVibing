"""
Generates the MetaVibing logo and the four release-minimum diagrams for the
Field Manual (dist/ PDF + DOCX build). Regenerate with:

    python scripts/gen_assets.py

Outputs to book/assets/. These are committed build assets, not the source
of truth — the source of truth is this script plus the palette below.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Wedge
from matplotlib.path import Path
import matplotlib.patches as mpatches
import pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "book" / "assets"
OUT.mkdir(parents=True, exist_ok=True)

INDIGO = "#4F46E5"
TEAL = "#0D9488"
VIOLET = "#7C3AED"
AMBER = "#D97706"
DARK = "#1F2937"
GRAY = "#6B7280"
LIGHT = "#F3F4F6"
WHITE = "#FFFFFF"

plt.rcParams["font.family"] = "DejaVu Sans"


def _box(ax, xy, w, h, text, fc=WHITE, ec=INDIGO, tc=DARK, fontsize=11, weight="bold", lw=1.8):
    x, y = xy
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        linewidth=lw, edgecolor=ec, facecolor=fc, zorder=2,
    ))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
             fontsize=fontsize, color=tc, weight=weight, zorder=3, wrap=True)


def _arrow(ax, xy1, xy2, color=TEAL, lw=2.2):
    ax.add_patch(FancyArrowPatch(
        xy1, xy2, arrowstyle="-|>", mutation_scale=16,
        linewidth=lw, color=color, zorder=1,
    ))


def _finish(fig, ax, path, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    fig.savefig(path, dpi=300, bbox_inches="tight", pad_inches=0.15,
                facecolor="white", transparent=False)
    plt.close(fig)
    print("wrote", path)


# ── Logo ──────────────────────────────────────────────────────────────────

def gen_logo():
    fig, ax = plt.subplots(figsize=(3, 3))
    r_out, r_in = 1.0, 0.62
    wedges = [
        (90, 210, INDIGO),
        (210, 330, TEAL),
        (330, 450, VIOLET),
    ]
    for t1, t2, color in wedges:
        ax.add_patch(Wedge((0, 0), r_out, t1, t2, width=r_out - r_in,
                            facecolor=color, edgecolor="white", linewidth=3))
    # Arrowhead at the end of the violet arc, pointing into the gap, to read
    # as a cycle/loop rather than a plain ring.
    ax.add_patch(FancyArrowPatch((0.02, -1.02), (0.55, -0.86),
                                  arrowstyle="-|>", mutation_scale=26,
                                  linewidth=0, color=VIOLET))
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(OUT / "logo.png", dpi=400, bbox_inches="tight",
                pad_inches=0.05, transparent=True)
    plt.close(fig)
    print("wrote", OUT / "logo.png")


# ── Diagram 1: The Core Loop ────────────────────────────────────────────────

def gen_core_loop():
    fig, ax = plt.subplots(figsize=(5.4, 8.6))
    steps = [
        "AI makes a mistake",
        "You correct it",
        "Correction repeats",
        "Extract the pattern",
        "Rule / Skill / Agent / Check",
        "Future work inherits\nthe correction",
    ]
    w, h, gap = 3.2, 0.9, 0.55
    x = 0.4
    n = len(steps)
    top = n * (h + gap)
    for i, label in enumerate(steps):
        y = top - (i + 1) * (h + gap) + gap
        last = i == n - 1
        _box(ax, (x, y), w, h, label,
             fc=VIOLET if last else WHITE,
             ec=VIOLET if last else INDIGO,
             tc=WHITE if last else DARK,
             fontsize=12.5)
        if i > 0:
            prev_y = top - i * (h + gap) + gap
            _arrow(ax, (x + w / 2, prev_y), (x + w / 2, y + h), color=TEAL, lw=2.6)
    _finish(fig, ax, OUT / "diagram-core-loop.png", (0, x * 2 + w), (0, top + gap))


# ── Diagram 2: The Meta-Stack (layered architecture) ───────────────────────

def gen_meta_stack():
    fig, ax = plt.subplots(figsize=(7.2, 5.6))
    layers = [
        ("CLAUDE.md", "recurring fact or convention", INDIGO),
        (".claude/rules/", "context-specific convention", INDIGO),
        ("Skill", "repeated procedure", TEAL),
        ("Subagent", "repeated specialist role", TEAL),
        ("Hook / Permission", "hard behavioral boundary", VIOLET),
        ("MCP", "missing external capability", VIOLET),
        ("Evaluation", "uncertain improvement", GRAY),
    ]
    w, h, gap = 6.0, 0.62, 0.18
    x = 0.6
    n = len(layers)
    top = n * (h + gap)
    for i, (name, desc, color) in enumerate(layers):
        y = top - (i + 1) * (h + gap) + gap
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015,rounding_size=0.03",
                                     linewidth=1.8, edgecolor=color, facecolor=WHITE, zorder=2))
        ax.text(x + 0.18, y + h / 2, name, ha="left", va="center",
                 fontsize=12.5, color=color, weight="bold", zorder=3)
        ax.text(x + w - 0.18, y + h / 2, desc, ha="right", va="center",
                 fontsize=10, color=GRAY, style="italic", zorder=3)
    _finish(fig, ax, OUT / "diagram-meta-stack.png", (0, x * 2 + w), (0, top + gap))


# ── Diagram 3: Three-Strikes / escalation ──────────────────────────────────

def gen_three_strikes():
    fig, ax = plt.subplots(figsize=(8.6, 3.4))
    steps = [
        ("1st occurrence", "Correct it", INDIGO, 0.85),
        ("2nd occurrence", "Diagnose it", TEAL, 1.1),
        ("3rd occurrence", "Externalize it", VIOLET, 1.4),
    ]
    x = 0.6
    w = 2.3
    gap = 0.9
    for i, (top_label, bottom_label, color, height) in enumerate(steps):
        bx = x + i * (w + gap)
        _box(ax, (bx, 0.3), w, height, f"{top_label}\n\n{bottom_label}",
             fc=color, ec=color, tc="white", fontsize=12)
        if i < len(steps) - 1:
            _arrow(ax, (bx + w, 0.3 + height / 2), (bx + w + gap, 0.3 + steps[i + 1][3] / 2),
                   color=GRAY, lw=2.4)
    ax.text(x, 2.05, "increasing permanence →", fontsize=11, color=GRAY, style="italic")
    _finish(fig, ax, OUT / "diagram-three-strikes.png",
            (0, x + 3 * w + 2 * gap + 0.6), (0, 2.3))


# ── Diagram 4: Friction → Artifact map ──────────────────────────────────

def gen_friction_artifact():
    fig, ax = plt.subplots(figsize=(8.6, 6.4))
    rows = [
        ("forgotten context", "CLAUDE.md", INDIGO),
        ("path-specific mistake", "Rule", INDIGO),
        ("repeated procedure", "Skill", TEAL),
        ("specialist judgment", "Agent", TEAL),
        ("objective invariant", "Checker", VIOLET),
        ("must-never-happen", "Hook", AMBER),
        ("external capability", "Tool / MCP", VIOLET),
    ]
    left_w, right_w, h, gap = 3.4, 2.4, 0.62, 0.2
    left_x, right_x = 0.4, 5.6
    n = len(rows)
    top = n * (h + gap)
    ax.text(left_x + left_w / 2, top + 0.35, "FRICTION", ha="center", fontsize=13,
            weight="bold", color=DARK)
    ax.text(right_x + right_w / 2, top + 0.35, "ARTIFACT", ha="center", fontsize=13,
            weight="bold", color=DARK)
    for i, (friction, artifact, color) in enumerate(rows):
        y = top - (i + 1) * (h + gap) + gap
        _box(ax, (left_x, y), left_w, h, friction, fc=LIGHT, ec=GRAY, tc=DARK, fontsize=10.5, weight="normal")
        _box(ax, (right_x, y), right_w, h, artifact, fc=color, ec=color, tc="white", fontsize=11.5)
        _arrow(ax, (left_x + left_w, y + h / 2), (right_x, y + h / 2), color=GRAY, lw=2.0)
    _finish(fig, ax, OUT / "diagram-friction-artifact.png",
            (0, right_x + right_w + 0.4), (0, top + 0.8))


if __name__ == "__main__":
    gen_logo()
    gen_core_loop()
    gen_meta_stack()
    gen_three_strikes()
    gen_friction_artifact()
    print("done")
