# Fontes de dados

Registo de todas as fontes usadas no projeto, para transparência e reprodutibilidade.
Última atualização: **2026-09-03**.

---

## 1. Dataset base — preços de combustível

| Item | Detalhe |
|---|---|
| **Fonte** | DGEG — Direção-Geral de Energia e Geologia |
| **Página** | <https://precoscombustiveis.dgeg.gov.pt/estatistica/preco-medio-diario/> |
| **Ficheiro** | `Postos.csv` |
| **Conteúdo** | Preço médio diário de 8 combustíveis em Portugal |
| **Período** | desde 2008-11-18 (atualizado automaticamente) |

**Atualização automática (API da DGEG):** o `scripts/00_atualizar_postos.py` vai buscar
os dias mais recentes à mesma API que a página "Preço médio diário" usa, e acrescenta-os
ao `Postos.csv` (corre no início do `run_all`). Endpoint (GET, devolve JSON):
```
https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/PMD?idsTiposComb=&dataIni=YYYY-MM-DD&dataFim=YYYY-MM-DD&qtdPorPagina=9999&pagina=1&orderDesc=0
```
Campos usados: `Data`, `TipoCombustivel`, `PrecoMedioC4` (preço a 4 casas, ex.: "0,8849 €").
Descoberto pela inspeção dos pedidos de rede da página; filtra os 8 combustíveis do projeto.

---

## 2. Drivers internacionais (FRED — Federal Reserve Bank of St. Louis)

Descarregáveis em CSV, sem chave de API. Guardados em cache local (`dados/externo_*.csv`).

| Variável | Série FRED | URL |
|---|---|---|
| **Petróleo Brent (USD/barril)** | `DCOILBRENTEU` | <https://fred.stlouisfed.org/series/DCOILBRENTEU> |
| **Câmbio EUR/USD** | `DEXUSEU` | <https://fred.stlouisfed.org/series/DEXUSEU> |
| **Gasolina spot US Gulf Coast (USD/galão)** ¹ | `DGASUSGULF` | <https://fred.stlouisfed.org/series/DGASUSGULF> |
| **Gasóleo spot US Gulf Coast (USD/galão)** ¹ | `DDFUELUSGULF` | <https://fred.stlouisfed.org/series/DDFUELUSGULF> |
| **Petróleo WTI (USD/barril)** | `DCOILWTICO` | <https://fred.stlouisfed.org/series/DCOILWTICO> |

¹ **A2 — produto refinado:** usado como *proxy* dos preços grossistas (tipo Roterdão),
que é o elo em falta entre o crude e o preço à bomba. Convertido para €/litro e usado
para calcular o **crack spread** (margem de refinação = produto − crude). O produto
refinado (`gasoleo_spot_eur_l`) correlaciona-se **0,91** com o preço à bomba, mais do
que o Brent (0,82). *(A4: os stocks/inventários semanais da EIA não estão acessíveis
via FRED neste ambiente — apenas o crack spread foi implementado.)*

Download direto (CSV):
```bash
curl -s "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DCOILBRENTEU" -o dados/externo_brent.csv
curl -s "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXUSEU"      -o dados/externo_eurusd.csv
```

---

## 3. Impostos

### 3.1. IVA (taxa normal) — **valores exatos**
Taxa normal do IVA aplicada aos combustíveis rodoviários:

| Período | Taxa |
|---|---|
| até 30/06/2010 | 20 % |
| 01/07/2010 – 31/12/2010 | 21 % |
| desde 01/01/2011 | 23 % |

### 3.2. ISP (Imposto Sobre Produtos Petrolíferos)
> ⚠️ **Nota de honestidade dos dados:** o ISP muda por Portaria (com um mecanismo de
> revisão semanal em 2022–2023). A maior parte das âncoras abaixo foi **extraída e
> confirmada diretamente dos PDFs oficiais do Diário da República** (`oficial_DR`);
> algumas provêm de notícias que citam a Portaria (`oficial_noticia`); e o nível
> pré-2018 é uma aproximação (`referencia_aproximada`, base de 2018 aplicada para
> trás). Entre datas o valor mantém-se constante (é assim que a lei funciona entre
> Portarias); o mecanismo semanal fino de 2022–2023 está simplificado aos passos
> capturados. A escala está em [`dados/isp_portarias.csv`](dados/isp_portarias.csv).

**Âncoras em vigor (€/1000 L) — ver `origem` no CSV:**

| Data de vigência | Portaria | Gasolina | Gasóleo | Origem |
|---|---|---|---|---|
| (pré-2018) | 301-A/2018 (base p/ trás) | 526,64 | 343,15 | referência |
| 2018-11-23 | **301-A/2018** | 526,64 | 343,15 | **DR ✓** |
| 2022-03-14 | 111-A/2022 | 489,92 | 308,83 | OA (compila DR) |
| 2022-03-28 | 128-A/2022 | 489,92 | 295,98 | OA (compila DR) |
| 2022-05-02 | 140-A/2022 | 363,78 | 180,58 | OA (compila DR) |
| 2022-05-09 | 141-B/2022 | 343,70 | 168,37 | OA (compila DR) |
| 2022-06-27 | **164-A/2022** | 316,06 | 162,80 | **DR ✓** |
| 2022-10-03 | **249-C/2022** | 360,52 | 163,48 | **DR ✓** (base − redução) |
| 2022-12-31 | **312-F/2022** | 471,64 | 295,98 | **DR ✓** |
| 2023-03-03 | **65-B/2023** | 459,83 | 311,47 | **DR ✓** |
| 2023-06-05 | **150-B/2023** | 460,36 | 323,54 | **DR ✓** |
| 2025-01-01 | **355-B/2024** | 481,26 | 337,21 | **DR ✓** |
| 2025-11-28 | 427-A/2025 | 497,52 | 361,60 | notícia |
| 2026-08-07 | 331-A/2026 | 462,13 | 302,44 | notícia |

