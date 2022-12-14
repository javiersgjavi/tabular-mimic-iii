-- This query extracts dose+durations of dopamine administration
select
stay_id, linkorderid
-- all rows in mcg/kg/min
, rate as vaso_rate
, amount as vaso_amount
, starttime
, endtime
from `physionet-data.mimic_icu.inputevents`
where itemid = 221653 -- dobutamine