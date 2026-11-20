# US Data Center Permit & Filing Sources (`datacenter-permit-sources`)

A curated, machine-readable directory (`sources.json`) and zero-dependency Python CLI (`lookup.py`) of official US public portals used to check whether a data center campus announcement has a primary permit, zoning case, utility filing, or grid record behind it.

## Why primary filings matter

Press releases, news blurbs, and third-party lists often repeat announced capacity figures without showing whether a project has moved through zoning, environmental permitting, or utility agreements. Every entry in `sources.json` states both **what the record proves** and **what it does not prove** so analysts do not confuse an architectural registration or regional load forecast with active construction or energized megawatts.

## Quick start

Requires Python 3.10+. No third-party packages.

```bash
# List all official portals with scope and caveats
python3 lookup.py list

# Filter by state or jurisdiction
python3 lookup.py list --jurisdiction Texas

# Filter by category (power, utility, grid, environmental-permit, utility-filing, building-registration)
python3 lookup.py list --category environmental-permit

# Export machine-readable JSON
python3 lookup.py list --json

# Validate that a project record JSON links to an official filing
python3 lookup.py validate-record sample-record.json --strict-source
```

---

## Included official public portals

| Source | Jurisdiction | Category | What it proves | Key limit |
|---|---|---|---|---|
| [EIA-860M](https://www.eia.gov/electricity/data/eia860m/) | US Federal | Power | Utility-scale operating/planned/retired generators (>= 1 MW) | Not data center IT load or committed grid capacity |
| [EIA-861](https://www.eia.gov/electricity/data/eia861/) | US Federal | Utility | County-level reported electric utility territories | Utility candidate only; not parcel serviceability |
| [PJM Load Forecast (B9 / B9b)](https://www.pjm.com/library/reports-notices.aspx) | PJM RTO | Grid | Regional zone/RTO summer peak load forecast adjustments | Not site-level MW; do not sum B9 and B9b |
| [GLEIF LEI API](https://www.gleif.org/en/lei-data/gleif-api/) | Global / US | Entity | Legal entity identity, status, and registered addresses | Does not prove parcel ownership or tenant |
| [US Census Places](https://www.census.gov/data/tables/time-series/demo/popest/2020s-total-cities-and-towns.html) | US Federal | Geography | Official state/place FIPS codes for incorporated places | Excludes unincorporated county areas & CDPs |
| [TDLR TABS](https://www.tdlr.texas.gov/TABS/Search/) | Texas | Building registration | Registered project scope, reported cost, sq ft, proposed dates | Registration status is not construction stage |
| [MDE Frederick Index](https://mde.maryland.gov/datacenters/Pages/FrederickDataCenter.aspx) | Maryland | Environmental permit | Index of state environmental filings for Frederick projects | Listed title is not an approved permit |
| [Oklahoma DEQ Data Centers](https://oklahoma.gov/deq/deq-information-on-data-centers.html) | Oklahoma | Environmental permit | Air/Water permit status (`ISSUED`, `PENDING`, `REVIEW`) | Permit status is not construction stage |
| [Minnesota PUC ESAs](https://mn.gov/puc/activities/v-l-e-c/data-centers/) | Minnesota | Utility filing | Public docket IDs and ESA filings for large loads | Docket review is not approval or energized MW |

## Filing-backed US pre-operational tracker

If you sell into data center construction (generators, switchgear, cooling, electrical/mechanical contracting, engineering, or land/power brokerage) and want US pre-operational projects tracked from announced through zoning, permits, and construction with every stage linked back to its source record, see **[Wattlas](https://wattlas.io)**.

## License

MIT
