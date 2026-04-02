# CAN Bus Entity Analyse — TTF07C Sniffer

Abgleich der gesnifften CAN-Pakete (`sensor.heizung_can_bus_sniffer`) mit den definierten Properties in `property.h`.

## Legende

- ✅ **Aktiv** — Sensor/Callback vorhanden, Wert wird in HA angezeigt
- ⚙️ **Definiert** — In `property.h` vorhanden, aber kein Sensor/Callback konfiguriert
- ❌ **Unbekannt** — Nicht in `property.h`, nur in ElsterTable oder komplett unbekannt

## CAN Bus Teilnehmer

| CAN ID | Name | Beschreibung |
|--------|------|-------------|
| 0x180 | Kessel | Wärmepumpe (Hauptgerät) |
| 0x301 | HK1 | Heizkreis 1 (Mischermodul) |
| 0x480 | WPM2 | Wärmepumpenmanager (integriert) |
| 0x601 | FEK | Fernbedienung (Raumgerät) |
| 0x680 | ESPClient | ESP32 (unser Gerät) |

## Aktive Sensoren (✅)

| Property ID | Name | Typ | Beispielwert | Quelle |
|------------|------|-----|-------------|--------|
| 0x0003 | SPEICHERSOLLTEMP | et_dec_val | 50.0°C | Kessel |
| 0x0004 | RUECKLAUFSOLLTEMP | et_dec_val | 28.7°C | HK1 |
| 0x000C | AUSSENTEMP | et_dec_val | 10.1°C | Kessel |
| 0x000E | SPEICHERISTTEMP | et_dec_val | 50.9°C | Kessel |
| 0x0011 | RAUMISTTEMP | et_dec_val | 22.3°C | HK1→FEK |
| 0x0012 | VERSTELLTE_RAUMSOLLTEMP | et_dec_val | 22.7°C | HK1 |
| 0x0016 | RUECKLAUFISTTEMP | et_dec_val | 28.1–29.2°C | Kessel |
| 0x0075 | RAUMFEUCHTE | et_dec_val | 33.4–33.8% | HK1→FEK |
| 0x010F | RAUMEINFLUSS | et_little_endian | 4 | HK1 |
| 0x0112 | PROGRAMMSCHALTER | et_betriebsart | (mapped) | Kessel |
| 0x01D6 | VORLAUFISTTEMP | et_dec_val | 28.1–28.7°C | Kessel |
| 0x0A20 | BETRIEBS_STATUS | et_default | Bitfield | Kessel |
| 0x4F1E | SOMMERBETRIEB | — | (bool) | Kessel |

## Definiert, aber kein Sensor konfiguriert (⚙️)

| Property ID | Name | Typ | Beispielwert | Quelle | Kommentar |
|------------|------|-----|-------------|--------|-----------|
| 0x01D5 | PUFFERSOLLTEMP | et_dec_val | 28.7°C | Kessel→HK1 | Broadcast alle ~10s |
| 0x01E8 | MAXVORLAUFTEMP | et_dec_val | 45.0°C | Kessel→HK1 | Broadcast alle ~10s |

## Nicht in property.h — Interessant (❌)

| Property ID | Name (ElsterTable) | Typ | Beispielwert | Quelle → Ziel | Beschreibung |
|------------|-------------------|-----|-------------|---------------|-------------|
| 0x0002 | KESSELSOLLTEMP | et_dec_val | 28.7°C | HK1→Kessel | Kessel-Solltemperatur |
| 0x0029 | MAX_TEMP_HZK | et_dec_val | ? | HK1→FEK | Max. Temperatur Heizkreis |
| 0x0053 | HZK_PUMPE | default | 0 | Kessel | Heizkreispumpe Status |
| 0x0058 | MISCHER_ZU | et_little_endian | 2 | HK1→FEK | Mischer zu |
| 0x006E | HEIZKREIS_STATUS_PROGSTELL | default | 1 | HK1→Kessel | Heizkreis Programmstellung |

## Bus-intern / System (wenig nützlich)

