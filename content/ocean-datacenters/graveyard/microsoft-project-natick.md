# Microsoft Project Natick

**Status: Dead (officially confirmed mid-2024).** The segment's flagship validator and its most important graveyard entry. It worked, and Microsoft killed it anyway.

## What they built

Submerged sealed-pod datacenters, tested in two phases:

- **Phase 1 — "Leona Philpot" (2015).** 105-day proof-of-concept, 11 m deep off San Luis Obispo, CA. 38,000-lb container. Measured PUE 1.07.
- **Phase 2 — "Northern Isles" (2018–2020).** 864 servers in 12 racks, 27.6 PB storage, 240 kW, sealed in dry nitrogen inside a ~12 m × 2.8 m cylinder, 117 ft deep off Orkney, Scotland (sited at the European Marine Energy Centre for its renewable grid). Ran Azure workloads untouched for 25 months and 8 days.

Stated purpose: test feasibility of subsea datacenters powered by offshore renewables, on 5-year no-maintenance deployment cycles.

## Results

- **1/8th the server failure rate** of the land control (6 of 855 failed underwater vs. 8 of 135 on land). Credited to the oxygen-free nitrogen atmosphere and zero human handling.
- PUE 1.07 vs. 1.125 for Microsoft's best contemporary land facilities; ~3% cooling overhead.
- Zero water consumption.
- Claimed 90 days factory-to-operation vs. 18–24 months for a land build.

All figures self-reported by Microsoft; never independently replicated; prototype scale only.

## How it died

Quietly, then officially. The pod was retrieved July 2020, cut up and recycled by early 2021, with no commitment to further deployments. In June 2024, Cloud Operations chief Noelle Walsh confirmed to DatacenterDynamics: **"I'm not building subsea data centers anywhere in the world"** — while acknowledging "my team worked on it, and it worked." No revival through mid-2026.

## Why it died

**Unknown — and that's the point.** Microsoft never publicly stated a reason. No technical failure was cited. The widely repeated explanation — "you can't service submerged servers" — is third-party commentary, and it failed adversarial verification (0–3) as the confirmed cause. Candidate explanations, all unconfirmed: economics at scale, power density limits vs. AI-era GPU racks, permitting friction, or land-based datacenters simply winning the internal capital allocation. Learnings (sealed nitrogen atmospheres, lights-out operation) were redirected into land-based work, notably liquid cooling.

**For diligence:** any startup pitching this segment must answer why they'll succeed where the world's best-resourced datacenter operator validated the tech and still declined to deploy it.

## Sources

[Natick project site](https://natick.research.microsoft.com/) · [Microsoft feature, Sep 2020](https://news.microsoft.com/source/features/sustainability/project-natick-underwater-datacenter/) · [IEEE Spectrum (by the Natick team)](https://spectrum.ieee.org/underwater-data-centers/particle-10) · [DCD analysis](https://www.datacenterdynamics.com/en/analysis/project-natick-microsofts-underwater-voyage-discovery/) · [Redmond Mag on the shutdown](https://redmondmag.com/articles/2024/06/24/project-natick-dries-up.aspx) · [IT Pro skeptical take](https://www.itpro.com/infrastructure/data-centres/microsoft-scrapped-its-project-natick-underwater-data-center-trial-heres-why-it-was-never-going-to-work)
