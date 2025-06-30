# ddns

Monitor public IPs on routers and update dynamic DNS records.

## Documentation

All configuration is supplied through the CLI argument `-c`/`--config` using parameters and values specified below.

### Routers

Parameters to define the router whose public IP to resolve.

| Paremeter  | Type     | Required | Description |
|------------|----------|----------|-------------|
| `type`     | String   | Yes      | Type of router (see below). |
| `host`     | String   | Yes      | IP address of router. |
| `username` | String   | Depends  | Username to authenticate into the router. |
| `password` | String   | Depends  | Password to authenticate into the router. |

**List of supported routers**:

| Type       | Requires   | Description |
|------------|------------|-------------|
| `movistar` | `password` | Routers deployed by Spanish ISP [Movistar](https://www.movistar.es/) and affiliates, e.g. [O2](https://o2online.es/). Requires HTTP access. Tested with GPT-2741GNAC. |
| `turris`   | `username`, `password` | Routers manufactured by [Turris](https://www.turris.com/en/). Requires SSH access. Tested with Turris Omnia Wi-Fi 6. |

### DNS

Parameters to define DNS records to update.

| Paremeter  | Type     | Required | Description |
|------------|----------|----------|-------------|
| `name`     | String   | Yes      | Record name. |
| `type`     | String   | Yes      | Record type, e.g. `A` or `AAAA`. |
| `data`     | [String] | No       | Static record data to preserve during update (defaults to `[]`). |

**List of supported DNS providers**:

| Key        | Requires   | Description |
|------------|------------|-------------|
| `livedns`  | `key`      | [Gandi LiveDNS](https://www.gandi.net/en/domain/dns) services. |

## Example

Example configuration file:

```json
{
    "router": {
        "type": "movistar",
        "host": "192.168.1.1",
        "password": "123456"
    },
    "dns": [{
        "type": "livedns",
        "key": "1234ABCD5678WXYZ",
        "domains": [{
            "name": "example.com",
            "records": [{
                "name": "@",
                "type": "A",
                "data": ["127.0.0.1"]
            }, {
                "name": "test",
                "type": "A"
            }]
        }]
    }]
}
```
