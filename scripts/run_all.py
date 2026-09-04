# -*- coding: utf-8 -*-
"""
run_all.py — C4: corre todo o pipeline por ordem, com um só comando.

Uso:
    python scripts/run_all.py            # pipeline principal (01–17)
    python scripts/run_all.py --tudo     # inclui os 19 algoritmos (lento: LSTM/Prophet)

Mostra [OK]/[FALHOU] e o tempo de cada passo. Continua mesmo que um passo falhe,
e no fim resume quantos correram.
"""
import os, sys, subprocess, time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SCRIPTS = RAIZ / "scripts"

PRINCIPAL = [
    "00_atualizar_postos.py",                       # buscar dados novos à DGEG
    "01_enriquecer_dataset.py", "testes_pipeline.py", "02_analise_dados.py",
    "03_modelo_classificacao.py", "04_modelo_regressao.py",
    "05_modelo_delta_e_7dias.py", "06_gradient_boosting.py",
    "07_tuning_validacao.py", "08_multiclasse.py", "09_probabilidade.py",
    "10_decisao.py", "11_dashboard.py", "12_previsao_ao_vivo.py",
    "13_por_combustivel.py", "14_permutacao.py", "15_analise_erros.py",
    "16_shap.py", "17_skill_horizonte.py",
    "18_apresentacao.py",                           # gerar apresentacao.html
]
SUPERVISIONADA = [
    "supervisionada/01_regressao.py", "supervisionada/02_classificacao.py",
    "supervisionada/03_series_temporais.py", "supervisionada/04_metodos_conjunto.py",
]


def main():
    passos = PRINCIPAL + (SUPERVISIONADA if "--tudo" in sys.argv else [])
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "MPLBACKEND": "Agg"}
    print("=" * 64)
    print(f"CORRER TUDO — {len(passos)} passos"
          f"{' (inclui os 19 algoritmos)' if '--tudo' in sys.argv else ''}")
    print("=" * 64)
    falhas, t0 = [], time.time()
    for i, s in enumerate(passos, 1):
        ini = time.time()
        r = subprocess.run([sys.executable, str(SCRIPTS / s)], env=env,
                           capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        dt = time.time() - ini
        estado = "OK    " if r.returncode == 0 else "FALHOU"
        print(f"  [{estado}] {i:2}/{len(passos)}  {s:38} ({dt:5.1f}s)")
        if r.returncode != 0:
            falhas.append(s)
            print("    └─", (r.stderr.strip().splitlines() or ["(sem stderr)"])[-1][:120])
    print("-" * 64)
    print(f"{len(passos)-len(falhas)}/{len(passos)} passos OK em {time.time()-t0:.0f}s.")
    if falhas:
        print("Falharam:", ", ".join(falhas))
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
