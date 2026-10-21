"""Gera os SVGs do perfil (claro e escuro) em profile/assets."""
import sys
from pathlib import Path
from xml.sax.saxutils import escape as esc

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

SANS = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Inter, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'SF Mono', SFMono-Regular, ui-monospace, Menlo, Consolas, 'Liberation Mono', monospace"

TEMAS = {
    "dark": dict(bg="#0b0b0d", card="#131316", line="#26262b", text="#f5f5f7", muted="#a1a1a6",
                 faint="#6e6e73", accent="#2997ff", accent2="#5ac8fa", tint="#0b2540", ok="#30d158",
                 glow=0.42, term="#0f0f12", bar="#1c1c20"),
    "light": dict(bg="#fbfbfd", card="#ffffff", line="#e3e3e8", text="#1d1d1f", muted="#6e6e73",
                  faint="#a1a1a6", accent="#0071e3", accent2="#2fb4f5", tint="#e8f2fd", ok="#1fa246",
                  glow=0.20, term="#ffffff", bar="#f2f2f5"),
}


def salvar(nome, svg):
    (OUT / nome).write_text(svg.strip() + "\n", encoding="utf-8")


# ---------------------------------------------------------------- hero
def hero(t, c):
    W, H = 1280, 420
    # trilhas do circuito: saem do chip e terminam num rótulo
    trilhas = [
        ("M 905 175 H 860 L 830 145 H 790", 760, 145, "firmware", "end"),
        ("M 905 245 H 850 L 815 280 H 790", 760, 280, "sensores", "end"),
        ("M 1055 175 H 1100 L 1130 145 H 1170", 1200, 145, "web", "start"),
        ("M 1055 245 H 1110 L 1145 280 H 1170", 1200, 280, "dados", "start"),
        ("M 980 135 V 95 L 1010 65 H 1040", 1062, 65, "gente", "start"),
    ]
    paths, pulsos, rotulos = [], [], []
    for i, (d, lx, ly, txt, anc) in enumerate(trilhas):
        paths.append(f'<path d="{d}" class="trilha"/>')
        pulsos.append(f'<path d="{d}" class="pulso" style="animation-delay:{i * 0.7:.1f}s"/>')
        ex_x = float(d.split()[-1])
        rotulos.append(
            f'<circle cx="{ex_x}" cy="{ly}" r="4" class="no"/>'
            f'<text x="{lx}" y="{ly + 5}" text-anchor="{anc}" class="rot">{txt}</text>')
    pinos = "".join(
        f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" class="pino"/>'
        for x in range(935, 1030, 18) for (y1, y2) in ((135, 127), (285, 293)))
    return f'''
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Willian Rupert — Do silício à sala de aula">
<defs>
  <radialGradient id="glow" cx="78%" cy="95%" r="60%">
    <stop offset="0" stop-color="{c['accent']}" stop-opacity="{c['glow']}"/>
    <stop offset="1" stop-color="{c['accent']}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="grad" x1="0" x2="1">
    <stop offset="0" stop-color="{c['accent']}"/><stop offset="1" stop-color="{c['accent2']}"/>
  </linearGradient>
  <pattern id="pontos" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.1" fill="{c['faint']}"/>
  </pattern>
  <linearGradient id="fade" x1="0" x2="1"><stop offset="0.45" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity="0.55"/></linearGradient>
  <mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
  <clipPath id="borda"><rect width="{W}" height="{H}" rx="28"/></clipPath>
</defs>
<style>
  .t{{font-family:{SANS};}}
  .eyebrow{{font-size:14px;letter-spacing:3.2px;font-weight:600;fill:{c['accent']}}}
  .nome{{font-size:76px;font-weight:650;letter-spacing:-2.4px;fill:{c['text']}}}
  .lema{{font-size:32px;font-weight:600;letter-spacing:-0.6px;fill:url(#grad)}}
  .corpo{{font-size:18px;fill:{c['muted']}}}
  .entra{{animation:entra .9s cubic-bezier(.2,.7,.2,1) backwards}}
  @keyframes entra{{from{{opacity:0;transform:translateY(14px)}}}}
  .trilha{{fill:none;stroke:{c['line']};stroke-width:2}}
  .pulso{{fill:none;stroke:{c['accent']};stroke-width:2.4;stroke-linecap:round;stroke-dasharray:22 400;stroke-dashoffset:22;animation:corre 3.5s linear infinite}}
  @keyframes corre{{0%{{stroke-dashoffset:22;opacity:0}}8%{{opacity:1}}70%{{opacity:1}}100%{{stroke-dashoffset:-260;opacity:0}}}}
  .no{{fill:{c['bg']};stroke:{c['accent']};stroke-width:2}}
  .rot{{font-family:{MONO};font-size:13px;fill:{c['muted']}}}
  .chip{{fill:{c['card']};stroke:{c['line']};stroke-width:2}}
  .pino{{stroke:{c['faint']};stroke-width:3;stroke-linecap:round}}
  .chiptxt{{font-family:{MONO};font-size:14px;font-weight:600;fill:{c['text']};letter-spacing:1px}}
  .led{{fill:{c['ok']};animation:pisca 2.4s ease-in-out infinite}}
  @keyframes pisca{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
  .respira{{animation:respira 7s ease-in-out infinite}}
  @keyframes respira{{0%,100%{{opacity:.75}}50%{{opacity:1}}}}
  @media (prefers-reduced-motion: reduce){{*{{animation:none!important;opacity:1!important}}}}
</style>
<g clip-path="url(#borda)">
  <rect width="{W}" height="{H}" fill="{c['bg']}"/>
  <rect width="{W}" height="{H}" fill="url(#glow)" class="respira"/>
  <rect width="{W}" height="{H}" fill="url(#pontos)" mask="url(#m)" opacity=".5"/>
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="27" fill="none" stroke="{c['line']}" stroke-width="2"/>

<g class="t">
  <text x="72" y="118" class="eyebrow entra" style="animation-delay:.05s">CIÊNCIA DA COMPUTAÇÃO · CIn-UFPE · RECIFE</text>
  <text x="68" y="198" class="nome entra" style="animation-delay:.15s">Willian Rupert</text>
  <text x="72" y="252" class="lema entra" style="animation-delay:.3s">Do silício a quem usa.</text>
  <text class="corpo entra" style="animation-delay:.45s">
    <tspan x="72" y="304">Firmware, apps e dados para coisas que precisam</tspan>
    <tspan x="72" y="331">funcionar fora do laboratório: numa sala de aula,</tspan>
    <tspan x="72" y="358">numa oficina, na porta de casa.</tspan>
  </text>
</g>

<g class="entra" style="animation-delay:.6s">
  {''.join(paths)}
  {''.join(pulsos)}
  {''.join(rotulos)}
  {pinos}
  <rect x="905" y="135" width="150" height="150" rx="18" class="chip"/>
  <rect x="925" y="155" width="110" height="110" rx="10" fill="none" stroke="{c['line']}" stroke-dasharray="3 5"/>
  <text x="980" y="214" text-anchor="middle" class="chiptxt">ESP32</text>
  <text x="980" y="236" text-anchor="middle" class="rot" style="font-size:11px">S3 · C3</text>
  <circle cx="1037" cy="153" r="4" class="led"/>
</g>
</svg>'''


