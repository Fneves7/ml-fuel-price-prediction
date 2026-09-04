# -*- coding: utf-8 -*-
"""Constrói a apresentação HTML (deck de slides) com as figuras embutidas em base64."""
import base64, pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FIG = RAIZ / "figuras"
SAIDA = RAIZ / "apresentacao.html"

def img(nome):
    b = (FIG / nome).read_bytes()
    return "data:image/png;base64," + base64.b64encode(b).decode()

IMGS = {k: img(k+".png") for k in [
    "02_preco_vs_brent", "11_decomposicao_impostos", "09_importancias_classificacao",
    "13_regressao_delta", "15_comparacao_gradient_boosting", "16_validacao_tuning",
    "18_probabilidade"]}

# ---------- slides (HTML de cada um) ----------
def chart(src, alt):
    return f'<figure class="chart"><img src="{src}" alt="{alt}"></figure>'

slides = []

# 1 — TÍTULO
slides.append(('dark title', '''
<div class="t-wrap">
  <p class="eyebrow light">Projeto · Fundamentos de Inteligência Artificial</p>
  <h1>Prever os preços dos<br>combustíveis em Portugal</h1>
  <p class="lede">“Conseguimos prever se o preço de um combustível<br>sobe ou desce num determinado dia?”</p>
  <p class="byline"><strong>Francisco Neves</strong><span>Setembro de 2026</span></p>
</div>
<div class="orb orb-a"></div><div class="orb orb-b"></div>'''))

# 2 — O DESAFIO
slides.append(('light', '''
<header class="s-head"><p class="eyebrow">O desafio</p><h2>De uma pergunta simples a um problema de IA</h2></header>
<div class="cols">
  <div class="question">
    <p class="q">Conseguimos prever o aumento ou a descida do preço de um tipo de combustível num determinado dia?</p>
    <p class="q-cap">a pergunta de investigação</p>
  </div>
  <ul class="rows">
    <li><b>Tema do dia a dia</b><span>o preço que todos pagamos ao abastecer.</span></li>
    <li><b>Aprendizagem supervisionada</b><span>classificação (sobe/desce) e regressão.</span></li>
    <li><b>Ferramentas Python</b><span>pandas · scikit-learn · matplotlib · seaborn.</span></li>
  </ul>
</div>
<p class="concepts">Inteligência Artificial &nbsp;·&nbsp; Machine Learning &nbsp;·&nbsp; Aprendizagem supervisionada &nbsp;·&nbsp; Avaliação de modelos</p>'''))

# 3 — DADOS
slides.append(('light', '''
<header class="s-head"><p class="eyebrow">Seleção e enriquecimento do dataset</p><h2>Dos dados brutos aos dados que explicam</h2></header>
<div class="cols">
  <div class="stats">
    <div class="stat"><span class="big">45&thinsp;188</span><span class="lbl">registos diários</span></div>
    <div class="stat"><span class="big">8</span><span class="lbl">combustíveis</span></div>
    <div class="stat"><span class="big">2008–2026</span><span class="lbl">de cobertura</span></div>
    <div class="stat"><span class="big accentnum">3 → 47</span><span class="lbl">colunas (após enriquecer)</span></div>
    <p class="src">Fonte base: DGEG — preço médio diário</p>
  </div>
  <div class="panel">
    <p class="panel-h">O que juntámos — e porquê</p>
    <ul class="rows tight">
      <li><b>Petróleo Brent (€)</b><span>o principal driver internacional.</span></li>
      <li><b>Câmbio EUR/USD</b><span>o petróleo é cotado em dólares.</span></li>
      <li><b>ISP + IVA</b><span>metade do preço são impostos.</span></li>
      <li><b>Calendário + feriados</b><span>sazonalidade e dias sem atualização.</span></li>
      <li><b>Limpeza</b><span>133 zeros e 5 outliers tratados; encoding corrigido.</span></li>
    </ul>
  </div>
</div>'''))

# 4 — PREÇO vs PETRÓLEO
slides.append(('light chart-slide', f'''
<header class="s-head"><p class="eyebrow">Análise dos dados</p><h2>O preço segue o petróleo</h2></header>
<div class="cols wide-left">
  {chart(IMGS["02_preco_vs_brent"], "Preço do gasóleo vs Brent em euros")}
  <aside class="note">
    <span class="hero-num">0,72–0,91</span>
    <p class="hero-lbl">correlação preço ↔ Brent (€), por combustível</p>
    <p>Vê-se o <b>crash de 2020</b> (COVID) e o <b>pico de 2022</b> (guerra na Ucrânia) refletidos no preço à bomba.</p>
  </aside>
</div>'''))

