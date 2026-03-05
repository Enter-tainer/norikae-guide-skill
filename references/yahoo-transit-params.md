# Yahoo Transit Parameter Map

Use this reference to convert natural language route constraints into a Yahoo! 乗換案内 URL, then fetch and extract route content.

Base URL:
`https://transit.yahoo.co.jp/search/result`

## Required Query Parameters

| Canonical Field | Query Key | Value Rule |
| --- | --- | --- |
| `from` | `from` | Japanese departure station |
| `to` | `to` | Japanese arrival station |
| `year` | `y` | 4-digit year |
| `month` | `m` | 2-digit month (`01`-`12`) |
| `day` | `d` | 2-digit day (`01`-`31`) |
| `hour` | `hh` | `0`-`23` |
| `minute` tens | `m1` | `floor(minute / 10)` |
| `minute` ones | `m2` | `minute % 10` |

## Option Mapping

### Time Type (`type`)

| Canonical Value | Query Value | Meaning |
| --- | --- | --- |
| `departure` | `1` | Depart at specified time |
| `last_train` | `2` | Last train |
| `first_train` | `3` | First train |
| `arrival` | `4` | Arrive by specified time |
| `unspecified` | `5` | No time preference |

### Ticket (`ticket`)

| Canonical Value | Query Value |
| --- | --- |
| `ic` | `ic` |
| `cash` | `normal` |

### Seat Preference (`expkind`)

| Canonical Value | Query Value |
| --- | --- |
| `non_reserved` | `1` |
| `reserved` | `2` |
| `green` | `3` |

### Walk Speed (`ws`)

| Canonical Value | Query Value |
| --- | --- |
| `fast` | `1` |
| `slightly_fast` | `2` |
| `slightly_slow` | `3` |
| `slow` | `4` |

### Sort (`s`)

| Canonical Value | Query Value |
| --- | --- |
| `time` | `0` |
| `fare` | `1` |
| `transfer` | `2` |

### Transport Toggles

| Canonical Field | Query Key | `true` | `false` |
| --- | --- | --- | --- |
| `useAirline` | `al` | `1` | `0` |
| `useShinkansen` | `shin` | `1` | `0` |
| `useExpress` | `ex` | `1` | `0` |
| `useHighwayBus` | `hb` | `1` | `0` |
| `useLocalBus` | `lb` | `1` | `0` |
| `useFerry` | `sr` | `1` | `0` |

## Via Stations

- Use repeated `via` parameters.
- Keep at most 3 via stations.
- Example: `...&via=表参道&via=飯田橋`

## Station Name Normalization Examples

| Input | Use in Query |
| --- | --- |
| Tokyo | 東京 |
| Shinjuku | 新宿 |
| Shibuya | 渋谷 |
| Ikebukuro | 池袋 |
| Yokohama | 横浜 |
| 东京 / 東京 | 東京 |
| 涩谷 / 澀谷 | 渋谷 |
| 横滨 / 橫濱 | 横浜 |

## Fetch and Extraction Commands

Fetch using canonical fields:

```bash
python3 scripts/fetch_norikae_routes.py \
  --from 東京 --to 新宿 --via 表参道 \
  --year 2026 --month 3 --day 6 --hour 10 --minute 30 \
  --time-type departure --sort-by time --show-url
```

Fetch from an existing URL:

```bash
python3 scripts/fetch_norikae_routes.py --url 'https://transit.yahoo.co.jp/search/result?...' --show-url
```

Return HTML snippet instead of plain text:

```bash
python3 scripts/fetch_norikae_routes.py --url '<url>' --format html
```

## Extraction Strategy

- Remove noisy elements (`script`, `style`, comments, nav/header/footer/aside).
- Prefer the HTML section starting at `class="...routeDetail..."` and ending before `条件を変更して検索`.
- Fallback to plain text extraction and same boundary markers.
