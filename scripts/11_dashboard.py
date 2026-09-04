# -*- coding: utf-8 -*-
"""F1 — Dashboard HTML "Vou atestar hoje?": previsão sobe/desce + probabilidade
por combustível para o dia seguinte à última data do dataset."""
from pathlib import Path
import numpy as np, pandas as pd, html
from lightgbm import LGBMClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.frozen import FrozenEstimator

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "dados" / "dataset_enriquecido.csv"
SAIDA = RAIZ / "dashboard.html"

FEATURES = [
    "preco_eur_l", "preco_lag_1d", "preco_lag_7d", "preco_lag_30d",
    "media_movel_7d", "media_movel_30d",
    "variacao_1d", "variacao_pct_1d", "variacao_7d", "desvio_media_30d",
    "brent_usd", "eur_usd", "brent_eur", "brent_eur_media_movel_7d",
    "brent_usd_var_pct_1d", "brent_usd_var_pct_7d",
    "eur_usd_var_pct_1d", "eur_usd_var_pct_7d",
    "brent_eur_var_pct_1d", "brent_eur_var_pct_7d",
    "isp_eur_l", "iva_taxa", "carga_fiscal_pct", "preco_sem_impostos_eur_l",
    "mes", "trimestre", "semana_ano", "dia_semana", "fim_de_semana", "feriado",
]

df = pd.read_csv(ENTRADA, parse_dates=["data"], encoding="utf-8")
dummies = pd.get_dummies(df["tipoCombustivel"], prefix="comb")
feats = FEATURES + list(dummies.columns)
dfx = pd.concat([df, dummies], axis=1)
valid = dfx.dropna(subset=feats).copy()
ultima = valid["data"].max()
proximo = ultima + pd.Timedelta(days=1)

# treino com alvo; calibração nos últimos ~180 dias antes da última data
comalvo = valid.dropna(subset=["target_subida"]).copy()
comalvo["target_subida"] = comalvo["target_subida"].astype(int)
corte_cal = comalvo["data"].max() - pd.Timedelta(days=180)
ajuste = comalvo[comalvo["data"] < corte_cal]
calib = comalvo[comalvo["data"] >= corte_cal]

base = LGBMClassifier(n_estimators=400, learning_rate=0.05, num_leaves=31,
    subsample=0.8, colsample_bytree=0.8, class_weight="balanced",
    random_state=42, n_jobs=-1, verbose=-1).fit(ajuste[feats], ajuste["target_subida"])
cal = CalibratedClassifierCV(FrozenEstimator(base), method="isotonic").fit(
    calib[feats], calib["target_subida"])

# previsão para as linhas da última data (uma por combustível)
alvo = valid[valid["data"] == ultima].copy()
alvo["p_sobe"] = cal.predict_proba(alvo[feats])[:, 1]

ordem = ["Gasolina especial 95", "Gasolina simples 95", "Gasolina 98",
         "Gasolina especial 98", "Gasóleo especial", "Gasóleo simples",
         "Biodiesel B15", "GPL Auto"]
alvo["ord"] = alvo["tipoCombustivel"].map({n: i for i, n in enumerate(ordem)})
alvo = alvo.sort_values("ord")

cards = []
for _, r in alvo.iterrows():
    p = float(r["p_sobe"]); sobe = p >= 0.5
    conf = p if sobe else 1 - p
    direcao = "Sobe" if sobe else "Desce"
    seta = "&#9650;" if sobe else "&#9660;"   # ▲ / ▼
    cls = "up" if sobe else "down"
    rec = "Atestar hoje" if sobe else "Pode esperar"
    rec_cls = "rec-now" if sobe else "rec-wait"
    nome = html.escape(r["tipoCombustivel"])
    preco = f'{r["preco_eur_l"]:.3f}'.replace(".", ",")
    cards.append(f'''<article class="card {cls}">
  <div class="c-top"><h3>{nome}</h3><span class="price">{preco} <small>€/L</small></span></div>
  <div class="dir {cls}"><span class="arrow">{seta}</span><span class="dir-txt">{direcao}</span>
     <span class="conf">{conf*100:.0f}% confiança</span></div>
  <div class="bar"><div class="bar-fill {cls}" style="width:{conf*100:.0f}%"></div></div>
  <div class="rec {rec_cls}">{rec}</div>
</article>''')

n_sobe = int((alvo["p_sobe"] >= 0.5).sum()); n_desce = len(alvo) - n_sobe
data_ref = ultima.strftime("%d/%m/%Y"); data_prox = proximo.strftime("%d/%m/%Y")

