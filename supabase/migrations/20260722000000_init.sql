create table if not exists dossiers (
  slug text primary key,
  title text not null,
  theme text,
  verdict text,
  status text default 'living',
  created date,
  updated date,
  page_count int,
  synced_at timestamptz default now()
);

create table if not exists push_log (
  id bigint generated always as identity primary key,
  slug text not null references dossiers(slug),
  pushed_at timestamptz default now(),
  page_count int,
  note text
);

alter table dossiers enable row level security;
alter table push_log enable row level security;

create policy "public read dossiers" on dossiers for select using (true);
create policy "public read push_log" on push_log for select using (true);
