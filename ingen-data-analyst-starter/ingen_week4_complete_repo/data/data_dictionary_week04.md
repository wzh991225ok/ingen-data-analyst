# Data Dictionary — Week 4

## Market total anchors (public market-research summaries, retrieved 2026-06-01)
| Vertical | Anchors (low–high, 2024-25) | Sources |
|----------|------------------------------|---------|
| Eldercare | $2.7B–$3.4B | Grand View, InsightAce, Global Industry Analysts, Vision Research |
| Education | $1.4B–$2.2B | Educational-robot market summaries; NCES base (Week 3) |
| Indoor security | $4.7B–$19.1B (scope-dependent) | Mordor, Precedence, MRFR, Grand View |
| Outdoor patrol | $153M–$2.0B (definition-dependent) | Valuates (narrow), Mordor, Precedence |
| Humanoid | $290M–$4.89B (very wide) | Grand View, Precedence, Fortune Business Insights, IntelMarket |

## Demand-side bases (from Week 3 warehouse — versioned, sha256-logged)
| Base | Source table |
|------|--------------|
| US 65+ population | shared.worldbank_pop_65plus / eldercare.census_population_by_age |
| K-12 enrollment | education.nces_k12_enrollment |
| Security/warehouse labor | indoor_security.bls_security_guards / outdoor_patrol.bls_warehousing_employment |
| Robotics research momentum | humanoid.openalex_robotics_publications |

Notes:
- Market totals are vendor estimates that DISAGREE; used as low/high ranges, never single points.
- Bottom-up unit bases (households, schools, buildings, sites, facilities) are public approximations;
  sharpen with paid databases before external use. Every assumption is in market_sizing_assumptions.csv.