HTML = f'''<title>Vou Atestar Hoje?</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Public+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap">
<style>
:root{{--bg:#EAF0F1;--surf:#FFFFFF;--ink:#16262E;--muted:#5E747D;--primary:#0E5A75;
  --up:#B4432B;--down:#2E7D6E;--accent:#C56A12;--line:#DFE7E9;--card:#F4F8F9;
  --sans:"Public Sans",system-ui,sans-serif;--disp:"Archivo",var(--sans);--mono:"IBM Plex Mono",monospace;}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);
  padding:26px 20px 40px;display:flex;flex-direction:column;align-items:center}}
.wrap{{width:min(94vw,980px)}}
header.top{{background:#0B2E3D;color:#fff;border-radius:16px;padding:26px 30px;
  position:relative;overflow:hidden;margin-bottom:20px}}
header.top .orb{{position:absolute;right:-40px;bottom:-60px;width:220px;height:220px;
  border-radius:50%;background:radial-gradient(circle at 40% 40%,#12658a,#0b2e3d 72%);opacity:.7}}
.kick{{font-family:var(--mono);font-size:12px;letter-spacing:.15em;text-transform:uppercase;
  color:var(--accent);margin:0 0 6px;font-weight:600}}
header.top h1{{font-family:var(--disp);font-weight:800;font-size:2.2rem;margin:0 0 6px;
  letter-spacing:-.02em;position:relative;z-index:2}}
header.top p{{margin:0;color:#CFE0E6;font-size:1rem;position:relative;z-index:2}}
header.top b{{color:#fff}}
.summary{{display:flex;gap:22px;margin-top:16px;position:relative;z-index:2}}
.summary div{{font-family:var(--mono);font-size:.9rem;color:#CFE0E6}}
.summary b{{font-family:var(--disp);font-size:1.4rem;display:block}}
.summary .s-up b{{color:#F08a70}} .summary .s-down b{{color:#7fd6c5}}
.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}}
@media(max-width:620px){{.grid{{grid-template-columns:1fr}}}}
.card{{background:var(--surf);border:1px solid var(--line);border-radius:12px;
  padding:16px 18px;box-shadow:0 6px 18px -12px rgba(11,46,61,.4)}}
.c-top{{display:flex;justify-content:space-between;align-items:baseline;gap:10px}}
.c-top h3{{font-family:var(--disp);font-weight:700;font-size:1.06rem;margin:0;color:var(--primary)}}
.price{{font-family:var(--mono);font-weight:600;font-size:1.1rem;color:var(--ink);white-space:nowrap}}
.price small{{color:var(--muted);font-size:.7rem;font-weight:500}}
.dir{{display:flex;align-items:center;gap:9px;margin:12px 0 8px}}
.dir .arrow{{font-size:1.15rem}}
.dir.up .arrow,.dir.up .dir-txt{{color:var(--up)}}
.dir.down .arrow,.dir.down .dir-txt{{color:var(--down)}}
.dir-txt{{font-family:var(--disp);font-weight:800;font-size:1.25rem}}
.conf{{margin-left:auto;font-family:var(--mono);font-size:.8rem;color:var(--muted)}}
.bar{{height:8px;background:#E7EEEF;border-radius:5px;overflow:hidden}}
.bar-fill{{height:100%;border-radius:5px}}
.bar-fill.up{{background:var(--up)}} .bar-fill.down{{background:var(--down)}}
.rec{{margin-top:13px;display:inline-block;font-family:var(--mono);font-weight:600;
  font-size:.82rem;padding:6px 12px;border-radius:20px}}
.rec-now{{background:rgba(180,67,43,.12);color:#8f2e1c}}
.rec-wait{{background:rgba(46,125,110,.13);color:#1d5a4d}}
.foot{{margin-top:20px;background:var(--card);border:1px solid var(--line);border-radius:12px;
  padding:16px 20px;font-size:.9rem;color:var(--muted);line-height:1.5}}
.foot b{{color:var(--ink)}}
.foot .warn{{color:var(--accent);font-weight:600}}
</style>

<div class="wrap">
  <header class="top">
    <div class="orb"></div>
    <p class="kick">Previsão para {data_prox}</p>
    <h1>Vou atestar hoje?</h1>
    <p>Estimativa do movimento do preço à bomba <b>amanhã</b> ({data_prox}),
       a partir dos dados de <b>{data_ref}</b>.</p>
    <div class="summary">
      <div class="s-up"><b>{n_sobe}</b> devem subir</div>
      <div class="s-down"><b>{n_desce}</b> devem descer/manter</div>
    </div>
  </header>

  <div class="grid">
    {"".join(cards)}
  </div>

  <div class="foot">
    <b>Como ler:</b> a barra mostra a <b>confiança</b> do modelo (LightGBM calibrado).
    Se o preço deve subir, o modelo sugere <b>atestar hoje</b>; se deve descer, <b>pode esperar</b>.
    <br><span class="warn">Aviso:</span> é uma estimativa estatística para fins do projeto
    (~79–82 % de acerto na direção), não um conselho financeiro. Fonte dos preços: DGEG.
  </div>
</div>'''

SAIDA.write_text(HTML, encoding="utf-8")
print(f"[ok] {SAIDA}  | ref={data_ref} prox={data_prox} | sobe={n_sobe} desce={n_desce}")
print(alvo[["tipoCombustivel", "preco_eur_l", "p_sobe"]].round(3).to_string(index=False))
