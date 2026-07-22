# HiCloud / Highlander (Hailanyun)

**Status: Alive — the only operator anywhere with underwater datacenters in commercial operation.** Not a graveyard entry; the counter-example the rest of the graveyard is judged against. The catch: "commercial" is heavily state-scaffolded.

## Who they are

Beijing Highlander Digital Technology (Shenzhen-listed, founded 2001) is a maritime electronics company, not a datacenter operator by origin. The underwater business runs through subsidiaries Shenzhen HiCloud and Shanghai Hailanyun (海兰云), with CNOOC's offshore-engineering arm as build partner. Notably, they incorporate tech from their acquired Canadian subsidiary OceanWorks despite subsidiaries sitting on the US Entity List.

## Deployment 1 — Hainan (Lingshui, "first commercial UDC")

First 1,300-ton cabin submerged Dec 2022 at ~35 m, launched with customers Mar 2023; second cabin (400+ servers, pitched at AI inference) added Feb 2025. **Execution reality: 2 cabins, ~1,200 servers total, three years into a plan for 100 cabins** under an RMB 5.6B (~$880M) framework with the Sanya government. Named customers: China Telecom, SenseTime, Tencent (early reports), "about ten companies" by 2025. Workloads skew mundane and latency-tolerant — inference, annotation, consumer app backends. Light Reading's read: effectively a Hainan Free Trade Port demonstration project, not operator-funded colo.

## Deployment 2 — Shanghai Lingang (24 MW, offshore-wind-powered)

The flagship. Launched Jun 2025, built by Oct 2025, full operation May 2026 — commercial rollout in under 30 months, which one UC Davis researcher calls "something Natick never attempted." ~10 m depth, 6–10 km offshore, direct connection to an adjacent 50+ turbine wind farm (97% wind-powered, bypassing the grid). 198 racks, ~2,000 servers. Claimed PUE ~1.15, ≥30% less electricity than land per a CAICT assessment, zero freshwater. Financing: CNY 1.6B (~$222M), state/SOE-heavy (Lingang Special Area committee, state investment holding group, CCCC). Tenants: China Telecom (GPU clusters) and LinkWise.

## Pipeline and export talk

Jun 2025: cooperation agreement targeting a **500 MW** underwater deployment (Shenergy, Shanghai Telecom, INESA, CCCC) — no location or timeline. Export ambitions (Japan, HK, Singapore, Korea) are talk; **no signed overseas deal or shipment as of Jul 2026.** Company claims an 80% cost reduction from shallow-water (<50 m) redesign vs. Natick-style pressure vessels.

## The skeptical read

- Every named tenant is a state carrier or Chinese AI firm. No disclosed pricing, occupancy, contract values, or segment revenue — ever.
- Both flagship sites sit in free-trade/special zones with government co-investment; MERICS traces the driver to state energy-efficiency mandates and AI-infrastructure policy, not market demand.
- Scale is small: 198 racks vs. 2,000–10,000+ for typical land facilities; Hainan is at 2% of its announced cabin count.
- Unanswered engineering questions (per CleanTechnica): failed-server replacement philosophy, cable landing, marine-risk ownership. The "zero failures" claim is unverified.
- Environmental: warm low-oxygen outlet water during marine heat waves; the Hainan site was deliberately sited in an upwelling zone (<24.5°C year-round) — i.e., the model depends on favorable oceanography.

## What it means for the segment

This is the only place on Earth to test whether anyone pays for underwater compute — and the honest answer so far is "the Chinese state pays, with real workloads running." The engineering achievement is real and fast. The demand signal is not yet market-priced. If the 500 MW project gets a site and a date, or a single export order lands, this stops being a demo and starts being an industry.

## Sources

[offshorewind.biz: full operation May 2026](https://www.offshorewind.biz/2026/05/18/china-puts-worlds-first-offshore-wind-powered-underwater-data-centre-into-operation/) · [Scientific American analysis](https://www.scientificamerican.com/article/china-powers-ai-boom-with-undersea-data-centers/) · [Tom's Hardware specs](https://www.tomshardware.com/tech-industry/china-says-worlds-first-offshore-wind-powered-underwater-data-center-has-entered-full-operation-houses-2-000-servers-24-megawatt-subsea-ai-facility-uses-ocean-water-for-passive-cooling-and-offshore-wind-for-power) · [MERICS policy read](https://merics.org/en/comment/china-commercializing-energy-efficient-underwater-data-centers) · [DCD: exports ambition](https://www.datacenterdynamics.com/en/news/chinas-highlander-completes-first-commercial-underwater-data-center-looks-for-exports/) · [DCD: 500 MW agreement](https://www.datacenterdynamics.com/en/news/chinas-hicloud-launches-wind-powered-underwater-data-center-targets-500mw-subsea-deployment/) · [Light Reading skeptical take](https://www.lightreading.com/data-centers/why-subsea-data-centers-can-t-get-afloat) · [CleanTechnica critique](https://cleantechnica.com/2026/06/01/underwater-data-centers-hype/) · [SCMP: Hainan launch](https://www.scmp.com/economy/china-economy/article/3328063/china-launches-worlds-first-commercial-underwater-data-centre-hainan)
