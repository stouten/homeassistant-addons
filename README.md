# Biernet for Home Assistant

Custom integration that fetches filtered beer offers from [biernet.nl](https://www.biernet.nl/bier/aanbiedingen) and exposes them as a sensor, sorted by liter price. One integration entry per search profile ("zoekopdracht"), each with its own filters and sensor.

Full documentation: [custom_components/biernet/README.md](custom_components/biernet/README.md)

## Installation

1. Marketplace → custom repositories → add `https://github.com/stouten/homeassistant-addons`, category **Integration**
2. Install **Biernet**
3. Restart Home Assistant
4. **Instellingen → Apparaten & Diensten → Integratie toevoegen → Biernet**

## Also in this repository

| Type | Item |
|---|---|
| Add-on | [calibre-web-automated](calibre-web-automated/) — Calibre-Web-Automated as Home Assistant add-on (via the add-on store) |

## Note on multiple integrations

The Marketplace supports one integration per repository ("The Marketplace takes the first
folder in `custom_components/`"). If more custom integrations are added later, each one
needs its own repository to be listed separately in the Marketplace.

## Support

Report issues via [GitHub Issues](https://github.com/stouten/homeassistant-addons/issues).
