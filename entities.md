# CAN Bus Entity Analyse — TTF07C Sniffer

Abgleich der gesnifften CAN-Pakete (`sensor.heizung_can_bus_sniffer`) mit den definierten Properties in `property.h`.

**Letzte Analyse:** 06.05.2026 (Sniffer-Daten 26.04.–06.05.2026, 126.343 Einträge, 2.810 unique Pakete)
**System-Status während Analyse:** Sommerbetrieb aktiv, PROGRAMMSCHALTER: Programm/Eco

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

| Property ID | Name | Typ | Beispielwert | Quelle | Konfiguration |
|------------|------|-----|-------------|--------|---------------|
| 0x0003 | SPEICHERSOLLTEMP | et_dec_val | 45.0–46.0°C | Kessel | `wp_number` → WPM2 |
| 0x0004 | RUECKLAUFSOLLTEMP | et_dec_val | 5.0–38.0°C | HK1 | `wp_temperature` |
| 0x000C | AUSSENTEMP | et_dec_val | 0.2–29.8°C | Kessel | `wp_temperature` |
| 0x000E | SPEICHERISTTEMP | et_dec_val | 32.3–51.4°C | Kessel | `wp_temperature` |
| 0x0011 | RAUMISTTEMP | et_dec_val | 20.8–24.0°C | HK1 | `wp_temperature` |
| 0x0012 | VERSTELLTE_RAUMSOLLTEMP | et_dec_val | 5.0 / 22.6°C | HK1 | `wp_temperature` |
| 0x0016 | RUECKLAUFISTTEMP | et_dec_val | 16.1–32.0°C | Kessel | `wp_temperature` |
| 0x0075 | RAUMFEUCHTE | et_dec_val | 20.2–49.9% | HK1 | `wp_generic` |
| 0x010E | STEIGUNG_HK1 | et_cent_val | 0.35–1.50 | HK1 | `number` (Heizkurve) |
| 0x010F | RAUMEINFLUSS | et_little_endian | 4 | HK1 | defined, no sensor |
| 0x0112 | PROGRAMMSCHALTER | et_betriebsart | Programm(2)/Eco(5) | Kessel | `select` |
| 0x01D6 | VORLAUFISTTEMP | et_dec_val | 10.9–60.5°C | Kessel | `sensor` (custom) |
| 0x0A00 | ANLAGENFROST | et_dec_val | 4.0°C (konstant) | Kessel | broadcast passiv |
| 0x0A20 | BETRIEBS_STATUS | et_default | Bitfield (17 Werte) | Kessel | binary_sensors |
| 0x4F1E | SOMMERBETRIEB | — | (bool) | Kessel | `wp_binary` |

## Aktive Number-Entities (✅ — WPM2 Targets)

| Property ID | Name | Typ | Beispielwert | Quelle | Bereich |
|------------|------|-----|-------------|--------|---------|
| 0x0013 | WW_KOMF_TEMP | et_dec_val | 45.0–46.0°C | WPM2 | 30–65°C, Step 0.5 |
| 0x0022 | WW_HYSTERESE | et_dec_val | 2.0–3.0 K | WPM2 | 1–10 K, Step 0.5 |
| 0x0A06 | WW_ECO_TEMP | et_dec_val | 45.0–46.0°C | WPM2 | 30–65°C, Step 0.5 |

## Definiert, aber kein Sensor konfiguriert (⚙️)

| Property ID | Name | Typ | Beispielwert | Quelle | Kommentar |
|------------|------|-----|-------------|--------|-----------|
| 0x01D4 | QUELLE_IST | et_dec_val | — | Kessel | Nicht gesehen (Sommerbetrieb) |
| 0x01D5 | PUFFERSOLLTEMP | et_dec_val | — | Kessel | Nicht gesehen (Sommerbetrieb) |
| 0x01D7 | HKSOLLTEMP | et_dec_val | — | Kessel | Nicht gesehen (Sommerbetrieb) |
| 0x01E8 | MAXVORLAUFTEMP | et_dec_val | — | Kessel | Nicht gesehen (Sommerbetrieb) |
| 0x0078 | PUFFERISTTEMP | et_dec_val | — | Kessel | In property.h, kein Sensor |
| 0x0265 | HEISSGAS_TEMP | et_dec_val | — | Kessel | In property.h, kein Sensor |
| 0x01A2 | HDSENSORMAX | et_dec_val | — | Kessel | In property.h, kein Sensor |
| 0x0268 | DRUCK_HOCHDRUCK | et_cent_val | — | Kessel | In property.h, kein Sensor |
| 0x02CA | HKISTTEMP | et_dec_val | — | Kessel | In property.h, kein Sensor |

**Hinweis:** PUFFERSOLLTEMP, HKSOLLTEMP, MAXVORLAUFTEMP wurden in der Erstanalyse als "Broadcast alle ~10s" beobachtet, sind aber während Sommerbetrieb NICHT auf dem Bus sichtbar.

## Nicht in property.h — Interessant (❌)

