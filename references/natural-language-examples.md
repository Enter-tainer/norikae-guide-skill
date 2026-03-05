# Natural Language to Parameter Examples

Use these examples when translating user requests into canonical fields before querying Yahoo! 乗換案内.

## Basic Route

| User Request | Canonical Fields |
| --- | --- |
| 东京到新宿怎么走 | `from=東京`, `to=新宿` |
| Route from Shinjuku to Yokohama | `from=新宿`, `to=横浜` |
| 東京から九段下まで | `from=東京`, `to=九段下` |

## Via Stations

| User Request | Canonical Fields |
| --- | --- |
| 東京から新宿まで、表参道経由で | `from=東京`, `to=新宿`, `via=["表参道"]` |
| Shibuya to Ikebukuro via Harajuku and Shinjuku | `from=渋谷`, `to=池袋`, `via=["原宿","新宿"]` |
| 东京到上野，经过秋叶原和神田 | `from=東京`, `to=上野`, `via=["秋葉原","神田"]` |

## Time Intent

| User Request | Canonical Fields |
| --- | --- |
| 10:30出发 | `hour=10`, `minute=30`, `timeType=departure` |
| I need to arrive by 18:00 | `hour=18`, `minute=0`, `timeType=arrival` |
| 始発で行きたい | `timeType=first_train` |
| 最终电车回去 | `timeType=last_train` |

## Sort Preference

| User Request | Canonical Fields |
| --- | --- |
| 一番安いルート | `sortBy=fare` |
| 最快路线 | `sortBy=time` |
| 换乘最少 | `sortBy=transfer` |

## Fare, Seat, Walk

| User Request | Canonical Fields |
| --- | --- |
| きっぷ運賃で | `ticket=cash` |
| 指定席で | `seatPreference=reserved` |
| グリーン車で | `seatPreference=green` |
| 急いでるので早歩き | `walkSpeed=fast` |
| ゆっくり歩きたい | `walkSpeed=slow` |

## Transport Exclusion

| User Request | Canonical Fields |
| --- | --- |
| 新幹線なしで | `useShinkansen=false` |
| 在来線だけで | `useShinkansen=false`, `useExpress=false` |
| No buses please | `useHighwayBus=false`, `useLocalBus=false` |
| 飞机也不要 | `useAirline=false` |

## Combined Constraints

### Example 1

User request:

`明天早上10点前到大阪，不要新干线，最便宜。`

Canonical fields:

- `from=東京` (if implied departure from current context)
- `to=大阪`
- `timeType=arrival`
- `hour=10`
- `useShinkansen=false`
- `sortBy=fare`

### Example 2

User request:

`来週金曜18時までに品川着、新宿発、飛行機なし、乗換少なめ。`

Canonical fields:

- `from=新宿`
- `to=品川`
- `timeType=arrival`
- `year/month/day` resolved from "来週金曜"
- `hour=18`
- `useAirline=false`
- `sortBy=transfer`

## Clarification Rules

Ask one concise clarification when:

- station name is ambiguous
- departure station is missing and cannot be inferred from context
- user gives conflicting priorities (`fastest` and `cheapest`) without tie-break
