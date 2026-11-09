# Biernet integration for Home Assistant

Custom integration that fetches filtered beer offers from [biernet.nl](https://www.biernet.nl/bier/aanbiedingen) and exposes them as a sensor, sorted by liter price. One integration entry per search profile ("zoekopdracht"), each with its own filters and sensor.

## Installation

### HACS (custom repository)

1. HACS → ⋮ (rechtsboven) → **Custom repositories**
2. Voeg `https://github.com/stouten/homeassistant-addons` toe, category **Integration**
3. Zoek en installeer **Biernet**
4. Herstart Home Assistant

### Handmatig

Kopieer `custom_components/biernet/` naar `<config>/custom_components/biernet/` en herstart Home Assistant.

## Setup

1. **Instellingen → Apparaten & Diensten → Integratie toevoegen → Biernet**
2. Vul de zoekopdracht in:
   - **Naam** – vrij te kiezen, bepaelt de sensornaam
   - **Winkels** – meerdere te selecteren (Albert Heijn, Jumbo, Gall & Gall, ...)
   - **Biersoorten** – alcoholvrij, pils, radler, IPA, ...
   - **Verpakkingen** – alle blikjes / flessen / kratten / fusten
   - **Alcoholpercentage** – bijv. `0 tot 1% (alcoholvrij)`
   - **Sortering** – bijv. literprijs oplopend
   - **Top N** – aantal aanbiedingen in de sensor (standaard 10)
   - **Verversinterval** – uren (standaard 24)
3. Voeg de integratie nogmaals toe voor elke extra zoekopdracht.

Bestaande zoekopdrachten pas je aan via **Configureren** op de integratie-entry.

## Sensor

- **State**: laagste literprijs (€/l) van de zoekopdracht
- **Attributen**:
  - `items` – lijst met `naam`, `verpakking`, `winkel`, `prijs`, `literprijs`, `geldig`, `url`
  - `count`, `total_aanbiedingen`
  - `filters` – leesbare samenvatting van de filters
  - `site_url` – link naar de bijbehorende biernet.nl-pagina

## Voorbeeldkaart

```yaml
type: markdown
title: Alcoholvrij — beste literprijs
content: >
  {%- set items = state_attr('sensor.biernet_alcoholvrij', 'items') or [] %}
  | # | Bier | Verpakking | Winkel | Prijs | per liter |
  |---|---|---|---|---|---|
  {%- for i in items %}
  | {{ loop.index }} | {{ i.naam }} | {{ i.verpakking }} | {{ i.winkel }} | €{{ i.prijs }} | **€{{ i.literprijs }}** |
  {%- endfor %}
```

## Technische werking

De aanbiedingen op biernet.nl worden via een AJAX-endpoint geladen
(`POST /site/php/data/aanbiedingen.php` met een per-sessie token uit de pagina).
Deze integratie doet exact wat de site zelf doet en parseert het HTML-fragment.
Er is geen officiële API; als biernet.nl de site herstructureert kan de integratie breken.

## Notes

- No official API exists; this integration uses biernet.nl's internal AJAX endpoint.
- Keep the update interval at 24 hours (default); the Dutch offers change weekly.
