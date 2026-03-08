<p align="center">
  <img src="docs/images/banner.svg" alt="BuscaPaginasBlancas Banner" width="900" />
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.x-blue.svg?style=flat-square&logo=python&logoColor=white" alt="Python 3.x" /></a>
  <a href="https://github.com/GeiserX/BuscaPaginasBlancas/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-LGPL--3.0-green.svg?style=flat-square" alt="License: LGPL-3.0" /></a>
  <a href="https://github.com/GeiserX/BuscaPaginasBlancas/stargazers"><img src="https://img.shields.io/github/stars/GeiserX/BuscaPaginasBlancas?style=flat-square&color=yellow" alt="GitHub Stars" /></a>
  <a href="https://github.com/GeiserX/BuscaPaginasBlancas/issues"><img src="https://img.shields.io/github/issues/GeiserX/BuscaPaginasBlancas?style=flat-square" alt="GitHub Issues" /></a>
</p>

<p align="center">
  <strong>Python OSINT tool for extracting contact information from Spanish white pages (Paginas Blancas)</strong>
</p>

---

## About

**BuscaPaginasBlancas** is a command-line OSINT (Open Source Intelligence) tool that queries the Spanish white pages directory (Paginas Blancas) hosted on `paginasamarillas.es`. Given a list of surnames, it systematically extracts publicly listed contact information -- names, phone numbers, and addresses -- and stores the results in a local SQLite database with automatic deduplication.

The tool was designed with the Spanish naming convention in mind: it supports lookups against both the first surname (`apellido1`) and the second surname (`apellido2`) fields, and it automatically generates feminine surname variants (appending `-a`) to maximize coverage.

## Features

- **Dual surname field support** -- Queries both `apellido1` and `apellido2` fields, reflecting the Spanish dual-surname system.
- **Gender-aware surname variants** -- Automatically generates feminine forms of surnames (e.g., `Petrov` / `Petrova`) to broaden search results.
- **SQLite storage with deduplication** -- All results are persisted to a local `paginasblancas.db` file. Phone numbers serve as the primary key to prevent duplicates.
- **Batch processing** -- Accepts bulk surname lists and processes them sequentially.
- **Lightweight dependencies** -- Requires only `requests` and `BeautifulSoup4` on top of the Python standard library.

## Legal and Ethical Considerations

This tool accesses publicly available directory data. However, users bear full responsibility for how they use it. Before running this tool, consider the following:

- **GDPR / LOPDGDD** -- Spanish personal data is protected under the EU General Data Protection Regulation and Spain's Ley Organica de Proteccion de Datos y Garantia de los Derechos Digitales. Bulk collection, storage, or redistribution of personal data without a lawful basis may constitute a violation.
- **Terms of Service** -- Automated scraping may violate the terms of service of `paginasamarillas.es`. Review their ToS before use.
- **Responsible use** -- This tool is intended for lawful OSINT research, journalistic investigation, or personal use only. Do not use it for harassment, stalking, unsolicited marketing, or any purpose that infringes on individuals' privacy rights.
- **Rate limiting** -- Be respectful of the target service. Excessive requests may result in IP blocking and cause disruption.

**The authors assume no liability for misuse of this tool.**

## Installation

```bash
git clone https://github.com/GeiserX/BuscaPaginasBlancas.git
cd BuscaPaginasBlancas
pip install -r requirements.txt
```

### Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`

## Usage

The tool ships with a built-in surname list (sourced from Bulgarian surnames as a demonstration dataset). To run with the defaults:

```bash
python3 crawler.py
```

### Custom Surname Lists

The `SearchSurnames()` function in `crawler.py` fetches surnames from an external wiki page. To use your own list, modify this function to return a Python list of surname strings:

```python
def SearchSurnames():
    return ["Garcia", "Martinez", "Lopez", "Fernandez"]
```

Alternatively, you can call the crawler directly from the command line as documented in `cli.txt`, passing surnames as space-separated arguments.

## Output Format

Results are stored in a SQLite database file named `paginasblancas.db` in the working directory. The schema is:

| Column        | Type | Description                          |
|---------------|------|--------------------------------------|
| Nombre        | TEXT | First name                           |
| Apellido1     | TEXT | First surname (paternal)             |
| Apellido2     | TEXT | Second surname (maternal)            |
| Telefono      | TEXT | Phone number (**PRIMARY KEY**)       |
| Calle         | TEXT | Street address                       |
| CP            | TEXT | Postal code                          |
| CiudadRegion  | TEXT | City and region                      |

Duplicate entries (by phone number) are automatically ignored via `INSERT OR IGNORE`.

## Limitations

- **Single province** -- The current implementation is hardcoded to query `Albacete`. To search other provinces, modify the `nomprov` parameter in the `apellido1()` and `apellido2()` functions.
- **First page only** -- Only the first page of results is scraped per query. Pagination support is stubbed out in the code but not active.
- **No rate limiting** -- The tool does not throttle requests. Users should implement delays if performing large-scale lookups.
- **API stability** -- The tool depends on the HTML structure of `paginasamarillas.es`. Changes to the site may break parsing.

## License

This project is licensed under the [GNU Lesser General Public License v3.0](LICENSE).
