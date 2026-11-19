#!/usr/bin/env python3
"""Genera los encabezados y tarjetas SVG del README de perfil.

Uso:  python3 tools/make_cards.py
Para agregar un proyecto nuevo, añade una llamada a card(...) en la sección
PROYECTOS y vuelve a ejecutar el script.  Los SVG se guardan en ../assets/.
"""
import html
import os
import textwrap

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)

MONO = "'JetBrains Mono','Fira Code',Consolas,'Courier New',monospace"
SANS = "'Segoe UI',Roboto,Helvetica,Arial,sans-serif"

CYAN, VIOLET, GREEN = "#22d3ee", "#a78bfa", "#34d399"


def esc(s):
    return html.escape(s, quote=True)


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


def header(name, text, accent=CYAN, w=830, h=54):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(text)}">
<defs>
  <linearGradient id="tx" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="{accent}"/>
  </linearGradient>
  <linearGradient id="ln" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{accent}" stop-opacity="0.95"/>
    <stop offset="0.6" stop-color="#8b5cf6" stop-opacity="0.45"/>
    <stop offset="1" stop-color="#8b5cf6" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect x="0" y="8" width="4" height="26" rx="2" fill="{accent}"/>
<text x="16" y="29" font-family="{MONO}" font-size="21" font-weight="700" letter-spacing="2">
  <tspan fill="{accent}">//</tspan><tspan fill="url(#tx)"> {esc(text.upper())}</tspan>
</text>
<rect x="0" y="45" width="{w}" height="2" rx="1" fill="url(#ln)"/>
<circle cy="46" r="3.5" fill="{accent}">
  <animate attributeName="cx" values="0;{w}" dur="4s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0;1;1;0" dur="4s" repeatCount="indefinite"/>
</circle>
</svg>
"""
    save(name, svg)


def card(name, label, title, desc, chips=(), accent=CYAN, w=270, h=200,
         wrap=29, dashed=False):
    lines = textwrap.wrap(desc, wrap)[:4]
    dash = ' stroke-dasharray="7 6"' if dashed else ""
    parts = []
    for i, ln in enumerate(lines):
        parts.append(
            f'<text x="20" y="{96 + i * 20}" font-family="{SANS}" font-size="14" '
            f'fill="#9fb0c8">{esc(ln)}</text>'
        )
    desc_svg = "\n".join(parts)

    chip_svg, x = [], 20
    for c in chips:
        cw = len(c) * 7.4 + 20
        chip_svg.append(
            f'<rect x="{x}" y="{h - 40}" width="{cw:.0f}" height="25" rx="12.5" '
            f'fill="{accent}" fill-opacity="0.12" stroke="{accent}" stroke-opacity="0.55"/>'
            f'<text x="{x + cw / 2:.0f}" y="{h - 23}" text-anchor="middle" '
            f'font-family="{MONO}" font-size="12" fill="{accent}">{esc(c)}</text>'
        )
        x += cw + 8
    chip_svg = "\n".join(chip_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
<defs>
  <linearGradient id="bd" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="#8b5cf6"/>
  </linearGradient>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#101935"/><stop offset="1" stop-color="#080c18"/>
  </linearGradient>
  <pattern id="grid" width="18" height="18" patternUnits="userSpaceOnUse">
    <path d="M18 0H0V18" fill="none" stroke="#ffffff" stroke-opacity="0.045"/>
  </pattern>
  <linearGradient id="scan" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{accent}" stop-opacity="0"/>
    <stop offset="0.5" stop-color="{accent}"/>
    <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="clip"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14"/></clipPath>
</defs>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="url(#bg)"/>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="url(#grid)"/>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="none" stroke="url(#bd)" stroke-width="1.5"{dash}/>
<g clip-path="url(#clip)">
  <rect x="-90" y="1" width="90" height="2.5" fill="url(#scan)">
    <animate attributeName="x" from="-90" to="{w}" dur="3.6s" repeatCount="indefinite"/>
  </rect>
</g>
<path d="M{w - 26} {h - 12} H{w - 12} V{h - 26}" fill="none" stroke="{accent}" stroke-opacity="0.7" stroke-width="1.5" stroke-linecap="round"/>
<circle cx="{w - 22}" cy="28" r="3.5" fill="{accent}">
  <animate attributeName="opacity" values="1;0.25;1" dur="2s" repeatCount="indefinite"/>
</circle>
<text x="20" y="32" font-family="{MONO}" font-size="11.5" letter-spacing="1.4" fill="{accent}">{esc(label.upper())}</text>
<text x="20" y="66" font-family="{SANS}" font-size="18" font-weight="700" fill="#f1f5f9">{esc(title)}</text>
{desc_svg}
{chip_svg}
</svg>
"""
    save(name, svg)


def panel(name, paragraphs, accent=CYAN, w=830, size=18, wrap=76, lh=29, gap=14):
    """Panel grande de texto (para 'Sobre mí')."""
    blocks = [textwrap.wrap(p, wrap) for p in paragraphs]
    n = sum(len(b) for b in blocks)
    h = 44 + n * lh + gap * (len(blocks) - 1)
    y, out = 44, []
    for b in blocks:
        for ln in b:
            out.append(f'<text x="28" y="{y}" font-family="{SANS}" font-size="{size}" fill="#d6e0ee">{esc(ln)}</text>')
            y += lh
        y += gap
    body = "\n".join(out)
    save(name, f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(' '.join(paragraphs))}">