# 5 — IMPOSTOS
slides.append(('light chart-slide', f'''
<header class="s-head"><p class="eyebrow">Análise dos dados</p><h2>Metade do que pagamos são impostos</h2></header>
<div class="cols wide-left">
  {chart(IMGS["11_decomposicao_impostos"], "Decomposição do preço em ISP, IVA e componente comercial")}
  <aside class="note">
    <span class="hero-num">≈ 51%</span>
    <p class="hero-lbl">do preço da gasolina são impostos (≈ 42% no gasóleo)</p>
    <p>O <b>corte do ISP em 2022</b> vê-se na descida da faixa laranja. As taxas foram confirmadas nos <b>PDFs oficiais do Diário da República</b>.</p>
  </aside>
</div>'''))

# 6 — MODELO DIREÇÃO
slides.append(('light chart-slide', f'''
<header class="s-head"><p class="eyebrow">Criação e avaliação do modelo</p><h2>Conseguimos prever a direção?</h2></header>
<div class="cols wide-left">
  {chart(IMGS["09_importancias_classificacao"], "Variáveis mais importantes do modelo")}
  <aside class="note">
    <div class="ladder">
      <div><span class="pct muted">61%</span><span>acaso (baseline)</span></div>
      <div><span class="pct primary">79%</span><span>Random Forest</span></div>
      <div><span class="pct accent">82%</span><span>XGBoost / LightGBM</span></div>
    </div>
    <p>Acerto na previsão <b>sobe/desce a 1 dia</b> — bem acima do acaso.</p>
  </aside>
</div>'''))

# 7 — LIÇÃO HONESTA
slides.append(('light chart-slide', f'''
<header class="s-head"><p class="eyebrow">Avaliação honesta</p><h2>Valor exato? Não. Variação e direção? Sim.</h2></header>
<div class="cols wide-left">
  {chart(IMGS["13_regressao_delta"], "Erro e acerto na direção da variação diária")}
  <aside class="note">
    <p class="callout bad"><b>R² = 0,999</b> na previsão do valor parece ótimo, mas é <b>enganador</b> — “amanhã ≈ hoje”.</p>
    <p class="callout good">Prever a <b>variação</b> já compensa: <b>+22%</b> melhor que o baseline e <b class="accent-ink">76%</b> de acerto no sentido.</p>
  </aside>
</div>'''))

# 8 — ALGORITMOS
slides.append(('light chart-slide', f'''
<header class="s-head"><p class="eyebrow">Comparação de algoritmos</p><h2>Não há um modelo melhor para tudo</h2></header>
<div class="cols wide-left">
  {chart(IMGS["15_comparacao_gradient_boosting"], "Gradient boosting vs Random Forest nas três tarefas")}
  <aside class="note">
    <ul class="rows tight">
      <li><b>1 dia</b><span>XGBoost / LightGBM ganham (0,82).</span></li>
      <li><b>Variação</b><span>Random Forest ganha claramente.</span></li>
      <li><b>7 dias</b><span>Random Forest ligeiramente melhor.</span></li>
    </ul>
    <p class="em">A escolha do algoritmo deve ser guiada pela tarefa — não pela moda.</p>
  </aside>
</div>'''))

# 8b — PANORAMA DOS 19 ALGORITMOS
slides.append(('light', '''
<header class="s-head"><p class="eyebrow">Amplitude do estudo · aprendizagem supervisionada</p><h2>Testámos 19 algoritmos em 4 famílias</h2></header>
<div class="fam-grid">
  <div class="fam"><span class="fam-h">Regressão · 5</span><span class="fam-list">linear simples/múltipla · polinomial · Ridge · Lasso</span><span class="fam-best neutral">o valor exato não compensa</span></div>
  <div class="fam"><span class="fam-h">Classificação · 5</span><span class="fam-list">logística · SVM linear/kernel · KNN · Naïve Bayes</span><span class="fam-best">melhor: KNN &nbsp;0,73</span></div>
  <div class="fam"><span class="fam-h">Séries temporais · 5</span><span class="fam-list">suavização · ARIMA · SARIMA · Prophet · LSTM</span><span class="fam-best neutral">≈ random walk (não bate o baseline)</span></div>
  <div class="fam win"><span class="fam-h">Métodos de conjunto · 4</span><span class="fam-list">árvore · Random Forest · XGBoost · CatBoost</span><span class="fam-best">melhor global: XGBoost &nbsp;0,82</span></div>
</div>
<p class="concepts">Guiados pelos meta-prompts de <b>prompts_opencode_ml/01_supervisionada</b> — o <b>gradient boosting</b> é o melhor para prever a direção.</p>'''))

