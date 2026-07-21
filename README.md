# One2Track — Home Assistant Integratie

[![Version](https://img.shields.io/badge/version-1.0.21-blue)](https://github.com/onsmam/ha-one2track)

Custom Home Assistant integratie voor [One2Track](https://www.one2trackgps.com) GPS-horloges (kinder- en senioren-trackers).

> **Credits:** Het harde werk voor deze integratie is gedaan door [@jurrienk](https://github.com/jurrienk). Deze fork voegt extra functies toe.

> **Taal / Language:** [English](#english) | [Nederlands](#nederlands)

---

## Nederlands

### Functies

- **Device tracker** met GPS-coördinaten, zone-detectie en adres
- **12 sensoren** — batterij, SIM-tegoed, signaalsterkte, aantal satellieten, snelheid, hoogte, koers, GPS-nauwkeurigheid, stappen, status, tijdstempels
- **Telefoonboek & whitelist-sensoren** — tonen het aantal contacten/nummers met volledige lijst als attribuut (alleen aangemaakt als het horloge deze functies ondersteunt)
- **Binaire sensor** — valdetectie
- **Knoppen** — locatie vernieuwen (activeer GPS-modus), horloge bellen
- **Schakelaar** — stappenteller aan/uit
- **Selecties** — GPS-interval, profielmodus
- **19 diensten** — bericht sturen, update forceren, horloge bellen, intercom, SOS-nummer instellen, contacten beheren, whitelist beheren, wekkers instellen, stille tijden instellen, taal/tijdzone instellen, wachtwoord wijzigen, fabrieksinstellingen, uitschakelen op afstand, en een diagnostische dienst
- **Multi-model ondersteuning** — detecteert automatisch de functies van elk horloge (Connect MOVE, Connect UP, Connect Go en andere modellen)
- **Apparaat-targeting** — alle diensten ondersteunen `entity_id`, `device_id` en `area_id`
- **Persistente instellingen** — telefoonboek, whitelist, wekkers en stille tijden blijven bewaard na herstart van HA
- **Niet beschikbaar bij offline** — locatie-sensoren en de device tracker gaan op "niet beschikbaar" als het horloge offline is

### Installatie

#### HACS (aanbevolen)

1. Open HACS in je Home Assistant
2. Ga naar **Integraties** en klik op het drie-puntjes-menu rechtsboven
3. Kies **Aangepaste repositories**
4. Voeg `https://github.com/onsmam/ha-one2track` toe met categorie **Integratie**
5. Zoek naar "One2Track" en installeer het
6. Herstart Home Assistant
7. Ga naar **Instellingen > Apparaten & Diensten > Integratie toevoegen** en zoek op **One2Track**
8. Voer je One2Track portal gebruikersnaam en wachtwoord in

#### Handmatig

1. Kopieer de map `custom_components/one2track` naar je Home Assistant `config/custom_components/` map
2. Herstart Home Assistant
3. Voeg de integratie toe via **Instellingen > Apparaten & Diensten**

### Ondersteunde apparaten

De integratie detecteert automatisch je horloges en hun functies. Getest met:

- **Connect UP** (model_id 77) — GPS-interval code 0077, stappenteller code 0082
- **Connect MOVE** (model_id 27) — GPS-interval code 0078, stappenteller code 0079, plus whitelist, intercom en wachtwoord wijzigen
- **Connect Go** — ondersteuning aanwezig; run `one2track.get_raw_device_data` om het model-ID te achterhalen

Andere One2Track horlogemodellen zouden ook moeten werken — de integratie detecteert beschikbare commando's dynamisch.

### Hoe het werkt

Er is geen officiële One2Track API. Deze integratie communiceert met `www.one2trackgps.com` (een Ruby on Rails webapplicatie) via:

1. Inloggen via het inlogformulier met sessiecookies en CSRF-tokens
2. Apparaatstatus ophalen door inline JavaScript-variabelen van apparaatpagina's te scrapen
3. Basisdata vernieuwen via het JSON-apparatenlijst-endpoint
4. Commando's sturen via formulier-POSTs die de PATCH-verzoeken van de webportal nabootsen

### Diagnostiek

Roep de dienst `one2track.get_raw_device_data` aan om ruwe data van alle bronnen op te halen (JSON API, HTML-scraping, coördinator-status, ontdekte functies). Dit is onmisbaar voor het debuggen van dataproblemen.

### Credits

Het originele werk is gedaan door [@jurrienk](https://github.com/jurrienk) — hij heeft de One2Track-portal ontcijferd, de scraping-laag gebouwd en alle diensten geïmplementeerd. Deze fork voegt extra functionaliteit toe bovenop zijn werk.

---

## English

### Features

- **Device tracker** with GPS coordinates, zone detection, and address
- **12 sensors** — battery, SIM balance, signal strength, satellite count, speed, altitude, heading, GPS accuracy, steps, status, timestamps
- **Phonebook & whitelist sensors** — show contact/number count with full list as attributes (only created if the device supports these features)
- **Binary sensor** — fall detection
- **Buttons** — refresh location (activate GPS mode), find device (ring the watch)
- **Switch** — step counter toggle
- **Selects** — GPS tracking interval, profile/sound mode
- **19 services** — send message, force update, find device, intercom, set SOS number, set/add/remove phonebook contacts, set/add/remove whitelist numbers, set alarms, set quiet times, set language/timezone, change password, factory reset, remote shutdown, and a raw diagnostics service
- **Multi-model support** — automatically discovers each watch's capabilities (Connect MOVE, Connect UP, Connect Go, and others)
- **Device targeting** — all services support `entity_id`, `device_id`, and `area_id` targeting
- **Persistent settings** — phonebook, whitelist, alarms, and quiet times survive HA restarts
- **Unavailable when offline** — location sensors and the device tracker become unavailable when the watch goes offline

### Installation

#### HACS (recommended)

1. Open HACS in your Home Assistant instance
2. Go to **Integrations** and click the three-dot menu in the top right
3. Select **Custom repositories**
4. Add `https://github.com/onsmam/ha-one2track` with category **Integration**
5. Search for "One2Track" and install it
6. Restart Home Assistant
7. Go to **Settings > Devices & Services > Add Integration** and search for **One2Track**
8. Enter your One2Track portal username and password

#### Manual

1. Copy the `custom_components/one2track` folder to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant
3. Add the integration via **Settings > Devices & Services**

### Supported Devices

The integration auto-discovers your watches and their capabilities. Tested with:

- **Connect UP** (model_id 77) — GPS interval code 0077, step counter code 0082
- **Connect MOVE** (model_id 27) — GPS interval code 0078, step counter code 0079, plus whitelist, intercom, and password change
- **Connect Go** — supported; run `one2track.get_raw_device_data` to find the model ID

Other One2Track watch models should work — the integration discovers available commands dynamically rather than hardcoding per model.

### How It Works

There is no official One2Track API. This integration communicates with `www.one2trackgps.com` (a Ruby on Rails web application) by:

1. Authenticating via the login form with session cookies and CSRF tokens
2. Polling device state by scraping inline JavaScript variables from device pages
3. Refreshing base data from the JSON device list endpoint
4. Sending commands via form POSTs that mimic the web portal's PATCH requests

### Diagnostics

Call the `one2track.get_raw_device_data` service to get raw data from all sources (JSON API, HTML scraping, coordinator state, discovered capabilities). This is invaluable for debugging data issues.

### Credits

The original integration was built by [@jurrienk](https://github.com/jurrienk) — all the hard work of reverse-engineering the One2Track portal, building the scraping layer, and creating the full service set is his.

### Changelog

#### v1.0.21

- **Feature:** Schakelaar "Volledig pollen" toegevoegd — **Uit**: alleen JSON status-check elke 60 seconden (weet of horloge online is, geen GPS-data); **Aan**: volledige poll (JSON + HTML-scraping) eens per 60 minuten, direct een volle refresh bij inschakelen; instelling blijft bewaard na herstart

#### v1.0.20

- **Fix:** Removed HA deprecation warnings — `TrackerEntity` now imported from `homeassistant.components.device_tracker`, `source_type` returns `SourceType.GPS` enum, deprecated `battery_level` and `location_name` properties removed
- **Fix:** Alarm-malformed log message downgraded from WARNING to DEBUG (portal always returns JS template strings for alarm fields — this is expected behaviour)

#### v1.0.19

- **Feature:** Connect Go toegevoegd aan modelnamenregister (model_id 28)
- **Feature:** Firmwareversie van het horloge zichtbaar in HA-apparaatdetails (`sw_version`)

#### v1.0.18

- **Feature:** Location sensors (altitude, GPS accuracy, satellite count, signal strength, speed, heading) and device tracker now return `unavailable` when the watch is offline
- **Feature:** Added Dutch translation (`nl.json`)
- **Feature:** Added `brands/` folder for HA brands proxy API logo assets
- **Docs:** Bilingual README (NL + EN), credits added, full changelog restored

#### v1.0.17 (2026-03-21)

- **Fix:** Zone detection now returns the zone slug (e.g. `home`) instead of the display name (`Home`), fixing person tile not turning green when in the home zone

#### v1.0.15 (2026-03-16)

- **Fix:** Transient server errors (e.g. HTTP 503) during setup now raise `ConfigEntryNotReady` so Home Assistant automatically retries instead of marking the integration as permanently failed

#### v1.0.13 (2026-03-16)

- **Docs:** Added git workflow rules to CLAUDE.md

#### v1.0.8 (2026-03-16)

- **Fix:** Phonebook and whitelist attributes now always exposed on device tracker (empty list when no data, instead of missing)
- **Improvement:** Device entries now include manufacturer ("One2Track") and model name from the portal

#### v1.0.7 (2026-03-16)

- **Fix:** Added missing `remote_shutdown` translation to `en.json`
- **Housekeeping:** Added `__pycache__` and `.private/` to `.gitignore`

#### v1.0.6 (2026-03-16)

- **Docs:** Added test safety section — snapshot and restore device state

#### v1.0.5 (2026-03-16)

- **Improvement:** Select entities (GPS interval, profile mode) now appear in the Configuration section on the device page
- **Fix:** Reverted step counter switch change that broke functionality — restored assumed state behavior

#### v1.0.4 (2026-03-15)

- **Feature:** Added remote shutdown button entity (disabled by default — must be manually enabled per device to prevent accidental use)

#### v1.0.3 (2026-03-15)

- **Fix:** `last_location_update` sensor now guards against corrupt device RTC timestamps (e.g. 10 years in the future). Falls back to server-stamped `created_at` with a warning log when the device-reported value is more than 24 hours in the future

#### v1.0.2 (2026-03-15)

- **Docs:** Aligned version numbers across all documentation

#### v1.0.1 (2026-03-15)

- **Docs:** Removed personal name references from documentation

#### v1.0.0 (2026-03-15)

- **Fix:** Alarm values synced from portal are now validated — malformed values (e.g. JavaScript template fragments) are discarded and local state is preserved
- **Fix:** `add_phonebook_contact` no longer raises a false error when the portal returns HTTP 500 on a successful write — local state is updated optimistically
- **Fix:** All service validation errors now use `ServiceValidationError` for proper HA UI error display instead of raw 500 messages
- **Fix:** `intercom` and `change_password` capability errors now show the device name and a clear message about Connect MOVE requirement
- **Fix:** `alarms` and `quiet_times` attributes are always present on the device tracker (empty list `[]` when cleared, instead of disappearing)
- **Improvement:** Heading sensor satellite_count comparison is now type-safe
- **Improvement:** Whitelist full error message now suggests using `set_whitelist` as an alternative

#### v0.9.9

- Individual phonebook/whitelist management (add/remove contacts and numbers)
- Portal readback before modify operations
- Persistent settings storage across HA restarts
- 19 services with full entity/device/area targeting