<defs>
  <linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#101935"/><stop offset="1" stop-color="#080c18"/></linearGradient>
  <pattern id="grid" width="18" height="18" patternUnits="userSpaceOnUse"><path d="M18 0H0V18" fill="none" stroke="#ffffff" stroke-opacity="0.045"/></pattern>
</defs>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="url(#bg)"/>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="url(#grid)"/>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="none" stroke="url(#bd)" stroke-width="1.5"/>
<rect x="0" y="22" width="4" height="{h-44}" rx="2" fill="{accent}"/>
<path d="M{w-26} {h-12} H{w-12} V{h-26}" fill="none" stroke="{accent}" stroke-opacity="0.7" stroke-width="1.5" stroke-linecap="round"/>
{body}
</svg>
""")


def tagline(name, title, body=None, accent=CYAN, w=830, wrap=74):
    """Frase destacada con barra de color (título grande + texto)."""
    out, y = [], 30
    if title:
        out.append(f'<text x="20" y="{y}" font-family="{SANS}" font-size="22" font-weight="700" fill="#f1f5f9">{esc(title)}</text>')
        y += 30
    if body:
        for ln in textwrap.wrap(body, wrap):
            out.append(f'<text x="20" y="{y}" font-family="{SANS}" font-size="18" fill="#a9b8cf">{esc(ln)}</text>')
            y += 27
    h = y - 2
    save(name, f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc((title or '') + ' ' + (body or ''))}">
<rect x="0" y="6" width="4" height="{h-12}" rx="2" fill="{accent}"/>
{chr(10).join(out)}
</svg>
""")


def label(name, text, accent=CYAN, w=300, h=34):
    """Etiqueta de grupo (Lenguajes, Frontend, ...)."""
    save(name, f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(text)}">
<rect x="0" y="6" width="4" height="22" rx="2" fill="{accent}"/>
<text x="16" y="24" font-family="{MONO}" font-size="17" font-weight="700" letter-spacing="1.5" fill="{accent}">{esc(text.upper())}</text>
</svg>
""")


# ───────────────────────── ENCABEZADOS ─────────────────────────
header("hdr-sobre-mi.svg", "Sobre mí", CYAN)
header("hdr-stack.svg", "Stack", CYAN)
header("hdr-personales.svg", "Proyectos personales", CYAN)
header("hdr-universitarios.svg", "Proyectos universitarios", VIOLET)
header("hdr-formacion.svg", "Formación y certificaciones", GREEN)
header("hdr-github.svg", "GitHub", VIOLET)
header("hdr-contacto.svg", "Contacto", CYAN)

# Textos grandes
panel("about.svg", [
    "Soy estudiante de cierre de Ingeniería en Ciencias y Sistemas (USAC). Desarrollo aplicaciones web de punta a punta: interfaces modernas y responsivas en el frontend, y módulos de software y bases de datos SQL en el backend. También despliego proyectos con Docker en servidores Linux y trabajo en equipo con Git Flow, pull requests y code reviews.",
    "Me gusta aprender tecnologías nuevas y adaptarme a distintos entornos. Estoy abierto a puestos donde pueda aportar valor, ya sea de desarrollo, backend o infraestructura.",
])
tagline("tag-personales.svg", "Ideas que se convierten en código.",
        "Lo que construyo por pasión, un proyecto a la vez: cada lanzamiento nuevo aterriza aquí.", CYAN)
tagline("tag-universitarios.svg", None,
        "Trabajos realizados durante mi carrera en la Universidad de San Carlos de Guatemala.", VIOLET)
label("lbl-lenguajes.svg", "Lenguajes")
label("lbl-frontend.svg", "Frontend")
label("lbl-backend.svg", "Backend y bases de datos")
label("lbl-devops.svg", "DevOps, nube y herramientas")

# ───────────────────────── PROYECTOS ─────────────────────────
# Personales (agrega aquí los nuevos)
card("card-personal-next.svg", "Proyecto personal", "Próximamente",
     "Mi primer proyecto personal está en construcción.",
     ["EN DESARROLLO"], CYAN, dashed=True)

# Universitarios
card("card-compi2-fase1.svg", "Compiladores 2 · USAC", "Compi2_Fase1",
     "Primera fase del proyecto de compiladores.",
     ["JavaScript"], VIOLET)
card("card-fortranpeg-f2.svg", "Compiladores 2 · USAC", "G22_Fase2_Fortranpeg",
     "Generador de parsers para Fortran con PEG y analizador descendente "
     "recursivo (fork del curso).",
     ["JavaScript", "PEG", "Fortran"], VIOLET)
card("card-fortranpeg-f3.svg", "Compiladores 2 · USAC", "G22_Fase3_FortranPEG",
     "Tercera fase del generador de parsers FortranPEG.",
     ["JavaScript", "PEG", "Fortran"], VIOLET)

# ───────────────────────── FORMACIÓN ─────────────────────────
card("card-edu-usac.svg", "Formación · USAC", "Ciencias y Sistemas",
     "Cierre de pensum. Software Avanzado, Bases de Datos 1 y 2, Redes 1 y 2, Análisis y Diseño.",
     [], GREEN)
card("card-edu-aws.svg", "Certificación · AWS", "AWS Academy Graduate",
     "Machine Learning Foundations (Training Badge), Amazon Web Services.",
     ["AWS", "ML"], GREEN)
card("card-edu-cpp.svg", "Curso profesional", "C++",
     "Curso profesional de C++.",
     ["C++"], GREEN)
print("SVG generados en", os.path.abspath(OUT))