# ---------------------------------------------------------------- terminal
def terminal(t, c):
    W, H = 1280, 400
    CH = 9.75  # largura de um caractere em 16.25px mono
    x0, y0, lh = 48, 104, 31
    linhas = [
        ("cmd", "whoami", 0.5, 0.5),
        ("out", [("Willian Rupert", c["text"]), (" · Ciência da Computação, CIn-UFPE · Recife", c["muted"])], 1.2, 0),
        ("cmd", "ls ~/em-producao", 1.9, 0.8),
        ("out", [("adsum/    portaria/    rlight-pendant/    caixa-dagua/", c["accent"])], 2.9, 0),
        ("cmd", "cat agora.txt", 3.6, 0.7),
        ("out", [("→ ", c["accent"]), ("levando uma CNC de 12 anos do Mach3 para o FluidNC", c["text"])], 4.5, 0),
        ("out", [("→ ", c["accent"]), ("prevendo inadimplência com dados reais, em Aprendizagem de Máquina", c["text"])], 4.85, 0),
        ("out", [("→ ", c["accent"]), ("roteamento inter-VLAN para os laboratórios do CIn", c["text"])], 5.2, 0),
        ("fim", "", 5.7, 0),
    ]
    corpo, quadros = [], []
    for i, (tipo, conteudo, ini, dur) in enumerate(linhas):
        y = y0 + i * lh
        if tipo == "cmd":
            n = len(conteudo)
            larg = n * CH + 4
            quadros.append(f"@keyframes d{i}{{from{{transform:translateX(0)}}to{{transform:translateX({larg:.0f}px)}}}}")
            corpo.append(
                f'<g class="ap" style="animation-delay:{ini - 0.05:.2f}s">'
                f'<text x="{x0}" y="{y}" class="m" fill="{c["ok"]}">❯</text>'
                f'<text x="{x0 + 26}" y="{y}" class="m" fill="{c["text"]}">{esc(conteudo)}</text>'
                f'<rect x="{x0 + 24}" y="{y - 20}" width="{larg + 4}" height="28" fill="{c["term"]}" '
                f'transform="translate({larg:.0f} 0)" style="animation:d{i} {dur}s steps({n}) {ini}s both"/>'
                f'</g>')
        elif tipo == "out":
            spans = "".join(f'<tspan fill="{cor}">{esc(s)}</tspan>' for s, cor in conteudo)
            corpo.append(f'<text x="{x0}" y="{y}" class="m ap" style="animation-delay:{ini}s">{spans}</text>')
        else:
            corpo.append(
                f'<g class="ap" style="animation-delay:{ini}s"><text x="{x0}" y="{y}" class="m" fill="{c["ok"]}">❯</text>'
                f'<rect x="{x0 + 24}" y="{y - 17}" width="10" height="21" fill="{c["accent"]}" class="cursor"/></g>')
    return f'''
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal: quem sou, o que está em produção e no que estou trabalhando agora">
<style>
  .m{{font-family:{MONO};font-size:16.25px;white-space:pre}}
  .ap{{animation:ap .01s linear backwards}}
  @keyframes ap{{from{{opacity:0}}to{{opacity:0}}}}
  {''.join(quadros)}
  .cursor{{animation:cur 1.1s steps(1) infinite}}
  @keyframes cur{{50%{{opacity:0}}}}
  .tt{{font-family:{SANS};font-size:13px;fill:{c['muted']}}}
  @media (prefers-reduced-motion: reduce){{.ap{{animation:none;opacity:1}}rect[style]{{display:none}}}}
</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="{c['term']}" stroke="{c['line']}" stroke-width="2"/>
<path d="M1 19 a18 18 0 0 1 18 -18 H{W - 19} a18 18 0 0 1 18 18 V46 H1 Z" fill="{c['bar']}"/>
<line x1="1" y1="46" x2="{W - 1}" y2="46" stroke="{c['line']}" stroke-width="1.5"/>
<circle cx="28" cy="24" r="6.5" fill="#ff5f57"/><circle cx="50" cy="24" r="6.5" fill="#febc2e"/><circle cx="72" cy="24" r="6.5" fill="#28c840"/>
<text x="{W / 2}" y="29" text-anchor="middle" class="tt">willian@rlight — zsh</text>
{''.join(corpo)}
</svg>'''