| Property ID | Name (ElsterTable) | Typ | Beispielwert | Quelle → Ziel | Beschreibung |
|------------|-------------------|-----|-------------|---------------|-------------|
| 0x0002 | KESSELSOLLTEMP | et_dec_val | 5.0–38.0°C | HK1→Kessel | Kessel-Solltemperatur (bestätigt) |
| 0x0053 | HZK_PUMPE | default | 0 / 1 | Kessel | Heizkreispumpe Status (bestätigt) |
| 0x005E | TEILVORRANG_WW | default | 0 / 1 | Kessel | Teilvorrang Warmwasser (bestätigt) |
| 0x0058 | MISCHER_ZU | et_little_endian | 1 / 2 | HK1→FEK | Mischer-Position (bestätigt) |
| 0x006E | HEIZKREIS_STATUS_PROGSTELL | default | 1, 2, 3 | HK1→Kessel | Heizkreis Programmstellung (NEU: 3 Werte!) |
| 0x0009 | AUSSEN_VERZOEGERT | et_dec_val | ? | Kessel | Verzögerte Außentemperatur (Werte nicht plausibel im short format) |
| 0x0029 | MAX_TEMP_HZK | et_little_endian | 10 (0x0A00) | HK1→FEK | Max. Temperatur Heizkreis |
| 0x0010 | RAUMSOLLTEMP_TAG | et_dec_val | 8.1°C | Kessel | Raum-Solltemperatur Tag (Frostschutz?) |
| 0x0028 | MAX_RUECKLAUFTEMP | et_dec_val | 38.0°C | FEK→HK1 | Max. Rücklauftemperatur (bestätigt) |
| 0x0052 | BRENNER | et_little_endian | 0 / 1 | FEK | Wärmeanforderung FEK (bestätigt) |
| 0x0264 | TAUPUNKT_TEMP | et_dec_val | — | Kessel | Nicht gesehen (Sommerbetrieb) |
| 0x0261 | TAGESHEIZGRENZE | et_dec_val | — | FEK→HK1 | **Nicht gesehen** — nur bei FEK-Polling sichtbar |
| 0x01AC | BIVALENZTEMPERATUR_HZG | et_dec_val | — | Kessel→HK1 | Nicht gesehen (Sommerbetrieb) |
| 0x01AD | BIVALENZTEMPERATUR_WW | et_dec_val | — | Kessel→HK1 | Nicht gesehen (Sommerbetrieb) |
| 0x01AE | EINSATZGRENZE_HZG | ? | — | Kessel→HK1 | Nicht gesehen (Sommerbetrieb) |
| 0x01B0 | QUELLENTEMP_MIN | et_dec_val | — | Kessel→HK1 | Nicht gesehen (Sommerbetrieb) |
| 0x01C0 | FESTWERTBETRIEB | ? | — | Kessel→HK1 | Nicht gesehen (Sommerbetrieb) |

## FEK → HK1 (erweiterte Properties)

| Property ID | Name (ElsterTable) | Typ | Beschreibung | Sniffer-Status |
|------------|-------------------|-----|-------------|----------------|
| 0x0010 | RAUMSOLLTEMP_TAG | et_dec_val | Raum-Solltemperatur Tag | Kessel broadcast: 8.1°C |
| 0x0012 | VERSTELLTE_RAUMSOLLTEMP | et_dec_val | Verstellte Raumsolltemperatur | ✅ Aktiv (HK1, 5.0/22.6°C) |
| 0x0028 | MAX_RUECKLAUFTEMP | et_dec_val | Max. Rücklauftemperatur | FEK write: 38.0°C |
| 0x0057 | KESSELSCHUTZ | default | Kesselschutz | FEK write: 0 (konstant) |
| 0x0261 | TAGESHEIZGRENZE | et_dec_val | Grenze Sommerabschaltung | **Nicht sichtbar** (nur bei FEK-Polling) |

## Bus-intern / System (wenig nützlich)

| Property ID | Name (ElsterTable) | Typ | Beschreibung |
|------------|-------------------|-----|-------------|
| 0x000A | DATUM | et_datum | Datumssynchronisation |
| 0x000B | GERAETE_ID | et_dev_id | Gerätekennung (blacklisted) |
| 0x000F | VORLAUFISTTEMP (FEK) | et_dec_val | FEK-Variante, antwortet mit N/A |
| 0x002A | KP | default | Reglerparameter (HK1→FEK) |
| 0x0052 | BRENNER | et_little_endian | Wärmeanforderung FEK |
| 0x0056 | DCF | et_little_endian | Alterniert mit 0x52 |
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
- **0x0002 (KESSELSOLLTEMP)** könnte als passiver Sensor eingebaut werden (5.0–38.0°C bestätigt)
- Die FEK (0x601) sendet regelmäßig RAUMISTTEMP und RAUMFEUCHTE an HK1
- Kessel broadcastet alle ~10s: VORLAUFISTTEMP, PUFFERSOLLTEMP, MAXVORLAUFTEMP, RUECKLAUFISTTEMP
  - **Achtung:** PUFFERSOLLTEMP/HKSOLLTEMP/MAXVORLAUFTEMP nur im Heizbetrieb sichtbar!
- **Workaround:** ESP könnte VERSTELLTE_RAUMSOLLTEMP oder RUECKLAUFSOLLTEMP direkt schreiben, um den Effekt einer FEK-Modusumschaltung zu simulieren
- **TAGESHEIZGRENZE (0x0261):** Wert wurde am 05.05.2026 geändert, ist aber NICHT passiv auf dem Bus sichtbar. Nur während FEK↔HK1 Polling (alle ~7min) als einmaliger Write übertragen. Um den neuen Wert zu lesen, muss eine gezielte Abfrage an HK1 oder FEK gesendet werden.
- **Sommerbetrieb-Effekt:** Viele Heizungs-Properties (PUFFERSOLLTEMP, HKSOLLTEMP, MAXVORLAUFTEMP, BIVALENZTEMPERATUR_*, QUELLENTEMP_MIN) werden im Sommerbetrieb NICHT auf den Bus gesendet.
- **CAN Sniffer deaktiviert** am 06.05.2026 — Daten als `sniffer_history.json` gespeichert (126.343 Einträge, 10 Tage)