# 9 — ROBUSTEZ
slides.append(('light chart-slide', f'''
<header class="s-head"><p class="eyebrow">Robustez e validação</p><h2>Resultados sólidos, sem exageros</h2></header>
<div class="cols wide-left">
  {chart(IMGS["16_validacao_tuning"], "Validação temporal e afinação")}
  <aside class="note">
    <span class="hero-num">≈ 0,79 <small>± 0,04</small></span>
    <p class="hero-lbl">em 5 janelas temporais (TimeSeriesSplit)</p>
    <p>A <b>afinação não melhorou</b> o resultado — sinal de honestidade: não “vendemos” ganhos que não existem.</p>
  </aside>
</div>'''))

# 9b — DA PREVISÃO À DECISÃO (B8 + B9)
slides.append(('light chart-slide', f'''
<header class="s-head"><p class="eyebrow">Da previsão à decisão</p><h2>Com confiança, quase não erra — e ajuda a poupar</h2></header>
<div class="cols wide-left">
  {chart(IMGS["18_probabilidade"], "Calibração e acerto por nível de confiança")}
  <aside class="note">
    <span class="hero-num">96%</span>
    <p class="hero-lbl">de acerto quando o modelo tem ≥ 90 % de confiança (cobre 38 % dos dias)</p>
    <p class="callout good"><b>Atesto ou espero?</b> Seguir o modelo capta <b>76 %</b> da poupança máxima possível; nos dias em que mandou esperar, o preço desceu mesmo <b class="accent-ink">67 %</b> das vezes.</p>
  </aside>
</div>'''))

# 10 — CONCLUSÃO
slides.append(('dark', '''
<header class="s-head"><h2 class="light-h">Conclusão</h2></header>
<ul class="concl">
  <li><b>Sim, prevemos a direção com utilidade.</b><span>79% a 1 dia e 69% a 7 dias — bem acima do acaso.</span></li>
  <li><b>O valor exato não compensa; a variação sim.</b><span>Prever a variação bate o baseline em +22% (76% de sentido).</span></li>
  <li><b>Petróleo e impostos explicam o preço.</b><span>O enriquecimento (Brent, câmbio, ISP/IVA) foi decisivo.</span></li>
</ul>
<p class="concepts light">IA &nbsp;·&nbsp; Machine Learning &nbsp;·&nbsp; Aprendizagem supervisionada &nbsp;·&nbsp; Avaliação de modelos</p>'''))

# 11 — OBRIGADO
slides.append(('dark end', '''
<div class="orb orb-c"></div>
<div class="end-wrap">
  <h1 class="thanks">Obrigado</h1>
  <p class="foot"><span class="k">Fontes</span> DGEG (preços) · FRED (Brent, EUR/USD) · Diário da República (ISP)</p>
  <p class="foot"><span class="k">Ferramentas</span> pandas · scikit-learn · XGBoost · LightGBM · matplotlib · seaborn</p>
  <p class="sig">Francisco Neves · Fundamentos de Inteligência Artificial</p>
</div>'''))

# ---------- montar HTML ----------
slides_html = "\n".join(
    f'<section class="slide {cls}" data-i="{i}">{body}</section>'
    for i, (cls, body) in enumerate(slides))
dots = "".join(f'<button class="dot" data-to="{i}" aria-label="Slide {i+1}"></button>'
               for i in range(len(slides)))
N = len(slides)