# ---------------------------------------------------------------- cartões
def glifo(nome, c):
    a = c["accent"]
    s = f'fill="none" stroke="{a}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"'
    if nome == "adsum":  # crachá encostando no leitor, com onda
        return f'''
<g {s}>
  <rect x="30" y="22" width="30" height="40" rx="5"/>
  <path d="M40 22 v-6 h10 v6"/>
  <circle cx="45" cy="36" r="5"/>
  <path d="M37 50 h16 M39 55 h12"/>
</g>
<g fill="none" stroke="{a}" stroke-width="2.2" stroke-linecap="round">
  <path d="M18 34 a12 12 0 0 0 0 16" class="onda" style="animation-delay:0s"/>
  <path d="M12 29 a19 19 0 0 0 0 26" class="onda" style="animation-delay:.25s"/>
</g>'''
    if nome == "pendant":  # celular com mira que passeia
        return f'''
<g {s}>
  <rect x="24" y="12" width="36" height="58" rx="7"/>
  <path d="M37 18 h10"/>
</g>
<g class="mira">
  <g {s.replace('2.6', '2')}>
    <circle cx="42" cy="42" r="7"/>
    <path d="M42 31 v6 M42 47 v6 M31 42 h6 M47 42 h6"/>
  </g>
</g>'''
    if nome == "portaria":  # caixa descendo até a balança
        return f'''
<g class="cai">
  <g {s}>
    <path d="M42 14 l16 8 v16 l-16 8 l-16 -8 v-16 z"/>
    <path d="M26 22 l16 8 l16 -8 M42 30 v16"/>
  </g>
</g>
<g {s}><path d="M18 62 h48 M24 62 v6 M60 62 v6"/></g>
<circle cx="64" cy="18" r="3.5" fill="{c['ok']}" class="led"/>'''
    if nome == "caixa":  # caixa d'água com onda
        return f'''
<defs><clipPath id="tq"><rect x="22" y="18" width="40" height="48" rx="7"/></clipPath></defs>
<g clip-path="url(#tq)">
  <g class="agua">
    <path d="M-20 42 q8 -5 16 0 t16 0 t16 0 t16 0 t16 0 t16 0 t16 0 V80 H-20 Z" fill="{a}" opacity=".9"/>
  </g>
</g>
<g {s}><rect x="22" y="18" width="40" height="48" rx="7"/><path d="M34 12 h16"/></g>'''
    return ""


