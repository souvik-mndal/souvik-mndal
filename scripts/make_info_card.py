
from pathlib import Path
import html
import os


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "info-card.svg"

STATIC = bool(os.environ.get("STATIC"))

# ------------------------------------------------------------
# Canvas
# ------------------------------------------------------------

WIDTH = 490
HEIGHT = 530

PAD = 24

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"

TEXT = "#c9d1d9"
MUTED = "#7d8590"
DIM = "#484f58"

GREEN = "#39d353"
BLUE = "#58a6ff"
PURPLE = "#bc8cff"
YELLOW = "#d29922"


# ------------------------------------------------------------
# Helper
# ------------------------------------------------------------

def esc(value):
    return html.escape(value)


parts = []

parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{WIDTH}" height="{HEIGHT}" '
    f'viewBox="0 0 {WIDTH} {HEIGHT}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">'
)

# ------------------------------------------------------------
# Background
# ------------------------------------------------------------

parts.append(
    f'''
    <defs>
      <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="{BG2}"/>
        <stop offset="1" stop-color="{BG}"/>
      </linearGradient>
    </defs>
    '''
)

parts.append(
    f'<rect width="{WIDTH}" height="{HEIGHT}" rx="12" fill="url(#bg)"/>'
)

parts.append(
    f'<rect x="0.5" y="0.5" width="{WIDTH-1}" height="{HEIGHT-1}" '
    f'rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>'
)


# ------------------------------------------------------------
# Terminal title bar
# ------------------------------------------------------------

parts.append(
    f'<line x1="0" y1="34" x2="{WIDTH}" y2="34" stroke="{FRAME}"/>'
)

for i, color in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(
        f'<circle cx="{22 + i * 16}" cy="17" r="5" fill="{color}"/>'
    )

parts.append(
    f'<text x="{WIDTH / 2}" y="21" fill="{MUTED}" '
    f'font-size="12" text-anchor="middle">'
    f'souvik@github: ~ $ neofetch'
    f'</text>'
)


# ------------------------------------------------------------
# Animation helper
# ------------------------------------------------------------

def animated_group(content, delay, x_shift=-10):

    if STATIC:
        return content

    return (
        f'<g opacity="0" transform="translate({x_shift} 0)">'
        f'{content}'
        f'<animate attributeName="opacity" '
        f'from="0" to="1" '
        f'begin="{delay:.2f}s" '
        f'dur="0.35s" '
        f'fill="freeze"/>'
        f'<animateTransform attributeName="transform" '
        f'type="translate" '
        f'from="{x_shift} 0" to="0 0" '
        f'begin="{delay:.2f}s" '
        f'dur="0.35s" '
        f'fill="freeze"/>'
        f'</g>'
    )


# ------------------------------------------------------------
# Identity
# ------------------------------------------------------------

identity = (
    f'<text x="{PAD}" y="76" fill="{GREEN}" '
    f'font-size="21" font-weight="700">'
    f'Souvik Mondal'
    f'</text>'
)

parts.append(animated_group(identity, 0.15))

subtitle = (
    f'<text x="{PAD}" y="99" fill="{MUTED}" font-size="11">'
    f'full-stack developer  ·  extension developer'
    f'</text>'
)

parts.append(animated_group(subtitle, 0.28))


# ------------------------------------------------------------
# Section helper
# ------------------------------------------------------------

def section_title(y, command, delay):
    content = (
        f'<text x="{PAD}" y="{y}" fill="{DIM}" font-size="11">'
        f'$ {esc(command)}'
        f'</text>'
    )

    return animated_group(content, delay)


# ------------------------------------------------------------
# Identity section
# ------------------------------------------------------------

parts.append(section_title(138, "cat identity", 0.45))

rows = [
    ("NOW", "Full Stack Developer · Extension Developer", GREEN),
    ("PREV", "Full Stack Developer · Research Intern", PURPLE),
    ("FOCUS", "Cybersecurity", BLUE),
]

start_y = 165

for i, (label, value, accent) in enumerate(rows):

    y = start_y + i * 31
    delay = 0.58 + i * 0.12

    content = (
        f'<text x="{PAD}" y="{y}" fill="{accent}" '
        f'font-size="11" font-weight="700">'
        f'{label}'
        f'</text>'
        f'<text x="92" y="{y}" fill="{TEXT}" font-size="11">'
        f'{esc(value)}'
        f'</text>'
    )

    parts.append(animated_group(content, delay))


# ------------------------------------------------------------
# Stack
# ------------------------------------------------------------

parts.append(section_title(280, "cat stack", 1.05))

stack_lines = [
    "C · C++ · Python · Java",
    "JavaScript (ES6+) · Manifest V3",
    "SQL · Bash · Linux Shell",
]

for i, line in enumerate(stack_lines):

    y = 309 + i * 25
    delay = 1.18 + i * 0.12

    content = (
        f'<text x="{PAD}" y="{y}" fill="{TEXT}" font-size="11">'
        f'{esc(line)}'
        f'</text>'
    )

    parts.append(animated_group(content, delay))


# ------------------------------------------------------------
# Interests
# ------------------------------------------------------------

parts.append(section_title(397, "cat interests", 1.62))

interest_content = (
    f'<text x="{PAD}" y="425" fill="{TEXT}" font-size="11">'
    f'<tspan fill="{GREEN}">●</tspan> Cybersecurity'
    f'<tspan dx="18" fill="{BLUE}">●</tspan> Research'
    f'<tspan dx="18" fill="{PURPLE}">●</tspan> Open Source'
    f'</text>'
)

parts.append(animated_group(interest_content, 1.75))


# ------------------------------------------------------------
# Bottom divider
# ------------------------------------------------------------

parts.append(
    f'<line x1="{PAD}" y1="454" x2="{WIDTH-PAD}" y2="454" '
    f'stroke="{FRAME}"/>'
)


# ------------------------------------------------------------
# Terminal prompt
# ------------------------------------------------------------

prompt = (
    f'<text x="{PAD}" y="483" fill="{GREEN}" font-size="11">'
    f'souvik@github:~$ '
    f'<tspan fill="{TEXT}">whoami</tspan>'
    f'</text>'
)

parts.append(animated_group(prompt, 2.05))


# Cursor
if STATIC:
    parts.append(
        f'<rect x="{PAD + 113}" y="472" width="7" height="14" '
        f'fill="{GREEN}" opacity="0.9"/>'
    )
else:
    parts.append(
        f'''
        <rect x="{PAD + 113}" y="472" width="7" height="14"
              fill="{GREEN}">
          <animate
            attributeName="opacity"
            values="1;1;0;0"
            keyTimes="0;0.5;0.51;1"
            dur="1s"
            repeatCount="indefinite"/>
        </rect>
        '''
    )


# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------

footer = (
    f'<text x="{PAD}" y="512" fill="{DIM}" font-size="9">'
    f'building things · learning security · shipping code'
    f'</text>'
)

parts.append(animated_group(footer, 2.2))


# ------------------------------------------------------------
# Finish
# ------------------------------------------------------------

parts.append("</svg>")

svg = "".join(parts)

OUT.write_text(svg, encoding="utf-8")

print(f"wrote {OUT}")
print(f"size: {WIDTH}x{HEIGHT}")