HTML = f'''<title>Previsão de Preços de Combustíveis</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Public+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@500;600&display=swap">
<style>
:root{{
  --bg:#E9F0F1; --slide:#FDFEFE; --ink:#16262E; --muted:#5E747D;
  --primary:#0E5A75; --accent:#C56A12; --accent-bright:#E8991F;
  --green:#2E7D6E; --red:#B4432B; --line:#E1E8EA; --card:#F2F7F8;
  --d-bg:#0B2E3D; --d-ink:#FFFFFF; --d-muted:#A7C0C8;
  --sans:"Public Sans",system-ui,sans-serif; --disp:"Archivo",var(--sans);
  --mono:"IBM Plex Mono",ui-monospace,monospace;
}}
*{{box-sizing:border-box}}
html,body{{margin:0}}
body{{background:var(--bg);color:var(--ink);font-family:var(--sans);
  min-height:100vh;display:flex;flex-direction:column;align-items:center;
  justify-content:center;padding:18px 18px 64px;gap:14px;}}
.deck{{width:min(96vw,1180px)}}
.stage{{position:relative;width:100%;aspect-ratio:16/9;border-radius:16px;
  overflow:hidden;box-shadow:0 18px 50px -20px rgba(11,46,61,.45),0 2px 8px rgba(11,46,61,.12);
  background:var(--slide);container-type:size;}}
.slide{{position:absolute;inset:0;padding:5.2cqw 5.6cqw;
  font-size:clamp(11px,2.02cqw,23px);opacity:0;visibility:hidden;
  transition:opacity .45s ease;display:flex;flex-direction:column;
  background:var(--slide);}}
@media (prefers-reduced-motion:reduce){{.slide{{transition:none}}}}
.slide.active{{opacity:1;visibility:visible}}
.slide.dark{{background:var(--d-bg);color:var(--d-ink)}}

/* headings */
.eyebrow{{font-family:var(--mono);font-size:.72em;letter-spacing:.14em;
  text-transform:uppercase;color:var(--accent);margin:0 0 .5em;font-weight:600}}
.eyebrow.light{{color:var(--accent-bright)}}
.s-head{{margin-bottom:.5em}}
.s-head h2{{font-family:var(--disp);font-weight:800;font-size:2.15em;margin:0;
  line-height:1.04;letter-spacing:-.015em;text-wrap:balance;color:var(--primary)}}
.slide.dark .s-head h2,.light-h{{color:var(--d-ink)!important}}

/* title slide */
.slide.title{{justify-content:center}}
.t-wrap{{position:relative;z-index:2;max-width:80%}}
h1{{font-family:var(--disp);font-weight:800;font-size:3.5em;line-height:1.02;
  letter-spacing:-.02em;margin:.15em 0 .5em;color:#fff;text-wrap:balance}}
.lede{{font-size:1.32em;line-height:1.4;color:#CFE0E6;margin:0 0 2em;font-weight:400}}
.byline{{font-family:var(--mono);font-size:.92em;color:#9FB8C0;display:flex;
  gap:.9em;align-items:center}}
.byline strong{{color:#fff}}
.byline span{{color:#87a3ac}}
.orb{{position:absolute;border-radius:50%;z-index:1;filter:blur(2px)}}
.orb-a{{right:-8cqw;bottom:-14cqw;width:42cqw;height:42cqw;
  background:radial-gradient(circle at 35% 35%,#12658a,#0b2e3d 70%);opacity:.85}}
.orb-b{{right:6cqw;bottom:2cqw;width:16cqw;height:16cqw;
  background:radial-gradient(circle at 40% 40%,var(--accent-bright),#a9640c);opacity:.55}}
.orb-c{{left:-12cqw;top:-12cqw;width:38cqw;height:38cqw;
  background:radial-gradient(circle at 60% 60%,#12658a,#0b2e3d 72%);opacity:.7}}

/* columns */
.cols{{flex:1;display:grid;grid-template-columns:1fr 1fr;gap:2.4em;align-items:center;min-height:0}}
.cols.wide-left{{grid-template-columns:1.62fr 1fr;gap:2em;align-items:center}}

/* question card */
.question{{background:var(--card);border:1px solid var(--line);border-radius:.7em;
  padding:1.3em 1.4em}}
.question .q{{font-family:var(--disp);font-weight:700;font-size:1.32em;line-height:1.24;
  color:var(--primary);margin:0}}
.q-cap{{font-size:.8em;color:var(--muted);font-style:italic;margin:.7em 0 0}}

/* row lists */
.rows{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:1.05em}}
.rows.tight{{gap:.82em}}
.rows li{{position:relative;padding-left:1.35em;line-height:1.32}}
.rows li::before{{content:"";position:absolute;left:0;top:.42em;width:.52em;height:.52em;
  border-radius:50%;background:var(--accent-bright)}}
.rows b{{color:var(--ink);font-weight:600}}
.rows span{{color:var(--muted)}}
.rows b::after{{content:" — "}}

.concepts{{margin:0;text-align:center;font-family:var(--mono);font-size:.82em;
  color:var(--primary);background:var(--card);border-radius:.5em;padding:.85em 1em;
  font-weight:600;letter-spacing:.01em}}
.concepts.light{{background:rgba(255,255,255,.06);color:#CFE0E6}}
.concepts b{{color:var(--accent)}}

/* família de algoritmos (grelha 2x2) */
.fam-grid{{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;
  gap:1.1em;min-height:0;margin-bottom:.9em}}
.fam{{background:var(--card);border:1px solid var(--line);border-radius:.6em;
  padding:1.05em 1.15em;display:flex;flex-direction:column;gap:.4em;justify-content:center}}
.fam.win{{background:rgba(232,153,31,.12);border-color:var(--accent-bright)}}
.fam-h{{font-family:var(--disp);font-weight:700;font-size:1.18em;color:var(--primary)}}
.fam.win .fam-h{{color:#9a5a08}}
.fam-list{{font-size:.86em;color:var(--muted);line-height:1.3}}
.fam-best{{font-family:var(--mono);font-size:.82em;font-weight:600;color:var(--accent);
  margin-top:.15em}}
.fam-best.neutral{{color:var(--muted);font-weight:500}}

/* stats */
.stats{{display:grid;grid-template-columns:1fr 1fr;gap:1.1em 1.4em;align-content:center}}
.stat{{display:flex;flex-direction:column;gap:.1em}}
.stat .big{{font-family:var(--disp);font-weight:800;font-size:2.35em;line-height:1;
  color:var(--primary);letter-spacing:-.02em;font-variant-numeric:tabular-nums}}
.stat .big.accentnum{{color:var(--accent)}}
.stat .lbl{{font-size:.82em;color:var(--muted)}}
.stats .src{{grid-column:1/3;margin:.2em 0 0;font-size:.78em;font-style:italic;color:var(--muted)}}

/* panel */
.panel{{background:var(--card);border:1px solid var(--line);border-radius:.7em;padding:1.25em 1.35em}}
.panel-h{{font-family:var(--mono);font-size:.76em;letter-spacing:.1em;text-transform:uppercase;
  color:var(--accent);font-weight:600;margin:0 0 .95em}}

/* charts */
.chart-slide .cols{{align-items:center}}
.chart{{margin:0;background:#fff;border:1px solid var(--line);border-radius:.7em;
  padding:.7em;box-shadow:0 8px 22px -14px rgba(11,46,61,.4);min-height:0}}
.chart img{{display:block;width:100%;height:auto;border-radius:.2em}}
.note{{display:flex;flex-direction:column;gap:.9em;font-size:.96em;line-height:1.4;color:var(--ink)}}
.note p{{margin:0}}
.note b{{font-weight:600}}
.hero-num{{font-family:var(--disp);font-weight:800;font-size:2.5em;line-height:1;
  color:var(--accent);letter-spacing:-.02em}}
.hero-num small{{font-size:.5em;color:var(--muted);font-weight:700}}
.hero-lbl{{color:var(--muted);font-size:.92em;margin-top:-.4em!important}}
.accent-ink{{color:var(--accent)}}

/* ladder (percentages) */
.ladder{{display:flex;flex-direction:column;gap:.55em}}
.ladder>div{{display:flex;align-items:baseline;gap:.6em}}
.ladder .pct{{font-family:var(--disp);font-weight:800;font-size:1.7em;
  font-variant-numeric:tabular-nums;min-width:2.6em}}
.ladder .muted{{color:var(--muted)}} .ladder .primary{{color:var(--primary)}}
.ladder .accent{{color:var(--accent)}}
.ladder span:last-child{{font-size:.92em;color:var(--muted)}}

/* callouts */
.callout{{padding:.75em .9em;border-radius:.5em;font-size:.98em;line-height:1.36}}
.callout.bad{{background:rgba(180,67,43,.09);color:#7f2e1c}}
.callout.good{{background:rgba(46,125,110,.11);color:#1d5a4d}}
.callout.bad b,.callout.good b{{color:inherit}}
.em{{font-style:italic;color:var(--primary);font-size:.96em}}

/* conclusion */
.concl{{list-style:none;margin:0;padding:0;flex:1;display:flex;flex-direction:column;
  justify-content:center;gap:1.35em}}
.concl li{{position:relative;padding-left:1.6em}}
.concl li::before{{content:"";position:absolute;left:0;top:.34em;width:.62em;height:.62em;
  border-radius:50%;background:var(--accent-bright)}}
.concl b{{display:block;font-family:var(--disp);font-weight:700;font-size:1.32em;color:#fff;margin-bottom:.12em}}
.concl span{{color:var(--d-muted);font-size:1.02em}}

/* end slide */
.slide.end{{justify-content:center}}
.end-wrap{{position:relative;z-index:2}}
.thanks{{font-size:3.6em;margin:0 0 .7em}}
.foot{{font-size:1.02em;color:#CFE0E6;margin:.35em 0;line-height:1.4}}
.foot .k{{font-family:var(--mono);font-weight:600;color:var(--accent-bright);
  text-transform:uppercase;font-size:.78em;letter-spacing:.08em;margin-right:.7em}}
.sig{{margin-top:1.6em;font-family:var(--mono);font-size:.85em;color:#87a3ac}}

/* nav */
.controls{{width:min(96vw,1180px);display:flex;align-items:center;gap:14px}}
.nav-btn{{font:inherit;font-family:var(--mono);font-size:13px;font-weight:600;
  color:var(--primary);background:var(--slide);border:1px solid var(--line);
  border-radius:8px;padding:8px 14px;cursor:pointer;transition:.15s}}
.nav-btn:hover{{background:var(--card);border-color:var(--primary)}}
.nav-btn:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.counter{{font-family:var(--mono);font-size:13px;color:var(--muted);
  font-variant-numeric:tabular-nums;letter-spacing:.05em}}
.dots{{display:flex;gap:7px;margin-left:auto}}
.dot{{width:9px;height:9px;border-radius:50%;border:none;padding:0;cursor:pointer;
  background:#B9CBD0;transition:.2s}}
.dot:hover{{background:var(--primary)}}
.dot.on{{background:var(--accent);transform:scale(1.25)}}
.dot:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.progress{{position:absolute;left:0;top:0;height:4px;background:var(--accent);
  z-index:5;transition:width .4s ease;border-radius:0 3px 3px 0}}
.hint{{font-family:var(--mono);font-size:11px;color:var(--muted);opacity:.8}}
@media (max-width:640px){{.hint{{display:none}} .slide{{font-size:2.1cqw}}}}
</style>

<div class="deck">
  <div class="stage" id="stage">
    <div class="progress" id="progress"></div>
    {slides_html}
  </div>
</div>
<div class="controls">
  <button class="nav-btn" id="prev">‹ Anterior</button>
  <button class="nav-btn" id="next">Seguinte ›</button>
  <span class="counter" id="counter">01 / {N:02d}</span>
  <span class="hint">← → para navegar</span>
  <div class="dots" id="dots">{dots}</div>
</div>

<script>
const N={N};let cur=0;
const slides=[...document.querySelectorAll('.slide')];
const dots=[...document.querySelectorAll('.dot')];
const counter=document.getElementById('counter');
const progress=document.getElementById('progress');
function show(i){{
  cur=Math.max(0,Math.min(N-1,i));
  slides.forEach((s,k)=>s.classList.toggle('active',k===cur));
  dots.forEach((d,k)=>d.classList.toggle('on',k===cur));
  counter.textContent=String(cur+1).padStart(2,'0')+' / '+String(N).padStart(2,'0');
  progress.style.width=((cur+1)/N*100)+'%';
}}
document.getElementById('next').onclick=()=>show(cur+1);
document.getElementById('prev').onclick=()=>show(cur-1);
dots.forEach(d=>d.onclick=()=>show(+d.dataset.to));
document.addEventListener('keydown',e=>{{
  if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' ')  {{e.preventDefault();show(cur+1);}}
  if(e.key==='ArrowLeft' ||e.key==='PageUp') {{e.preventDefault();show(cur-1);}}
  if(e.key==='Home')show(0); if(e.key==='End')show(N-1);
}});
let sx=null;
document.getElementById('stage').addEventListener('touchstart',e=>sx=e.touches[0].clientX,{{passive:true}});
document.getElementById('stage').addEventListener('touchend',e=>{{
  if(sx===null)return;const dx=e.changedTouches[0].clientX-sx;
  if(Math.abs(dx)>45)show(cur+(dx<0?1:-1));sx=null;}});
show(0);
</script>'''

SAIDA.write_text(HTML, encoding="utf-8")
kb = len(HTML.encode())/1024
print(f"[ok] {SAIDA}  ({kb:.0f} KB, {N} slides)")