def cartao(nome, titulo, linhas, rodape, status, c):
    W, H = 640, 340
    texto = "".join(f'<tspan x="40" y="{196 + i * 26}">{esc(l)}</tspan>' for i, l in enumerate(linhas))
    pill_w = 22 + len(status) * 7.6
    return f'''
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(titulo)}">
<style>
  .s{{font-family:{SANS}}}
  .m{{font-family:{MONO}}}
  .onda{{animation:onda 2.2s ease-out infinite}}
  @keyframes onda{{0%{{opacity:0}}20%{{opacity:1}}100%{{opacity:0;transform:translateX(-6px)}}}}
  .mira{{animation:mira 6s ease-in-out infinite}}
  @keyframes mira{{0%,100%{{transform:translate(0,0)}}25%{{transform:translate(6px,-10px)}}50%{{transform:translate(-5px,-4px)}}75%{{transform:translate(4px,12px)}}}}
  .cai{{animation:cai 3.2s cubic-bezier(.3,.6,.3,1) infinite}}
  @keyframes cai{{0%{{transform:translateY(-6px);opacity:0}}20%{{opacity:1}}60%,85%{{transform:translateY(12px);opacity:1}}100%{{transform:translateY(12px);opacity:0}}}}
  .agua{{animation:agua 2.6s linear infinite, nivel 9s ease-in-out infinite}}
  @keyframes agua{{to{{transform:translateX(-32px)}}}}
  @keyframes nivel{{0%,100%{{translate:0 6px}}50%{{translate:0 -10px}}}}
  .led,.dot{{animation:pisca 2.4s ease-in-out infinite}}
  @keyframes pisca{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
  @media (prefers-reduced-motion: reduce){{*{{animation:none!important;opacity:1!important}}}}
</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="24" fill="{c['card']}" stroke="{c['line']}" stroke-width="2"/>
<g transform="translate(40 36)">
  <rect width="84" height="84" rx="20" fill="{c['tint']}"/>
  {glifo(nome, c)}
</g>
<g transform="translate({W - 40 - pill_w} 44)">
  <rect width="{pill_w}" height="28" rx="14" fill="none" stroke="{c['line']}" stroke-width="1.5"/>
  <circle cx="15" cy="14" r="4" fill="{c['ok']}" class="dot"/>
  <text x="26" y="19" class="s" font-size="13" font-weight="500" fill="{c['muted']}">{esc(status)}</text>
</g>
<text x="40" y="162" class="s" font-size="30" font-weight="650" letter-spacing="-0.6" fill="{c['text']}">{esc(titulo)}</text>
<text class="s" font-size="18" fill="{c['muted']}">{texto}</text>
<line x1="40" y1="276" x2="{W - 40}" y2="276" stroke="{c['line']}" stroke-width="1.5"/>
<text x="40" y="306" class="m" font-size="14" fill="{c['faint']}">{esc(rodape)}</text>
<text x="{W - 40}" y="307" text-anchor="end" class="s" font-size="20" font-weight="600" fill="{c['accent']}">→</text>
</svg>'''


