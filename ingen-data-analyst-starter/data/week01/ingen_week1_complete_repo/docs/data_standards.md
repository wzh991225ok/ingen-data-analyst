# Data Standards - Week 1 v0

## Naming
- Use `snake_case` for all column names.
- Use clear source-specific prefixes when merging datasets later.

## Dates
- Use ISO 8601 format: `YYYY-MM-DD`.
- Every public source should include a retrieval date.

## Source tracking
- Every dataset must record source name, URL, retrieval date, intended use, and license/reuse note.
- Company-reported metrics must be labeled as company-reported unless independently verified.

## Missing values
- Use blank cells for unknown values in raw source trackers.
- Use `not_publicly_available` for fields reviewed but not visible in public sources.

## Public-data boundary
- No inGen internal data, customer data, proprietary source code, or private financial information is used.
- Web scraping must respect robots.txt and Terms of Service.

Version: Week 1 initial standard. Retrieval date: 2026-05-26
