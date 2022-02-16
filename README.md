# homeassistant-goecharger-mqtt

![GitHub actions](https://github.com/syssi/homeassistant-goecharger-mqtt/actions/workflows/pytest.yaml/badge.svg)
![GitHub actions](https://github.com/syssi/homeassistant-goecharger-mqtt/actions/workflows/hassfest.yaml/badge.svg)
![GitHub actions](https://github.com/syssi/homeassistant-goecharger-mqtt/actions/workflows/hacs.yaml/badge.svg)
![GitHub stars](https://img.shields.io/github/stars/syssi/homeassistant-goecharger-mqtt)
![GitHub forks](https://img.shields.io/github/forks/syssi/homeassistant-goecharger-mqtt)
![GitHub watchers](https://img.shields.io/github/watchers/syssi/homeassistant-goecharger-mqtt)
[!["Buy Me A Coffee"](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg)](https://www.buymeacoffee.com/syssi)

This is a custom component for Home Assistant to integrate the go-eCharger HOME+ and HOMEfix using the MQTT API (v2).

## Installation

Use HACS to install this custom component.

## Configuration

Use the Web UI (Config flow) to add the "go-eCharger" integration. You have to know the `serial number` (6 digits) of your device. Please don't forget to [enable the MQTT API (v2) via the go-e Charger app](https://github.com/goecharger/go-eCharger-API-v2/blob/main/mqtt-en.md) first.

## Binary sensors

| Topic | Friendly name | Category | Enabled per default | Supported | Unsupported reason |
| ----- | ------------- | -------- | ------------------- | --------- | ------------------ |
| `acp` | Allow charge pause | `config` | :heavy_check_mark: | :x: | [^1] |
| `ara` | Automatic stop mode | `config` | :heavy_check_mark: | :heavy_check_mark: | |
| `awe` | Awattar mode | `config` | :heavy_check_mark: | :x: | [^1] |
| `bac` | Allow current change by button | `config` | :heavy_check_mark: | :heavy_check_mark: | |
| `cca` | Cloud websocket use client auth | `config` | :white_large_square: | :x: | [^1] |
| `cwe` | Cloud websocket enabled | `config` | :white_large_square: | :x: | [^1] |
| `esk` | Energy set | `config` | :white_large_square: | :x: | App only |
| `hsa` | HTTP STA authentication | `config` | :white_large_square: | :x: | [^1] |
| `hws` | HTTP STA reachable | `config` | :white_large_square: | :x: | [^1] |
| `loe` | Load balancing enabled | `config` | :white_large_square: | :x: | [^1] |
| `lse` | Led save energy | `config` | :white_large_square: | :x: | [^1] |
| `nmo` | Norway mode | `config` | :white_large_square: | :x: | [^1] |
| `ocuca` | OTA cloud use client auth | `config` | :white_large_square: | :x: | [^1] |
| `sdp` | Button allow force change | `config` | :white_large_square: | :x: | [^1] |
| `su` | Simulate unplugging | `config` | :white_large_square: | :x: | [^1] |
| `tse` | Time server enabled | `config` | :white_large_square: | :x: | [^1] |
| `upo` | Unlock power outage | `config` | :white_large_square: | :x: | [^1] |
| `wen` | WiFi enabled | `config` | :white_large_square: | :x: | [^1] |
| `sbe` | Secure boot enabled |  | :white_large_square: | :x: | [^1] |
| `adi` | Is the 16a adapter used | `diagnostic` | :heavy_check_mark: | :heavy_check_mark: | |
| `alw` | Car allowed to charge | `diagnostic` | :heavy_check_mark: | :heavy_check_mark: | |
| `cpe` | Charge control requests the cp signal enabled or not immediately | `diagnostic` | :white_large_square: | :x: | [^1] |
| `cpr` | CP enable request | `diagnostic` | :white_large_square: | :x: | [^1] |
| `cws` | Cloud websocket started | `diagnostic` | :white_large_square: | :x: | [^1] |
| `cwsc` | Cloud websocket connected | `diagnostic` | :white_large_square: | :x: | [^1] |
| `fsp` | Force single phase | `diagnostic` | :heavy_check_mark: | :heavy_check_mark: | |
| `lwcf` | Last failed WiFi connect | `diagnostic` | :white_large_square: | :x: | [^1] |
| `tlf` | Test charging finished | `diagnostic` | :white_large_square: | :x: | [^1] |
| `tls` | Test charging started | `diagnostic` | :white_large_square: | :x: | [^1] |

## Sensors

| Key | Friendly name | Category | Unit | Enabled per default | Supported | Unsupported reason |
| --- | ------------- | -------- | ---- | ------------------- | --------- | ------------------ |
| `acs` | Access control user setting | `config` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `ama` | Maximum current limit | `config` | A | :heavy_check_mark: | :heavy_check_mark: | |
| `amp` | Requested current | `config` | A | :heavy_check_mark: | :heavy_check_mark: | |
| `ate` | Automatic stop energy | `config` | Wh | :heavy_check_mark: | :heavy_check_mark: | |
| `att` | Automatic stop time | `config` | s | :heavy_check_mark: | :heavy_check_mark: | |
| `awc` | Awattar country | `config` |  | :white_large_square: | :x: | [^1] |
| `awp` | Awattar maximum price threshold | `config` | ¢ | :white_large_square: | :heavy_check_mark: | |
| `cch` | Color charging | `config` |  | :white_large_square: | :heavy_check_mark: | |
| `cco` | Car consumption | `config` |  | :white_large_square: | :x: | App only |
| `cfi` | Color finished | `config` |  | :white_large_square: | :heavy_check_mark: | |
| `cid` | Color idle | `config` |  | :white_large_square: | :heavy_check_mark: | |
| `clp` | Current limit presets | `config` | A | :white_large_square: | :heavy_check_mark: | |
| `ct` | Car type | `config` |  | :white_large_square: | :x: | App only |
| `cwc` | Color wait for car | `config` |  | :white_large_square: | :heavy_check_mark: | |
| `dwo` | Charging energy limit | `config` | Wh | :heavy_check_mark: | :heavy_check_mark: | |
| `fna` | Friendly name | `config` |  | :white_large_square: | :x: | [^1] |
| `frc` | Force state | `config` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `frc` | Force state code | `config` |  | :white_large_square: | :heavy_check_mark: | |
| `lbr` | LED brightness | `config` |  | :white_large_square: | :heavy_check_mark: | |
| `lmo` | Logic mode | `config` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `lmo` | Logic mode code | `config` |  | :white_large_square: | :heavy_check_mark: | |
| `lof` | Load fallback | `config` |  | :white_large_square: | :x: | [^1] |
| `log` | Load group id | `config` |  | :white_large_square: | :x: | [^1] |
| `lop` | Load priority | `config` |  | :white_large_square: | :x: | [^1] |
| `lot` | Load balancing total ampere | `config` |  | :white_large_square: | :x: | [^1] |
| `loty` | Load balancing type | `config` |  | :white_large_square: | :x: | [^1] |
| `map` | Load mapping | `config` |  | :white_large_square: | :x: | [^1] |
| `mca` | Minimum charging current | `config` | A | :heavy_check_mark: | :heavy_check_mark: | |
| `mci` | Minimum charging interval | `config` | ms | :white_large_square: | :x: | [^1] |
| `mcpd` | Minimum charge pause duration | `config` | ms | :white_large_square: | :x: | [^1] |
| `mptwt` | Minimum phase toggle wait time | `config` | ms | :white_large_square: | :x: | [^1] |
| `mpwst` | Minimum phase wish switch time | `config` | ms | :white_large_square: | :x: | [^1] |
| `pass` | User password | `config` |  | :white_large_square: | :x: | [^1] |
| `psmd` | Force single phase duration | `config` | ms | :white_large_square: | :x: | [^1] |
| `sch_satur` | Scheduler saturday | `config` |  | :white_large_square: | :x: | [^1] |
| `sch_sund` | Scheduler sunday | `config` |  | :white_large_square: | :x: | [^1] |
| `sch_week` | Scheduler weekday | `config` |  | :white_large_square: | :x: | [^1] |
| `spl3` | Three phase switch level | `config` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `sumd` | Simulate unplugging duration | `config` | ms | :white_large_square: | :x: | [^1] |
| `tds` | Timezone daylight saving mode | `config` |  | :white_large_square: | :x: | [^1] |
| `tof` | Timezone offset in minutes | `config` |  | :white_large_square: | :x: | [^1] |
| `ts` | Time server | `config` |  | :white_large_square: | :x: | [^1] |
| `tssi` | Time server sync interval | `config` |  | :white_large_square: | :x: | [^1] |
| `tssm` | Time server sync mode | `config` |  | :white_large_square: | :x: | [^1] |
| `tsss` | Time server sync status | `config` |  | :white_large_square: | :x: | [^1] |
| `ust` | Unlock setting | `config` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `ust` | Unlock setting code | `config` |  | :white_large_square: | :heavy_check_mark: | |
| `wak` | WiFi accesspoint encryption key | `config` |  | :white_large_square: | :x: | [^1] |
| `wan` | WiFi accesspoint network name | `config` |  | :white_large_square: | :x: | [^1] |
| `wifis` | WiFi configurations | `config` |  | :white_large_square: | :x: | [^1] |
| `apd` | Firmware description |  |  | :white_large_square: | :x: | [^1] |
| `arv` | App recommended version |  |  | :white_large_square: | :x: | [^1] |
| `ecf` | ESP CPU frequency |  |  | :white_large_square: | :x: | [^1] |
| `eci` | ESP Chip info |  |  | :white_large_square: | :x: | [^1] |
| `eem` | ESP CPU frequency |  |  | :white_large_square: | :x: | [^1] |
| `efi` | ESP Flash info |  |  | :white_large_square: | :x: | [^1] |
| `facwak` | WiFi accesspoint key reset value |  |  | :white_large_square: | :x: | [^1] |
| `fem` | Flash encryption mode |  |  | :white_large_square: | :x: | [^1] |
| `ffna` | Factory friendly name |  |  | :white_large_square: | :x: | [^1] |
| `fwan` | Factory WiFi accesspoint network name |  |  | :white_large_square: | :x: | [^1] |
| `fwc` | Firmware from car control |  |  | :white_large_square: | :x: | [^1] |
| `fwv` | Firmware version |  |  | :white_large_square: | :heavy_check_mark: | |
| `mod` | Hardware version |  |  | :white_large_square: | :x: | [^1] |
| `oem` | Manufacturer |  |  | :white_large_square: | :x: | [^1] |
| `otap` | Active OTA partition |  |  | :white_large_square: | :x: | [^1] |
| `part` | Partition table |  |  | :white_large_square: | :x: | [^1] |
| `pto` | Partition table offset in flash |  |  | :white_large_square: | :x: | [^1] |
| `sse` | Serial number |  |  | :white_large_square: | :x: | [^1] |
| `typ` | Device type |  |  | :white_large_square: | :x: | [^1] |
| `var` | Device variant |  | kW | :white_large_square: | :heavy_check_mark: | |
| `del` | Delete card | `config` |  | :white_large_square: | :x: | [^1] |
| `delw` | Delete STA config | `config` |  | :white_large_square: | :x: | [^1] |
| `lrn` | Learn card | `config` |  | :white_large_square: | :x: | [^1] |
| `oct` | Firmware update trigger | `config` |  | :white_large_square: | :x: | [^1] |
| `acu` | Maximum allowed current | `diagnostic` | A | :heavy_check_mark: | :heavy_check_mark: | |
| `amt` | Current temperature limit | `diagnostic` | °C | :heavy_check_mark: | :heavy_check_mark: | |
| `atp` | Next trip plan data | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `awcp` | Awattar current price | `diagnostic` |  | :white_large_square: | :heavy_check_mark: | |
| `awpl` | Awattar price list | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `car` | Car state | `diagnostic` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `cbl` | Cable maximum current limit | `diagnostic` | A | :white_large_square: | :heavy_check_mark: | |
| `ccu` | Charge controller update progress | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `ccw` | Connected WiFi | `diagnostic` |  | :white_large_square: | :x: | JSON decoding required. Values non-essential |
| `cdi` | Charging duration info | `diagnostic` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `cus` | Cable unlock status | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `cwsca` | Cloud websocket connected | `diagnostic` | ms | :white_large_square: | :x: | [^1] |
| `efh` | ESP free heap | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `efh32` | ESP free heap 32bit aligned | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `efh8` | ESP free heap 8bit aligned | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `ehs` | ESP heap size | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `emfh` | ESP minimum free heap since boot | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `emhb` | ESP maximum size of allocated heap block since boot | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `err` | Error | `diagnostic` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `err` | Error code | `diagnostic` |  | :white_large_square: | :heavy_check_mark: | |
| `esr` | RTC reset reason | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `eto` | Total energy | `diagnostic` | Wh | :heavy_check_mark: | :heavy_check_mark: | |
| `etop` | Total energy persisted | `diagnostic` | Wh | :white_large_square: | :x: | [^1] |
| `ffb` | Lock feedback | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `ffba` | Lock feedback age | `diagnostic` | ms | :white_large_square: | :x: | [^1] |
| `fhz` | Grid frequency | `diagnostic` | Hz | :white_large_square: | :heavy_check_mark: | |
| `fsptws` | Force single phase toggle wished since | `diagnostic` | ms | :white_large_square: | :x: | [^1] |
| `host` | Hostname on STA interface | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `lbp` | Last button press | `diagnostic` |  | :white_large_square: | :heavy_check_mark: | |
| `lccfc` | Last car state changed from charging | `diagnostic` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `lccfi` | Last car state changed from idle | `diagnostic` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `lcctc` | Last car state changed to charging | `diagnostic` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `lck` | Effective lock setting | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `led` | LED animation details | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `lfspt` | Last force single phase toggle | `diagnostic` | ms | :white_large_square: | :x: | [^1] |
| `lmsc` | Last model status change | `diagnostic` | ms | :white_large_square: | :heavy_check_mark: | |
| `loa` | Load balancing ampere | `diagnostic` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `loc` | Local time | `diagnostic` |  | :white_large_square: | :x: | Valueless with a high update interval of 1s |
| `lom` | Load balancing members | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `los` | Load balancing status | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `lssfc` | WiFi station disconnected since | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `lsstc` | WiFi station connected since | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `mcpea` | Minimum charge pause ends at | `diagnostic` | ms | :white_large_square: | :x: | [^1] |
| `mmp` | Maximum measured charging power | `diagnostic` | W | :white_large_square: | :x: | [^1] |
| `modelStatus` | Status | `diagnostic` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `modelStatus` | Status code | `diagnostic` |  | :white_large_square: | :heavy_check_mark: | |
| `msi` | Reason why we allow charging or not | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `nrg` | Voltage L1 | `diagnostic` | V | :heavy_check_mark: | :heavy_check_mark: | |
| `nrg` | Voltage L2 | `diagnostic` | V | :heavy_check_mark: | :heavy_check_mark: | |
| `nrg` | Voltage L3 | `diagnostic` | V | :heavy_check_mark: | :heavy_check_mark: | |
| `nrg` | Voltage N | `diagnostic` | V | :heavy_check_mark: | :heavy_check_mark: | |
| `nrg` | Current L1 | `diagnostic` | A | :heavy_check_mark: | :heavy_check_mark: | |
| `nrg` | Current L2 | `diagnostic` | A | :heavy_check_mark: | :heavy_check_mark: | |
| `nrg` | Current L3 | `diagnostic` | A | :heavy_check_mark: | :heavy_check_mark: | |
| `nrg` | Power L1 | `diagnostic` | kW | :heavy_check_mark: | :heavy_check_mark: | |
| `nrg` | Power L2 | `diagnostic` | kW | :heavy_check_mark: | :heavy_check_mark: | |
| `nrg` | Power L3 | `diagnostic` | kW | :heavy_check_mark: | :heavy_check_mark: | |
| `nrg` | Power N | `diagnostic` | kW | :heavy_check_mark: | :heavy_check_mark: | |
| `nrg` | Power total | `diagnostic` | kW | :heavy_check_mark: | :heavy_check_mark: | |
| `nrg` | Power factor L1 | `diagnostic` | % | :heavy_check_mark: | :heavy_check_mark: | |
| `nrg` | Power factor L2 | `diagnostic` | % | :heavy_check_mark: | :heavy_check_mark: | |
| `nrg` | Power factor L3 | `diagnostic` | % | :heavy_check_mark: | :heavy_check_mark: | |
| `nrg` | Power factor N | `diagnostic` | % | :heavy_check_mark: | :heavy_check_mark: | |
| `oca` | OTA cloud app description | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `ocl` | OTA from cloud length | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `ocm` | OTA from cloud message | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `ocp` | OTA from cloud progress | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `ocs` | OTA from cloud status | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `ocu` | List of available firmware versions | `diagnostic` |  | :white_large_square: | :heavy_check_mark: | |
| `onv` | Newest OTA version | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `pha` | Phases | `diagnostic` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `pwm` | Phase wish mode for debugging | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `qsc` | Queue size cloud | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `qsw` | Queue size web | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `rbc` | Reboot counter | `diagnostic` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `rbt` | Uptime | `diagnostic` |  | :white_large_square: | :x: | TODO: Convert to a timestamp first |
| `rcd` | Residual current detection | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `rfb` | Relay feedback | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `rr` | ESP reset reason | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `rssi` | WiFi signal strength | `diagnostic` | dBm | :white_large_square: | :heavy_check_mark: | |
| `scaa` | WiFi scan age | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `scan` | WiFi scan result | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `scas` | WiFi scan status | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `tma` | Temperature sensor 1 | `diagnostic` | °C | :heavy_check_mark: | :heavy_check_mark: | |
| `tma` | Temperature sensor 2 | `diagnostic` | °C | :heavy_check_mark: | :heavy_check_mark: | |
| `tpa` | Total power average | `diagnostic` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `trx` | Transaction | `diagnostic` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `tsom` | Time server operating mode | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `utc` | UTC time | `diagnostic` |  | :white_large_square: | :x: | Valueless with a high update interval of 1s |
| `wcch` | Clients via http | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `wccw` | Clients via websocket | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `wh` | Energy since car connected | `diagnostic` | Wh | :heavy_check_mark: | :heavy_check_mark: | |
| `wsms` | WiFi state machine state | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `wst` | WiFi station status | `diagnostic` |  | :white_large_square: | :x: | [^1] |
| `psm` | Configured phases | `config` |  | :heavy_check_mark: | :heavy_check_mark: | |

[^1]: Not exposed via MQTT in firmware 053.1

## References

* https://github.com/goecharger/go-eCharger-API-v2/blob/main/mqtt-en.md
* https://github.com/goecharger/go-eCharger-API-v2/blob/main/apikeys-en.md
* https://github.com/boralyl/github-custom-component-tutorial
