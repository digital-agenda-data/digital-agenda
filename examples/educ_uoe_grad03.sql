select
  d.code as dataset,
  'ICT_GRAD' as indicator,
  case
      when dvb.code = 'T' then 'TOTAL'
      else dvb.code
  end as breakdown,
  case
      when dvu.code = 'PC' then 'PC_GRAD'
      else dvu.code
  end as unit,
  case
      when dvc.code = 'EU27_2020' then 'EU'
      else dvc.code
  end as country,
  dvp.code as period,
  f.value as fact,
  f.flags as flags
from estat_facts f
  join estat_datasets d on d.id = f.dataset_id
  join estat_dim_values dvi on dvi.id = f.indicator_id
  join estat_dim_values dvb on dvb.id = f.breakdown_id
  join estat_dim_values dvu on dvu.id = f.unit_id
  join estat_dim_values dvc on dvc.id = f.country_id
  join estat_dim_values dvp on dvp.id = f.period_id

order by dataset, indicator, breakdown, unit, country, period;
