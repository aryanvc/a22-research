---
title: Ocean Datacenters
theme: Ocean Infrastructure
verdict: Physics proven, business unproven: everyone who learned the most chose land.
status: living
created: 2026-07-22
updated: 2026-07-22
---

# Ocean Datacenters

Segment deep-dive #1 of the ocean infrastructure research project. Researched Jul 22, 2026 via multi-source verified web research (20 sources fetched, 25 top claims adversarially verified, 23 confirmed).

**One-line verdict:** The physics works and is proven. The business is unproven — nobody outside China claims a paying customer, and the best-resourced operator (Microsoft) proved the concept and then walked away without saying why.

---

## The technology value proposition

The pitch: put sealed server pods on the seafloor (or servers on floating barges) and let the ocean do the cooling. Nearly all the hard numbers come from one experiment — Microsoft's Project Natick — so treat them as one vendor's self-reported results, never independently replicated, and demonstrated only at small prototype scale (864 servers, 240 kW).

**Reliability — the flagship result.** Microsoft's submerged pod had roughly one-eighth the server failure rate of its land-based control group: 6 of 855 servers failed underwater over ~25 months vs. 8 of 135 on land. Microsoft credits the sealed nitrogen atmosphere (no corrosive oxygen) and no humans bumping the hardware. Caveat: small absolute numbers, and the land control was a 135-server rack, not a full replica facility. *(High confidence, 5 sources)*

**Cooling efficiency.** The pod ran at PUE 1.07 vs. 1.125 for Microsoft's best land datacenters at the time — cooling overhead of about 3%, vs. 10–30% for air-cooled land facilities. It just pumped seawater through heat exchangers. *(High confidence)*

**Zero water use.** No water consumed for cooling at all, vs. up to 4.8 liters per kWh on land. Note: 4.8 is a worst-case land figure; industry average is ~1.8, so the headline contrast is framed against the least efficient land facilities. *(Medium confidence)*

**Deployment speed.** Standardized pods: factory to operational at any coastal site in under 90 days, vs. 18–24 months for a land build. Microsoft's project lead argued this transforms cost of capital — you don't build capacity years ahead of demand. Only ever demonstrated at single-pod scale. *(High confidence)*

**Latency.** Microsoft's framing: more than half the world's population lives within 120 miles of a coast, so coastal pods sit near users. The demographic figure is at the optimistic edge — peer-reviewed estimates run 38–44% depending on the distance band. *(Microsoft framing, directionally true)*

**The structural risk.** Peer-reviewed work (Scientific Reports 2024, plus Nature-family depth studies) shows marine heat waves are most intense at 50–250 m depth and reach continental-shelf bottoms — exactly where pods sit (Natick was at 36 m). The free-cooling advantage is climate-vulnerable, not permanent. *(High confidence, no commercial interest in the source)*

## Approaches attempted

