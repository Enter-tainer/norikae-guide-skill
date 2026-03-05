# Yahoo Transit Parameter Map

Use this reference to map canonical route fields into Yahoo! 乗換案内 query parameters.

Base URL:
`https://transit.yahoo.co.jp/search/result`

## Required Core Fields

| Canonical Field | Query Key | Rule |
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

| Canonical | Query | Meaning |
| --- | --- | --- |
| `departure` | `1` | Depart at specified time |
| `last_train` | `2` | Last train |
| `first_train` | `3` | First train |
| `arrival` | `4` | Arrive by specified time |
| `unspecified` | `5` | No time preference |

### Ticket (`ticket`)

| Canonical | Query |
| --- | --- |
| `ic` | `ic` |
| `cash` | `normal` |

### Seat Preference (`expkind`)

| Canonical | Query |
| --- | --- |
| `non_reserved` | `1` |
| `reserved` | `2` |
| `green` | `3` |

### Walk Speed (`ws`)

| Canonical | Query |
| --- | --- |
| `fast` | `1` |
| `slightly_fast` | `2` |
| `slightly_slow` | `3` |
| `slow` | `4` |

### Sort (`s`)

| Canonical | Query |
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
- Ignore additional stations after the third one.
- Example: `...&via=表参道&via=飯田橋&via=秋葉原`

## Defaults

If not provided explicitly:

- `timeType=departure`
- `ticket=ic`
- `seatPreference=non_reserved`
- `walkSpeed=slightly_slow`
- `sortBy=time`
- transport toggles all `true`

## Station Normalization Notes

Use Japanese station names for query parameters. A few common conversions:

| Input | Query Value |
| --- | --- |
| Tokyo | 東京 |
| Shinjuku | 新宿 |
| Shibuya | 渋谷 |
| Ikebukuro | 池袋 |
| Yokohama | 横浜 |
| 东京 / 東京 | 東京 |
| 涩谷 / 澀谷 | 渋谷 |
| 横滨 / 橫濱 | 横浜 |

When user-provided names can match multiple stations, ask one clarification question before querying.

## Command Examples

Build URL only:

```bash
python3 scripts/build_norikae_url.py \
  --from 東京 --to 新宿 --via 表参道 \
  --year 2026 --month 3 --day 6 --hour 10 --minute 30 \
  --time-type departure --sort-by time
```

Fetch and extract plain text:

```bash
python3 scripts/fetch_norikae_routes.py \
  --from 東京 --to 新宿 --via 表参道 \
  --year 2026 --month 3 --day 6 --hour 10 --minute 30 \
  --time-type departure --sort-by time --show-url
```

Fetch from existing URL:

```bash
python3 scripts/fetch_norikae_routes.py --url 'https://transit.yahoo.co.jp/search/result?...' --show-url
```

Return HTML snippet:

```bash
python3 scripts/fetch_norikae_routes.py --url '<url>' --format html
```

## Extraction Strategy

- Remove noisy tags (`script`, `style`, comments, nav/header/footer/aside).
- Prefer range from `class="...routeDetail..."` to `条件を変更して検索`.
- Fall back to text extraction when structural markers are missing.
