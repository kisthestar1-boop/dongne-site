-- 동네미팅 신청 저장소 (수파베이스 SQL Editor에 그대로 붙여넣고 Run)
-- 방문자는 '신청 넣기'와 '남은 자리 수 보기'만 할 수 있고, 명단은 볼 수 없습니다.

create table if not exists applicants (
  id bigint generated always as identity primary key,
  event_id text not null,
  gender text not null check (gender in ('M','F')),
  nick text not null check (char_length(nick) between 1 and 12),
  birth int not null check (birth between 1950 and 2010),
  phone text not null check (phone ~ '^010-[0-9]{4}-[0-9]{4}$'),
  status text not null default '신청' check (status in ('신청','대기','확정','취소','보관')),
  created_at timestamptz not null default now()
);

alter table applicants enable row level security;

-- 방문자(anon): 신청 넣기만 가능
drop policy if exists "anon insert" on applicants;
create policy "anon insert" on applicants for insert to anon
  with check (status in ('신청','대기'));

-- 남은 자리 계산용: 숫자만 돌려줌 (개인정보 없음)
create or replace function seat_counts(ev text)
returns table(m int, f int)
language sql security definer set search_path = public as $$
  select count(*) filter (where gender='M' and status in ('신청','확정'))::int,
         count(*) filter (where gender='F' and status in ('신청','확정'))::int
  from applicants where event_id = ev;
$$;
grant execute on function seat_counts(text) to anon;

-- 모임 7일 뒤 연락처 지우기 (진행자가 모임 후 한 번 실행)
-- update applicants set phone = '010-0000-0000', status = '보관' where event_id = 'ev1128jangyu';