1. **Submerged sealed pods** (Microsoft Natick; Subsea Cloud; NetworkOcean; China's Highlander/HiCloud). Phase 1 "Leona Philpot": 105-day test in 2015 off California. Phase 2 "Northern Isles": 864 servers, 12 racks, 27.6 PB, 240 kW, sealed in nitrogen in a ~12 m cylinder 117 ft deep off Orkney, Scotland — ran Azure workloads untouched for 25 months (Jun 2018–Jul 2020). Purpose: test subsea datacenters powered by offshore renewables, with 5-year no-maintenance deployment cycles.
2. **Floating barges** (Google's barge experiment; Nautilus Data Technologies) — datacenter stays above water, cooling water drawn from the body below. See company pages.
3. **China's commercial variant** (Highlander/HiCloud/Hailanyun) — the only claimed *commercial* underwater deployments: Hainan (~2023) and a 24 MW offshore-wind-powered facility off Shanghai (full operation ~May 2026). See company page.

## Customers

Three tiers of evidence, from company-page research (Jul 2026):

- **Underwater, Western vendors: zero paying customers, ever.** Microsoft framed Natick as research only and never productized it. Subsea Cloud and NetworkOcean never named a customer.
- **Floating, Western: one real but modest book.** Nautilus's Stockton barge reached 86% occupancy (5.58 MW) — City of Stockton and San Joaquin County disaster-recovery, Backblaze storage, a Cerebras deployment. Government DR and cold storage, not premium workloads — and the barge is now for sale.
- **Underwater, China: real workloads, state-scaffolded demand.** China Telecom, SenseTime, Tencent, LinkWise across two operating sites — every named tenant is a state carrier or Chinese AI firm, with no disclosed pricing or occupancy. See [HiCloud / Highlander](graveyard/hicloud-highlander.md).

Net: nobody has yet paid a market rate for underwater compute anywhere in the West. The buyer story (hyperscale, edge, AI training) remains a story.

## Graveyard

The flagship entry is the segment's own validator. Company pages:

- [Microsoft Project Natick](graveyard/microsoft-project-natick.md) — proved it, then killed it, never said why
- [Google barges](graveyard/google-barges.md) — floating datacenter patent → mystery barges → scrapped
- [Nautilus Data Technologies](graveyard/nautilus-data-technologies.md) — floating barge colo
- [Subsea Cloud](graveyard/subsea-cloud.md) — underwater pods, announced deployments
- [NetworkOcean](graveyard/networkocean.md) — YC startup, GPUs in SF Bay
- [HiCloud / Highlander](graveyard/hicloud-highlander.md) — the counter-example: alive and claiming commercial operation in China

Key nuance on Natick: the popular "you can't service submerged servers" explanation was **refuted** in verification (0–3) as the confirmed reason — it's third-party commentary. Microsoft never publicly stated why it stopped. Noelle Walsh (Cloud Ops chief, mid-2024): "I'm not building subsea data centers anywhere in the world… my team worked on it, and it worked." Learnings went into land-based liquid cooling.

## Open questions (the diligence list)

1. **Why did Microsoft actually kill Natick?** Economics at scale? Power density? Permitting? Land simply winning? This is the central question for anyone funding the segment.
2. **Has anyone, anywhere, paid market rates for underwater or floating capacity?** If China's deployments are real commercial operations, what do the economics and customers look like?
3. **Does the efficiency advantage survive AI-era rack density?** At 50–100+ kW/rack GPU clusters, land-based liquid cooling — the very tech Microsoft redirected Natick's learnings into — may have closed most of the cooling gap.

## Sources

Primary: [Microsoft Natick project site](https://natick.research.microsoft.com/) · [Microsoft feature](https://news.microsoft.com/source/features/sustainability/project-natick-underwater-datacenter/) · [IEEE Spectrum (Natick team)](https://spectrum.ieee.org/underwater-data-centers/particle-10) · [Scientific Reports 2024 (marine heat waves)](https://www.nature.com/articles/s41598-024-54050-8)

Secondary: [DCD Natick analysis](https://www.datacenterdynamics.com/en/analysis/project-natick-microsofts-underwater-voyage-discovery/) · [Redmond Mag shutdown](https://redmondmag.com/articles/2024/06/24/project-natick-dries-up.aspx) · [IT Pro skeptical take](https://www.itpro.com/infrastructure/data-centres/microsoft-scrapped-its-project-natick-underwater-data-center-trial-heres-why-it-was-never-going-to-work) · [DCK economics](https://www.datacenterknowledge.com/hyperscalers/why-microsoft-thinks-underwater-data-centers-may-cost-less) · [The Register Jun 2026 landscape](https://www.theregister.com/systems/2026/06/23/datacenters-dip-a-toe-back-into-waterborne-computing-despite-obvious-challenges/5259331) · [Tom's Hardware China UDC](https://www.tomshardware.com/tech-industry/china-says-worlds-first-offshore-wind-powered-underwater-data-center-has-entered-full-operation-houses-2-000-servers-24-megawatt-subsea-ai-facility-uses-ocean-water-for-passive-cooling-and-offshore-wind-for-power) · [Data Center Frontier offshore survey](https://www.datacenterfrontier.com/site-selection/article/55380207/innovations-in-offshore-data-centers-chinese-deployments-floating-platforms-and-future-prospects)
