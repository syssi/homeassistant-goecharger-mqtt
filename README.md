# homeassistant-goecharger-mqtt

![GitHub actions](https://github.com/syssi/homeassistant-goecharger-mqtt/actions/workflows/pytest.yaml/badge.svg)
![GitHub actions](https://github.com/syssi/homeassistant-goecharger-mqtt/actions/workflows/hassfest.yaml/badge.svg)
![GitHub actions](https://github.com/syssi/homeassistant-goecharger-mqtt/actions/workflows/hacs.yaml/badge.svg)
![GitHub stars](https://img.shields.io/github/stars/syssi/homeassistant-goecharger-mqtt)
![GitHub forks](https://img.shields.io/github/forks/syssi/homeassistant-goecharger-mqtt)
![GitHub watchers](https://img.shields.io/github/watchers/syssi/homeassistant-goecharger-mqtt)
[!["Buy Me A Coffee"](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg)](https://www.buymeacoffee.com/syssi)

This is a custom component for Home Assistant to integrate the go-eCharger HOME+, HOMEfix and Gemini using the MQTT API (v1 and v2). If you are using the go-eController there's [another project](https://github.com/karloskar/homeassistant-goecontroller-mqtt) covering that.

![Lovelace entities card](assets/lovelace-entities-card.png "Lovelace entities card")

## Setup and Configuration

1. Use HACS to install this custom component
1. Restart HA
1. Make sure you have an MQTT Broker ([e.g. Mosquitto broker](https://github.com/eclipse/mosquitto)) and a working [MQTT integration](https://www.home-assistant.io/integrations/mqtt/) in HA
1. (Recommended) Access to messages on MQTT Broker via client such as [MQTT Explorer](https://mqtt-explorer.com/)  
1. Enable the MQTT API of your charger at the [go-eCharger App](https://play.google.com/store/apps/details?id=co.goe.app&hl=de)
    - `Internet` -> `Advanced settings` -> scroll to bottom -> `Enable MQTT API` ([See also here](https://github.com/goecharger/go-eCharger-API-v2/blob/main/mqtt-en.md))
    - at the field `URL` enter your MQTT broker URL, e.g. mqtt://192.168.178.3:1883 for a broker running on a server with IP 192.168.178.3 on default port 1883
    ![alt text](assets/goe_app_settings.jpg)
    - (optional) Add MQTT keys and certificates as needed
    - Press the `SAVE` symbol in the top right to apply the settings
1. (Optional) Make sure you see a new topic on the MQTT broker using your MQTT client
    - New messages appear under `go-eCharger/[your serial number]/`
1. In HA, add new integration 
    - `Settings` -> `Devices & services` -> `ADD INTEGRATION` -> `go-eCharger (MQTT)`
    - enter serial number (6 digits) of your device (find via App or MQTT client)
    - make sure base topic matches what you see in the MQTT broker, in some cases the default `/go-eCharger` has to be changed to `go-eCharger`
1. See your go-e data pour into HA

### Alternative Installation Method (without HACS)

If you don't want to or cannot use HACS, you can install the integration manually:

1. Download the latest release from the [releases page](https://github.com/syssi/homeassistant-goecharger-mqtt/releases) or clone the repository
2. Copy the directory `/custom_components/goecharger_mqtt` from the repository to the `/custom_components` directory in your Home Assistant configuration folder:
   ```
   In your HA config directory:
   custom_components
   ├── goecharger_mqtt
   │   ├── __init__.py
   ...
   ```
3. Continue with step 2 "Restart HA" from the main instructions above

This manual method achieves the same result as the HACS installation but requires more manual effort and doesn't provide automatic updates like HACS does.

## Entities

### Binary sensors

| Topic | Friendly name | Category | Enabled per default | Supported | Unsupported reason |
| ----- | ------------- | -------- | ------------------- | --------- | ------------------ |
| `car` | Car connected | `diagnostic` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `pha` | Phase L1 after contactor | `diagnostic` | :white_large_square: | :heavy_check_mark: | |
| `pha` | Phase L2 after contactor | `diagnostic` | :white_large_square: | :heavy_check_mark: | |
| `pha` | Phase L3 after contactor | `diagnostic` | :white_large_square: | :heavy_check_mark: | |
| `pha` | Phase L1 before contactor | `diagnostic` | :white_large_square: | :heavy_check_mark: | |
| `pha` | Phase L2 before contactor | `diagnostic` | :white_large_square: | :heavy_check_mark: | |
| `pha` | Phase L3 before contactor | `diagnostic` | :white_large_square: | :heavy_check_mark: | |
| `cca` | Cloud websocket use client auth | `config` | :white_large_square: | :white_large_square: | [^1] [^3] |
| `ocuca` | OTA cloud use client auth | `config` | :white_large_square: | :white_large_square: | [^1] [^3] |
| `sbe` | Secure boot enabled |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `adi` | 16A adapter attached | `diagnostic` | :heavy_check_mark: | :heavy_check_mark: | |
| `cpe` | Charge control requests the cp signal enabled or not immediately | `diagnostic` | :white_large_square: | :white_large_square: | [^1] [^3] |
| `cpr` | CP enable request | `diagnostic` | :white_large_square: | :white_large_square: | [^1] [^3] |
| `cws` | Cloud websocket started | `diagnostic` | :white_large_square: | :white_large_square: | [^1] [^3] |
| `cwsc` | Cloud websocket connected | `diagnostic` | :white_large_square: | :white_large_square: | [^1] [^3] |
| `fsp` | Force single phase | `diagnostic` | :heavy_check_mark: | :heavy_check_mark: | Is always false. Please use `psm` instead [^3] |
| `lwcf` | Last failed WiFi connect | `diagnostic` | :white_large_square: | :white_large_square: | [^1] [^3] |
| `tlf` | Test charging finished | `diagnostic` | :white_large_square: | :white_large_square: | [^1] [^3] |
| `tls` | Test charging started | `diagnostic` | :white_large_square: | :white_large_square: | [^1] [^3] |
| `sua` | Simulate unplugging permanently | `config` | :white_large_square: | :white_large_square: | [^1] [^3] |

### Buttons

| Topic | Friendly name | Category | Enabled per default | Supported | Unsupported reason |
| ----- | ------------- | -------- | ------------------- | --------- | ------------------ |
| `rst` | Restart device | `config` | :heavy_check_mark:  | :heavy_check_mark: | [^3] |
| `frc` | Force state neutral | `config` | :white_large_square: | :heavy_check_mark: | [^3] |
| `frc` | Force state dont charge | `config` | :white_large_square: | :heavy_check_mark: | [^3] |
| `frc` | Force state charge | `config` | :white_large_square: | :heavy_check_mark: | [^3] |
| `dwo` | Clear energy limit | `config` | :heavy_check_mark:  | :heavy_check_mark: | |

### Sensors

| Key | Friendly name | Category | Unit | Enabled per default | Supported | Unsupported reason |
| --- | ------------- | -------- | ---- | ------------------- | --------- | ------------------ |
| `+/result` | Last set config key result | `config` |  | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `ate` | Automatic stop energy | `config` | Wh | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `att` | Automatic stop time | `config` | s | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `awc` | Awattar country | `config` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `awp` | Awattar maximum price threshold | `config` | ¢ | :white_large_square: | :heavy_check_mark: | [^3] |
| `cch` | Color charging | `config` |  | :white_large_square: | :heavy_check_mark: | |
| `cco` | Car consumption | `config` |  | :white_large_square: | :white_large_square: | App only |
| `cfi` | Color finished | `config` |  | :white_large_square: | :heavy_check_mark: | |
| `cid` | Color idle | `config` |  | :white_large_square: | :heavy_check_mark: | |
| `clp` | Current limit presets | `config` | A | :white_large_square: | :heavy_check_mark: | [^3] |
| `ct` | Car type | `config` |  | :white_large_square: | :white_large_square: | App only [^3] |
| `cwc` | Color wait for car | `config` |  | :white_large_square: | :heavy_check_mark: | [^3] |
| `fna` | Friendly name | `config` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `frc` | Force state | `config` |  | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `frc` | Force state code | `config` |  | :white_large_square: | :heavy_check_mark: | [^3] |
| `lbr` | LED brightness | `config` |  | :white_large_square: | :heavy_check_mark: | |
| `lmo` | Logic mode | `config` |  | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `lof` | Load balancing fallback current | `config` | A | :white_large_square: | :white_large_square: | [^1] |
| `log` | Load balancing group id | `config` |  | :white_large_square: | :white_large_square: | [^1] |
| `lop` | Load balancing priority | `config` |  | :white_large_square: | :white_large_square: | [^1] |
| `lot` | Load balancing total ampere | `config` | A | :white_large_square: | :white_large_square: | [^1] |
| `loty` | Load balancing type | `config` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `map` | Load mapping | `config` |  | :white_large_square: | :white_large_square: | [^1] |
| `mca` | Minimum charging current | `config` | A | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `mci` | Minimum charging interval | `config` | ms | :white_large_square: | :white_large_square: | [^1] [^3] |
| `mcpd` | Minimum charge pause duration | `config` | ms | :white_large_square: | :white_large_square: | [^1] [^3] |
| `mptwt` | Minimum phase toggle wait time | `config` | ms | :white_large_square: | :white_large_square: | [^1] [^3] |
| `mpwst` | Minimum phase wish switch time | `config` | ms | :white_large_square: | :white_large_square: | [^1] [^3] |
| `pass` | User password | `config` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `psmd` | Force single phase duration | `config` | ms | :white_large_square: | :white_large_square: | [^1] [^3] |
| `sch_satur` | Scheduler saturday | `config` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `sch_sund` | Scheduler sunday | `config` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `sch_week` | Scheduler weekday | `config` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `spl3` | Three phase switch level | `config` | W | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `sumd` | Simulate unplugging duration | `config` | ms | :white_large_square: | :white_large_square: | [^1] [^3] |
| `tds` | Timezone daylight saving mode | `config` |  | :white_large_square: | :white_large_square: | [^1] |
| `tof` | Timezone offset in minutes | `config` |  | :white_large_square: | :white_large_square: | [^1] |
| `ts` | Time server | `config` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `tssi` | Time server sync interval | `config` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `tssm` | Time server sync mode | `config` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `tsss` | Time server sync status | `config` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `ust` | Cable unlock mode | `config` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `ust` | Cable unlock mode code | `config` |  | :white_large_square: | :heavy_check_mark: | |
| `wak` | WiFi accesspoint encryption key | `config` |  | :white_large_square: | :white_large_square: | [^1] |
| `wan` | WiFi accesspoint network name | `config` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `wifis` | WiFi configurations | `config` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `apd` | Firmware description |  |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `arv` | App recommended version |  |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `ecf` | ESP CPU frequency |  |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `eci` | ESP Chip info |  |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `eem` | ESP CPU frequency |  |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `efi` | ESP Flash info |  |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `facwak` | WiFi accesspoint key reset value |  |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `fem` | Flash encryption mode |  |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `ffna` | Factory friendly name |  |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `fwan` | Factory WiFi accesspoint network name |  |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `fwc` | Firmware from car control |  |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `fwv` | Firmware version |  |  | :white_large_square: | :heavy_check_mark: | |
| `mod` | Hardware version |  |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `oem` | Manufacturer |  |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `otap` | Active OTA partition |  |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `part` | Partition table |  |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `pto` | Partition table offset in flash |  |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `sse` | Serial number |  |  | :white_large_square: | :white_large_square: | [^1] |
| `typ` | Device type |  |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `var` | Device variant |  | kW | :white_large_square: | :heavy_check_mark: | [^3] |
| `del` | Delete card | `config` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `delw` | Delete STA config | `config` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `lrn` | Learn card | `config` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `oct` | Firmware update trigger | `config` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `acu` | Maximum allowed current | `diagnostic` | A | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `amt` | Current temperature limit | `diagnostic` | °C | :heavy_check_mark: | :heavy_check_mark: | |
| `atp` | Next trip plan data | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `awcp` | Awattar current price | `diagnostic` | ¢ | :white_large_square: | :heavy_check_mark: | [^3] |
| `awpl` | Awattar price list | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `car` | Car state | `diagnostic` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `cbl` | Cable maximum current | `diagnostic` | A | :white_large_square: | :heavy_check_mark: | |
| `ccu` | Charge controller update progress | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `ccw` | Connected WiFi | `diagnostic` |  | :white_large_square: | :white_large_square: | JSON decoding required. Values non-essential [^3] |
| `cdi` | Charging duration | `diagnostic` | ms | :heavy_check_mark: | :heavy_check_mark: | |
| `cdi` | Charging duration counter | `diagnostic` |  | :white_large_square: | :heavy_check_mark: | |
| `cus` | Cable unlock status code | `diagnostic` |  | :white_large_square: | :heavy_check_mark: | [^3] |
| `cus` | Cable unlock status | `diagnostic` |  | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `cwsca` | Cloud websocket connected | `diagnostic` | ms | :white_large_square: | :white_large_square: | [^1] [^3] |
| `efh` | ESP free heap | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `efh32` | ESP free heap 32bit aligned | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `efh8` | ESP free heap 8bit aligned | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `ehs` | ESP heap size | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `emfh` | ESP minimum free heap since boot | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `emhb` | ESP maximum size of allocated heap block since boot | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `err` | Error | `diagnostic` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `err` | Error code | `diagnostic` |  | :white_large_square: | :heavy_check_mark: | |
| `esr` | RTC reset reason | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `dws` | Charged energy this session | `diagnostic` | Wh | :heavy_check_mark: | :white_large_square: | [^4] [^5] |
| `eto` | Total energy | `diagnostic` | Wh | :heavy_check_mark: | :heavy_check_mark: | [^5] |
| `etop` | Total energy persisted | `diagnostic` | Wh | :white_large_square: | :white_large_square: | [^1] [^3] |
| `ffb` | Lock feedback | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `ffba` | Lock feedback age | `diagnostic` | ms | :white_large_square: | :white_large_square: | [^1] [^3] |
| `fhz` | Grid frequency | `diagnostic` | Hz | :white_large_square: | :heavy_check_mark: | [^3] |
| `fsptws` | Force single phase toggle wished since | `diagnostic` | ms | :white_large_square: | :white_large_square: | [^1] [^3] |
| `host` | Hostname on STA interface | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `lbp` | Last button press | `diagnostic` |  | :white_large_square: | :heavy_check_mark: | [^3] |
| `lccfc` | Last car state changed from charging | `diagnostic` | ms | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `lccfi` | Last car state changed from idle | `diagnostic` | ms | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `lcctc` | Last car state changed to charging | `diagnostic` | ms | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `lck` | Effective lock setting | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `led` | LED animation details | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `lfspt` | Last force single phase toggle | `diagnostic` | ms | :white_large_square: | :white_large_square: | [^1] [^3] |
| `lmsc` | Last model status change | `diagnostic` | ms | :white_large_square: | :heavy_check_mark: | [^3] |
| `loa` | Load balancing available current | `diagnostic` | A | :heavy_check_mark: | :heavy_check_mark: | |
| `loc` | Local time | `diagnostic` |  | :white_large_square: | :white_large_square: | Valueless with a high update interval of 1s [^3] |
| `lom` | Load balancing members | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] |
| `los` | Load balancing status | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] |
| `lssfc` | WiFi station disconnected since | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `lsstc` | WiFi station connected since | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `mcpea` | Minimum charge pause ends at | `diagnostic` | ms | :white_large_square: | :white_large_square: | [^1] [^3] |
| `mmp` | Maximum measured charging power | `diagnostic` | W | :white_large_square: | :white_large_square: | [^1] [^3] |
| `modelStatus` | Status | `diagnostic` |  | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `modelStatus` | Status code | `diagnostic` |  | :white_large_square: | :heavy_check_mark: | [^3] |
| `msi` | Reason why we allow charging or not | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `nrg` | Voltage L1 | `diagnostic` | V | :heavy_check_mark: | :heavy_check_mark: | [^5] |
| `nrg` | Voltage L2 | `diagnostic` | V | :heavy_check_mark: | :heavy_check_mark: | [^5] |
| `nrg` | Voltage L3 | `diagnostic` | V | :heavy_check_mark: | :heavy_check_mark: | [^5] |
| `nrg` | Voltage N | `diagnostic` | V | :heavy_check_mark: | :heavy_check_mark: | [^5] |
| `nrg` | Current L1 | `diagnostic` | A | :heavy_check_mark: | :heavy_check_mark: | [^5] |
| `nrg` | Current L2 | `diagnostic` | A | :heavy_check_mark: | :heavy_check_mark: | [^5] |
| `nrg` | Current L3 | `diagnostic` | A | :heavy_check_mark: | :heavy_check_mark: | [^5] |
| `nrg` | Power L1 | `diagnostic` | W | :heavy_check_mark: | :heavy_check_mark: | [^5] |
| `nrg` | Power L2 | `diagnostic` | W | :heavy_check_mark: | :heavy_check_mark: | [^5] |
| `nrg` | Power L3 | `diagnostic` | W | :heavy_check_mark: | :heavy_check_mark: | [^5] |
| `nrg` | Power N | `diagnostic` | W | :heavy_check_mark: | :heavy_check_mark: | [^5] |
| `nrg` | Current power | `diagnostic` | W | :heavy_check_mark: | :heavy_check_mark: | [^5] |
| `nrg` | Power factor L1 | `diagnostic` | % | :heavy_check_mark: | :heavy_check_mark: | [^5] |
| `nrg` | Power factor L2 | `diagnostic` | % | :heavy_check_mark: | :heavy_check_mark: | [^5] |
| `nrg` | Power factor L3 | `diagnostic` | % | :heavy_check_mark: | :heavy_check_mark: | [^5] |
| `nrg` | Power factor N | `diagnostic` | % | :heavy_check_mark: | :heavy_check_mark: | [^5] |
| `oca` | OTA cloud app description | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `ocl` | OTA from cloud length | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `ocm` | OTA from cloud message | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `ocp` | OTA from cloud progress | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `ocs` | OTA from cloud status | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `ocu` | List of available firmware versions | `diagnostic` |  | :white_large_square: | :heavy_check_mark: | [^3] |
| `onv` | Newest OTA version | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `pwm` | Phase wish mode for debugging | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `pgrid` | Power from Grid |  |  | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `ppv` | Power from Solar Panels |  |  | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `pakku` | Power from External Battery |  |  | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `qsc` | Queue size cloud | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `qsw` | Queue size web | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `rbc` | Reboot counter | `diagnostic` |  | :heavy_check_mark: | :heavy_check_mark: | |
| `rbt` | Uptime | `diagnostic` |  | :white_large_square: | :white_large_square: | TODO: Convert to a timestamp first |
| `rcd` | Residual current detection | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] |
| `rfb` | Relay feedback | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `rr` | ESP reset reason | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `rssi` | WiFi signal strength | `diagnostic` | dBm | :white_large_square: | :heavy_check_mark: | [^3] |
| `scaa` | WiFi scan age | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `scan` | WiFi scan result | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `scas` | WiFi scan status | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `tma` | Temperature sensor 1 | `diagnostic` | °C | :heavy_check_mark: | :heavy_check_mark: | |
| `tma` | Temperature sensor 2 | `diagnostic` | °C | :heavy_check_mark: | :heavy_check_mark: | |
| `tpa` | Total power average | `diagnostic` | W | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `trx` | Transaction | `diagnostic` |  | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `tsom` | Time server operating mode | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `utc` | UTC time | `diagnostic` |  | :white_large_square: | :white_large_square: | Valueless with a high update interval of 1s [^3] |
| `wcch` | Clients via http | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `wccw` | Clients via websocket | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `wh` | Charged energy | `diagnostic` | Wh | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `wsms` | WiFi state machine state | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] [^3] |
| `wst` | WiFi station status | `diagnostic` |  | :white_large_square: | :white_large_square: | [^1] |
| `psm` | Configured phases | `config` |  | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `cards` | Charged energy card 1 | `diagnostic` | Wh | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `cards` | Charged energy card 2 | `diagnostic` | Wh | :white_large_square: | :heavy_check_mark: | [^3] |
| `cards` | Charged energy card 3 | `diagnostic` | Wh | :white_large_square: | :heavy_check_mark: | [^3] |
| `cards` | Charged energy card 4 | `diagnostic` | Wh | :white_large_square: | :heavy_check_mark: | [^3] |
| `cards` | Charged energy card 5 | `diagnostic` | Wh | :white_large_square: | :heavy_check_mark: | [^3] |
| `cards` | Charged energy card 6 | `diagnostic` | Wh | :white_large_square: | :heavy_check_mark: | [^3] |
| `cards` | Charged energy card 7 | `diagnostic` | Wh | :white_large_square: | :heavy_check_mark: | [^3] |
| `cards` | Charged energy card 8 | `diagnostic` | Wh | :white_large_square: | :heavy_check_mark: | [^3] |
| `cards` | Charged energy card 9 | `diagnostic` | Wh | :white_large_square: | :heavy_check_mark: | [^3] |
| `cards` | Charged energy card 10 | `diagnostic` | Wh | :white_large_square: | :heavy_check_mark: | [^3] |

### Switch entities

| Key | Friendly name | Category | Enabled per default | Supported | Unsupported reason |
| --- | ------------- | -------- | ------------------- | --------- | ------------------ |
| `alw` | Allow charging | `config` | :heavy_check_mark: | :heavy_check_mark: | [^4] |
| `ara` | Automatic stop mode | `config` | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `wen` | WiFi enabled | `config` | :white_large_square: | :white_large_square: | [^1] |
| `tse` | Time server enabled | `config` | :white_large_square: | :white_large_square: | [^1] [^3] |
| `nmo` | Norway mode | `config` | :white_large_square: | :white_large_square: | [^1] |
| `lse` | LED off on standby | `config` | :white_large_square: | :white_large_square: | [^1] |
| `awe` | Awattar mode | `config` | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `acp` | Allow charge pause | `config` | :heavy_check_mark: | :white_large_square: | [^1] [^3] |
| `esk` | Energy set | `config` | :white_large_square: | :white_large_square: | App only [^3] |
| `fup` | Charge with PV surplus | `config` | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `fzf` | Zero feedin | `config` | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `su` | Simulate unplugging | `config` | :white_large_square: | :white_large_square: | [^1] [^3] |
| `hws` | HTTP STA reachable | `config` | :white_large_square: | :white_large_square: | [^1] [^3] |
| `hsa` | HTTP STA authentication | `config` | :white_large_square: | :white_large_square: | [^1] [^3] |
| `loe` | Load balancing enabled | `config` | :white_large_square: | :white_large_square: | [^1] |
| `upo` | Unlock power outage | `config` | :white_large_square: | :white_large_square: | [^1] [^3] |
| `cwe` | Cloud websocket enabled | `config` | :white_large_square: | :white_large_square: | [^1] [^3] |
| `psm` | Force single phase | `diagnostic` | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `acs` | Card authorization required | `config` | :heavy_check_mark: | :heavy_check_mark: | [^3] |

### Number entities

| Key | Friendly name | Category | Enabled per default | Supported | Unsupported reason |
| --- | ------------- | -------- | ------------------- | --------- | ------------------ |
| `ama` | Maximum current limit | `config` | :heavy_check_mark: | :heavy_check_mark: | |
| `amp` | Requested current | `config` | :heavy_check_mark: | :heavy_check_mark: | |
| `ate` | Automatic stop energy | `config` | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `att` | Automatic stop time | `config` | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `awp` | Awattar maximum price threshold | `config` | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `dwo` | Charging energy limit | `config` | :heavy_check_mark: | :heavy_check_mark: | [^5] |
| `lop` | Load balancing priority | `config` | :white_large_square: | :white_large_square: | [^1] |
| `pgt` | Grid target | `config` | :heavy_check_mark: | :heavy_check_mark: | [^2] [^3] |
| `fst` | PV surplus starting power | `config` | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `sh` | PV surplus stop hysteresis | `config` | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `psh` | PV surplus phase switch hysteresis | `config` | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `po` | PV surplus power offset | `config` | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `zfo` | Zero feedin offset | `config` | :heavy_check_mark: | :heavy_check_mark: | [^3] |

### Select entities

| Key | Friendly name | Category | Enabled per default | Supported | Unsupported reason |
| --- | ------------- | -------- | ------------------- | --------- | ------------------ |
| `bac` | Button allow current change | `config` | :heavy_check_mark: | :heavy_check_mark: | Values: `always_lock` / `lock_when_car_connected` / `lock_when_charging` / `never_lock` [^3] |
| `sdp` | Button allow force change | `config` | :heavy_check_mark: | :heavy_check_mark: | Values: `always_lock` / `lock_when_car_connected` / `lock_when_charging` / `never_lock` |
| `lmo` | Logic mode | `config` | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `psm` | Phase switch mode | `config` | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `ust` | Cable unlock mode | `config` | :heavy_check_mark: | :heavy_check_mark: | |
| `frc` | Force state | `config` | :heavy_check_mark: | :heavy_check_mark: | [^3] |
| `trx` | Transaction | `config` | :heavy_check_mark: | :heavy_check_mark: | [^3] |

## Charge with PV Surplus

### Setable only PV-surplus entities

This feature requires firmware 0.55.6 or newer.

| Key | Friendly name | Category | Enabled per default | Supported | Unsupported reason |
| --- | ------------- | -------- | ------------------- | --------- | ------------------ |
| `ids` | Input avail Power | `config` | :white_large_square:  | :heavy_check_mark:  | [^3] |

`ids` is used to input values to the ECO PV-surplus charging mode. (PV = Photo Voltaic aka Solar Panels)

`ids` is set with a JSON list: `{"pGrid":0.0,"pAkku":0.0,"pPv":0.0}` - If values are accepted they can be read back thru the `pgrid`, `pakku` and `ppv` sensors. `pGrid` is required. The others are optional.

`ids` values decays, so must be updated every 10s or faster. No update for 10-15s means no PV-surplus is available. `pgrid`/`pakku`/`ppv` will thus all become `unknown`.

Only `pGrid` is used in calculations. Negative `pGrid` means power is exported, and thus available to the charger. Charger is then constantly calculating available power and adjusting charge power up and down multiple times per minute (on every update). If 1/3 phase is set to automatic, it will switch between 1 and 3 phases. The 1->3 phase switch level is set in `spl3`

By feeding `ids` values, ECO charging can be controlled (on/off) in the go-eCharger App. It is safe and expected to set this value often.

For PV surplus charging to be enabled, `lmo` (Logic mode) most be set to 4 (Eco mode), and `fup` (Use PV surplus) must be set to true.

See template example below for how to continuously update `ids`

#### Automation example
```
alias: go-e Surplus Charging
description: "Simple automation to update values needed for using solar surplus with go-e Chargers"
trigger:
  - platform: time_pattern
    seconds: /5
condition: []
action:
  - action: goecharger_mqtt.update_grid_power
      # Change to your device ID here
      device_id: !input wallbox_id
      # Please provide your own entities here, as described above
      power_grid: "{{ states('sensor.meter_active_power') | float }}"
      power_pv: "{{ states('sensor.total_dc_power') | float }}"
      power_battery: "{{ states('sensor.battery_power') | float }}"
```

## Platform services

### Service `goecharger_mqtt.set_config_key`

Sets a config `key` to a `value` by publishing to `{topic}/{key}/set`.

| Service data attribute    | Optional | Description                                                          |
|---------------------------|----------|----------------------------------------------------------------------|
| `device_id`               |       no | The go-eCharger device to configure                                  |
| `key`                     |       no | The key of the config parameter you want to change                   |
| `value`                   |       no | The new value                                                        |

`value` is a string (or YAML `null`). Numeric values are published as-is. The strings `true`/`True` and `false`/`False` are published as lowercase booleans. `null`/`none` (and YAML `null`) are published as JSON `null` — required to clear nullable keys such as `trx`. Any other string is JSON-quoted.

## Tips and tricks

### How to suspend the access point of the go-e charger

Per default the WiFi network of the charger is always active even if the device is connected as station to your
WiFi network. If `cloud access` is enabled the API key `wda` can be used to suspend the access point as soon
as the connection to the cloud is established:

```
# Suspend access point mode on cloud connection
curl -s "http://192.168.xx.xx/api/set?wda=true"

# Pretty print the full status
curl -s "http://192.168.xx.xx/api/status" | json_pp

# Check the value of the `wda` key
curl -s "http://192.168.1.11/api/status" | jq '.wda'
```

The `wda` key can be changed via the HTTP-API v2 only. The device doesn't accept the setting via MQTT. For more
details please see https://github.com/goecharger/go-eCharger-API-v2/issues/35.

## References

* https://github.com/goecharger/go-eCharger-API-v2/blob/main/mqtt-en.md
* https://github.com/goecharger/go-eCharger-API-v2/blob/main/apikeys-en.md
* https://github.com/goecharger/go-eCharger-API-v1/blob/master/go-eCharger%20API%20v1%20DE.md
* https://github.com/boralyl/github-custom-component-tutorial

[^1]: Not exposed via MQTT in firmware 053.1
[^2]: Exposed via MQTT since firmware 056.2
[^3]: Not available in v1 Devices
[^4]: Not available in v2 Devices
[^5]: V1 `eto` and `dwo` values (0.1 kWh), `dws` values (10 Ws), and the scaled current/power fields in `nrg` are converted to the entity's displayed unit. Power-factor values in `nrg` are already percentages.