> **Método:** os valores `DR ✓` foram extraídos dos PDFs oficiais (`curl` + `pypdf` +
> `cryptography`). Algumas Portarias fixam a taxa ("fixada no valor de € X"); outras
> indicam a redução face à base 2018 ("reduzida em € Y") — nesse caso o valor final é
> `base − Y` (ex.: 249-C/2022 gasolina = 526,64 − 166,12 = 360,52).
>
> **Lacunas restantes (menores):** jul–set/2022, jan–fev/2023 e 2024 não têm um passo
> próprio capturado; nesses intervalos vale o último valor oficial conhecido (os
> pontos que os rodeiam estão próximos, pelo que o erro é pequeno). Para os preencher,
> continuar a correr o extrator sobre as Portarias em falta.

GPL Auto: ISP ≈ 8 €/1000 L (regime próprio, quase nulo).

**PDFs oficiais do Diário da República (confirmados nesta análise):**
- Portaria 301-A/2018 (base, 23-11-2018): <https://files.diariodarepublica.pt/1s/2018/11/22601/0000200002.pdf>
- Portaria 63-A/2022 (gasolina 506,64; jan–abr 2022): <https://files.dre.pt/1s/2022/01/02101/0000200003.pdf>
- Portaria 65-B/2023 (03-03-2023): <https://files.dre.pt/1s/2023/03/04501/0000500006.pdf>
- Portaria 150-B/2023 (05-06-2023): <https://files.diariodarepublica.pt/1s/2023/06/10801/0000400005.pdf>
- Portaria 355-B/2024 (vigência 01-01-2025): <https://files.diariodarepublica.pt/1s/2024/12/25101/0000700008.pdf>
- Portaria 331-A/2026 (07-08-2026): <https://files.diariodarepublica.pt/1s/2026/08/15201/0000200003.pdf>

Os PDFs descarregados ficam em `dados/portarias_pdf/`.

**Fontes secundárias (contexto / valores de 2025-11 e 2026):**
- Ordem dos Advogados — tabela de taxas do ISP:
  <https://portal.oa.pt/publicacoes/informacao-juridica/direito-nacional/tipo-de-informacao/tabelas-custas-tarifarios-taxas-valores-etc/imposto-sobre-os-produtos-petroliferos-e-energeticos-isp-taxas/>
- RTP — desconto do ISP: <https://www.rtp.pt/noticias/economia/governo-aumenta-desconto-do-isp-sobre-gasoleo-e-gasolina-para-3034-e-3513-euros-por-1000-litros_n1751228>
- ECO — ISP no nível mais elevado em 27 anos (out. 2025): <https://eco.sapo.pt/2025/10/02/combustiveis-cortar-desconto-em-vigor-coloca-isp-no-nivel-mais-elevado-em-27-anos/>

---

### 3.3. Como o ISP é lido (ficheiro CSV editável)
A escala do ISP é lida de **`dados/isp_portarias.csv`** — para melhorar a precisão
basta editar/expandir este ficheiro (não é preciso mexer no código). Formato:

```csv
data_inicio,gasolina_eur_1000L,gasoleo_eur_1000L,gpl_eur_1000L,portaria,origem
2022-05-09,343.70,168.37,8.00,151-A/2022,oficial
```

- `data_inicio` — data em que o valor entra em vigor (vale até à linha seguinte).
- `origem` — `oficial_DR` (extraído do PDF do Diário da República), `oficial_noticia`
  (Portaria citada em notícia) ou `referencia_aproximada`.
- Se o ficheiro não existir, o script usa os valores de reserva em `ISP_ANCHORS`.

**Estado atual:** 13 valores oficiais (7 confirmados nos PDFs do DR + 4 compilados
pela Ordem dos Advogados + 2 de notícia) e 1 de referência (nível pré-2018).

### Nota sobre a reconstrução completa a partir do Diário da República
Uma série ISP diária 100 % oficial 2018→2026 exigiria extrair **dezenas de Portarias**
semanais/mensais. Método validado nesta análise: descarregar o PDF do DR (`curl`) e
extrair o texto com `pypdf` + `cryptography` (os PDFs do DR são cifrados com AES).
Limitações: (a) muitas Portarias semanais **só alteram um dos combustíveis** e deixam
o outro como "[...]" (inalterado), obrigando a encadear todos os diplomas por ordem;
(b) os resumos de terceiros divergem (a "base 2018" da gasolina aparece como 363,78 ou
526,64 — sendo **526,64 o valor oficial confirmado no DR**). Por isso capturaram-se os
principais pontos de mudança (base 2018, corte 2022, 2023, 2025, 2026); entre eles
vale o último valor oficial. Para uma série semanal completa, o caminho é continuar a
correr o extrator sobre as restantes Portarias e acrescentá-las ao CSV.

**Portarias relevantes para completar o CSV:** 111-A/2022, 139-A/2022, 151-A/2022,
160-B/2022, 164-A/2022, 65-B/2023, 150-B/2023, 187-C/2023, 355-B/2024, 427-A/2025,
331-A/2026, base 301-A/2018. Extrator de referência: guardado em
`dados/portarias_pdf/` estão os PDFs já descarregados.