CARTOES = [
    ("adsum", "Adsum", ["Chamada por crachá, sem servidor, sem conta,", "sem login. A planilha sai pronta no fim da aula."],
     "PWA offline · React · TypeScript", "em uso no CIn"),
    ("pendant", "RLight Pendant", ["A sua CNC, ao vivo, na palma da mão: ver,", "mexer e confiar numa fresadora FluidNC."],
     "PWA · TypeScript estrito · 500+ testes", "na oficina"),
    ("portaria", "Portaria", ["Encomendas recebidas sem porteiro: o entregador", "digita um código, a casa faz o resto."],
     "ESP32-S3 · Python · FastAPI · Node", "em produção"),
    ("caixa", "Caixa d'água", ["Bombeamento que sobrevive a apagões, erro", "humano e sensor rompido. Um botão, um LED."],
     "ESP32 · ESPHome · Home Assistant", "em produção"),
]


# ---------------------------------------------------------------- rodapé
def rodape(t, c):
    W, H = 1280, 120
    return f'''
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="o simples é belo.">
<defs><linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="{c['line']}" stop-opacity="0"/><stop offset="1" stop-color="{c['line']}"/></linearGradient>
<linearGradient id="r" x1="1" x2="0"><stop offset="0" stop-color="{c['line']}" stop-opacity="0"/><stop offset="1" stop-color="{c['line']}"/></linearGradient></defs>
<rect x="240" y="59" width="290" height="2" fill="url(#l)"/>
<rect x="750" y="59" width="290" height="2" fill="url(#r)"/>
<text x="640" y="68" text-anchor="middle" font-family="{SANS}" font-size="22" font-style="italic" font-weight="500" letter-spacing="-0.2" fill="{c['muted']}">o simples é belo.</text>
</svg>'''


for t, c in TEMAS.items():
    salvar(f"hero-{t}.svg", hero(t, c))
    salvar(f"terminal-{t}.svg", terminal(t, c))
    salvar(f"rodape-{t}.svg", rodape(t, c))
print("ok", sorted(p.name for p in OUT.glob("*.svg")))


# ---------------------------------------------------------------- cartões de tema automático
# O GitHub não esconde mais imagens com #gh-dark-mode-only, e um <picture> dentro de
# um link perde o link. Então cada cartão é um arquivo só, que troca de cor por
# prefers-color-scheme dentro do próprio SVG.
import re

CHAVES = ["card", "line", "tint", "ok", "muted", "text", "faint", "accent", "bg"]


def tema_automatico(svg):
    def tag(m):
        t = m.group(0)
        vs = re.findall(r'\s(fill|stroke|stop-color)="(var\(--\w+\))"', t)
        if not vs:
            return t
        t = re.sub(r'\s(fill|stroke|stop-color)="var\(--\w+\)"', "", t)
        decl = ";".join(f"{k}:{v}" for k, v in vs)
        if ' style="' in t:
            return t.replace(' style="', f' style="{decl};', 1)
        fim = "/>" if t.endswith("/>") else ">"
        return t[: -len(fim)] + f' style="{decl}"' + fim
    svg = re.sub(r"<[a-zA-Z][^<>]*>", tag, svg)
    claro = ";".join(f"--{k}:{TEMAS['light'][k]}" for k in CHAVES)
    escuro = ";".join(f"--{k}:{TEMAS['dark'][k]}" for k in CHAVES)
    return svg.replace("<style>", f"<style>\n  :root{{{claro}}}\n  @media (prefers-color-scheme: dark){{:root{{{escuro}}}}}", 1)


VARS = {k: f"var(--{k})" for k in CHAVES}
for args in CARTOES:
    salvar(f"card-{args[0]}.svg", tema_automatico(cartao(*args, VARS)))
