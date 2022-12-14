-- This query extracts dose+durations of norepinephrine administration
select
  stay_id, linkorderid
  -- two rows in mg/kg/min... rest in mcg/kg/min
  -- the rows in mg/kg/min are documented incorrectly
  , CASE WHEN rateuom = 'mg/kg/min' AND patientweight = 1 THEN rate
  -- below row is written for completion, but doesn't impact rows
  WHEN rateuom = 'mg/kg/min' THEN rate * 1000.0
  ELSE rate END AS vaso_rate
  , amount as vaso_amount
  , starttime
  , endtime
from `physionet-data.mimic_icu.inputevents`
where itemid = 221906 -- norepinephrine