| Property ID | Name (ElsterTable) | Typ | Beschreibung |
|------------|-------------------|-----|-------------|
| 0x000A | DATUM | et_datum | Datumssynchronisation |
| 0x000B | GERAETE_ID | et_dev_id | Gerätekennung (blacklisted) |
| 0x000F | VORLAUFISTTEMP (FEK) | et_dec_val | FEK-Variante, antwortet mit N/A |
| 0x002A | KP | default | Reglerparameter |
| 0x0052 | BRENNER | et_little_endian | Brenner-Status |
| 0x0056 | DCF | et_little_endian | DCF77-Zeitsignal |
| 0x005A | SPEICHER_STATUS | et_little_endian | Speicher-Status |
| 0x005E | TEILVORRANG_WW | default | Teilvorrang Warmwasser |
| 0x00FD | BUSKONFIGURATION | default | Bus-Konfiguration (blacklisted) |
| 0x00FE | INITIALISIERUNG | et_little_endian | Bus-Initialisierung (blacklisted) |

## Eigene Nachrichten (ESP→Bus)

| Paket | Beschreibung |
|-------|-------------|
| `680#D600FD08000000` | ESP sendet Konfigurationsnachricht |

## FEK-Modus Analyse (Tag / Nacht / Bereitschaft / Automatik)

Die FEK (0x601) kommuniziert **nur** wenn HK1 sie pollt — ca. alle **7 Minuten**.
Es gibt **kein** CAN-Property für den FEK-Betriebsmodus. Der Modus ist nur am physischen Gerät umschaltbar.

### HK1↔FEK Protokoll (pro Polling-Zyklus, 2 Runden)

**FEK → HK1 (Antworten):**
| Property | Elster-Name | Typ | Beschreibung |
|----------|-------------|-----|-------------|
| 0x00FE | INITIALISIERUNG | Response | Handshake (immer 0x0100) |
| 0x0052 | BRENNER | Response | Raum hat Wärmeanforderung (1=ja, 0=nein) |
| 0x0056 | DCF | Response | Alternierend mit 0x52 (nicht DCF77!) |
| 0x005A | SPEICHER_STATUS | Response | Immer 0x0200 |
| 0x0011 | RAUMISTTEMP | Response | Raumtemperatur (et_dec_val) |
| 0x000F | VORLAUFISTTEMP | Response | Immer 0xFE70 (N/A — FEK hat keinen VL-Sensor) |
| 0x0004 | RUECKLAUFSOLLTEMP | Response | Immer 0xFE70 (N/A) |

**HK1 → FEK (Schreiben):**
| Property | Elster-Name | Typ | Beschreibung |
|----------|-------------|-----|-------------|
| 0x0029 | MAX_TEMP_HZK | Write | Immer 0x0A00 (konstant) |
| 0x0075 | RAUMFEUCHTE | Write | Aktuelle Raumfeuchte |
| 0x0011 | RAUMISTTEMP | Write | Aktuelle Raumtemperatur |
| 0x0004 | RUECKLAUFSOLLTEMP | Write | Berechnete Rücklauf-Solltemperatur |

### Vergleich FEK-Modi

| Modus | RUECKLAUFSOLLTEMP (0x04) | FEK 0x52 | Bemerkung |
|-------|----------------------|----------|-----------|
| **Tag** | ~28.6–29.0°C | 0x0100 / 0x0000 (alternierend) | Normaler Heizbetrieb |
| **Nacht** | ~28.1°C (reduziert) | 0x0100 | Abgesenkter Betrieb |
| **Bereitschaft** | 5.0°C (Frostschutz) | 0x0000 | Nur Frostschutz aktiv |
| **Automatik** | ~28.6°C (zeitgesteuert) | 0x0100 | Folgt Zeitprogramm |

**Fazit:** Der FEK-Modus wird **nicht** als Property auf den CAN-Bus übertragen. Er beeinflusst nur indirekt den RUECKLAUFSOLLTEMP, den HK1 berechnet. Eine Umschaltung per CAN ist nicht möglich — nur per physischer Taste an der FEK.

## Notizen

- **0x01D6** ist die korrekte Property-ID für VORLAUFISTTEMP bei der TTF07C (nicht 0x06A1)
- **0x0002 (KESSELSOLLTEMP)** könnte als passiver Sensor eingebaut werden
- Die FEK (0x601) sendet regelmäßig RAUMISTTEMP und RAUMFEUCHTE an HK1
- Kessel broadcastet alle ~10s: VORLAUFISTTEMP, PUFFERSOLLTEMP, MAXVORLAUFTEMP, RUECKLAUFISTTEMP
- **Workaround:** ESP könnte VERSTELLTE_RAUMSOLLTEMP oder RUECKLAUFSOLLTEMP direkt schreiben, um den Effekt einer FEK-Modusumschaltung zu simulieren
