# ERS-2026-003: Why Carrier-Board Module-Current Measurements Can Be Misleading

Supporting artefacts for **ERS-2026-003**, an independent engineering assessment published by Radianode Ltd (October 2026).

The report examines supply-header current on two off-the-shelf cellular carrier boards: a Quectel BG95-M3 on a DIP40CORE-A breakout, and a SIMCom SIM7080G on a Waveshare Cat-M/NB-IoT HAT. On both boards the off-state header current is about two orders of magnitude above the module manufacturer's power-off figure, so a header reading does not isolate module current.

- Report: [`ERS-2026-003_v1.0.pdf`](ERS-2026-003_v1.0.pdf)
- Reproducibility Statement: [`ERS-2026-003_Reproducibility_Statement.pdf`](ERS-2026-003_Reproducibility_Statement.pdf). It identifies every source (E, X, D numbers), the analysis, and the values a correct reproduction returns.

## Repository layout

| Path | Contents | Statement IDs |
|---|---|---|
| `data/waveshare_hat/raw/` | Waveshare HAT off-state raw capture, 26 August 2026 (CSV, 10.000 s at 100 kS/s) | E12 |
| `data/waveshare_hat/screenshots_15oct2026/` | Power Profiler views after each Waveshare HAT recording, 15 October 2026 | E33, E34 |
| `data/waveshare_hat/photos_15oct2026/` | Waveshare HAT photographs, module off and on, 15 October 2026 | E35 to E37 |
| `data/waveshare_hat/photos/` | Waveshare HAT attachment and board photographs (August and 14 October 2026) | E13, E14, E28, E29 |
| `data/dip40core_a/screenshots_sep2026/` | DIP40CORE-A Power Profiler screenshots, September 2026 | E2 to E5 |
| `data/dip40core_a/screenshots_14oct2026/` | DIP40CORE-A Power Profiler settings and selections, AT-command transcripts, 14 October 2026 | E17, E24, E25, E26, E30 |
| `data/dip40core_a/photos_14oct2026/` | DIP40CORE-A module marking photograph | E16 |
| `data/dip40core_a/derived/` | Per-second summaries computed from the raw recordings | X1 to X4 |
| `data/instrument/` | Power Profiler ampere-meter reference view | E6 |
| `docs/ERS-2026-003_Bench_Session_Log.md` | Session record of the 14 October 2026 bench session, frozen at release | E15 |
| `scripts/ers003_analysis.py` | Analysis of `.ppk2` and CSV recordings | |
| `scripts/figures/` | Figure generation | |
| `LICENSE`, `LICENSE-DATA`, `CITATION.cff` | Licences and citation metadata | |
| `SHA256SUMS` | SHA-256 of every file in this repository except this README | |

Manufacturer documents (Statement D1 to D8) are cited by version, table and SHA-256 only and are not redistributed.

## Raw recordings (Zenodo)

The seven raw DIP40CORE-A recordings from 14 October 2026 and the two Waveshare HAT recordings from 15 October 2026 are held in a Zenodo dataset, because six of them exceed GitHub's 100 MB file limit.

**Dataset DOI: [10.5281/zenodo.23399520](https://doi.org/10.5281/zenodo.23399520)**

| ID | File | Size | SHA-256 |
|---|---|---|---|
| E18 | `A2_run1_preliminary.ppk2` | 8.3 MB | `0b8d4d606998a7071c43000900744854ec1a9a2ec209f774df7f27b7c2e388b0` |
| E19 | `A2_run2.ppk2` | 180.0 MB | `3ae971a6932365778db464d8bd3f6fcf123edc60ab11f76e504c92b03826a921` |
| E20 | `A2_run3_off.ppk2` | 162.0 MB | `6e7cd6cd819d685534ad32b6a0db3fe1a243493b2e714ab0c86cfbc4f3275690` |
| E21 | `A2_run3_off.csv` | 4,851.6 MB | `cbc90e1e4c54e96df23a39d40b031cc448d02a9dd496c59cb40db014c1a946c8` |
| E22 | `A4_uart_disconnect.ppk2` | 27.1 MB | `d5229ae32e3cea104b03d472d841ad8df9cfe38811180f0627ee0f1dd57c0542` |
| E23 | `A4_uart_disconnect.csv` | 787.1 MB | `815c8ee42d31093f38a549c707fb9b54f093802078f381f52bcfbf8d7c6725d9` |
| E27 | `A2_run2.csv` | 27.5 MB | `5eabd903f7cc4a5cd7fc2639e528d5dab86a56405e9160df849ad390233d3177` |
| E31 | `ppk-20261015T194532.csv` | 802.8 MB | `f8df6e9e3ff49c11fb56df6fad380c893638f7086cd6ac33b06c0fdbaa1577ff` |
| E32 | `ppk-20261015T201803.csv` | 793.2 MB | `50cc29e359a2c0ced3b571b4c325e08faf931c2350aadcb7c6f3d64faad95eaa` |

The Zenodo record also contains `A2_run1_preliminary.ppk2.csv` and four PNG files (`A2_run1_preliminary.ppk2.png`, `A2_run2.png`, `A2_run3_off.png`, `A4_uart_disconnect.png`). The Statement does not cite them.

`.ppk2` files are Power Profiler v4.4.1 state files (formatVersion 2); the format, as read by the analysis script, is described in Statement section 4 and in the script's header.

## Verifying the files

Linux or macOS, from the repository root:

```
sha256sum -c SHA256SUMS
```

Windows (PowerShell), for a single file:

```
Get-FileHash -Algorithm SHA256 <file>
```

Compare the raw recordings downloaded from Zenodo against the table above.

## Reproducing the results

Requires Python 3 with NumPy; the figure scripts also use Matplotlib and Pillow. Example, run 3 off-state mean (Statement sections 5 and 6 give the full set of commands and the expected values):

```
python3 scripts/ers003_analysis.py csv A2_run3_off.csv X3.csv
python3 scripts/ers003_analysis.py stats X3.csv 0:600 600:1200 1200:1800 0:1801
python3 scripts/ers003_analysis.py events A2_run3_off.csv 1300 2000
```

Statement section 8 lists what cannot be reproduced from files (operator multimeter readings and statements).

## Licensing

Code and data are licensed separately:

- **`scripts/`** (analysis and figure-generation code): [MIT License](LICENSE).
- **`data/`, `docs/`** (measured evidence, raw captures, session log): [CC BY 4.0](LICENSE-DATA).

## Citation

See [CITATION.cff](CITATION.cff), or cite directly:

> Ogunjemilua, O.A. (2026). *ERS-2026-003: Why Carrier-Board Module-Current Measurements Can Be Misleading.* v1.0. Radianode Ltd.

## Authors

**Principal Engineer:** Oluwanifemi Ogunjemilua ([ORCID: 0009-0003-5205-7738](https://orcid.org/0009-0003-5205-7738))  
**Developed under:** Radianode Ltd  
**Website:** [https://radianode.com](https://radianode.com)

## Contact

Radianode Ltd, Company No. 17359155 · hello@radianode.com · radianode.com
