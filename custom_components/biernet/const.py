"""Constants for the Biernet integration."""

DOMAIN = "biernet"
BASE_URL = "https://www.biernet.nl"
PAGE_URL = f"{BASE_URL}/bier/aanbiedingen/"
LIST_URL = f"{BASE_URL}/site/php/data/aanbiedingen.php"

CONF_NAME = "name"
CONF_WINKEL = "winkel"
CONF_SOORT = "soort"
CONF_VERPAKKING = "verpakking"
CONF_PERCENTAGE = "percentage"
CONF_SORTEER = "sorteer"
CONF_TOP_N = "top_n"
CONF_UPDATE_HOURS = "update_hours"

DEFAULT_TOP_N = 10
DEFAULT_UPDATE_HOURS = 24

WINKELS = {
    "albert-heijn": "Albert Heijn",
    "alcoholvrijbierhuis": "Alcoholvrijbierhuis",
    "aldi": "Aldi",
    "biermomentje": "Biermomentje",
    "bierxl": "BierXL",
    "boni": "Boni",
    "boons-markt": "Boon's Markt",
    "buurtbiernl": "Buurtbier.nl",
    "coop": "Coop",
    "dagwinkel": "Dagwinkel",
    "dare-to-drink-different": "Dare to Drink Different",
    "dekamarkt": "DekaMarkt",
    "die-grenze": "Die Grenze",
    "dirck-iii": "Dirck III",
    "dirk": "Dirk",
    "ekoplaza": "EkoPlaza",
    "flink": "FLINK",
    "gall-en-gall": "Gall & Gall",
    "hanos": "Hanos",
    "hoogvliet": "Hoogvliet",
    "horecagoedkoopnl": "Horecagoedkoop.nl",
    "joybuy": "Joybuy",
    "jumbo": "Jumbo",
    "kantinewinkel": "Kantinewinkel",
    "lidl": "Lidl",
    "makro": "Makro",
    "mcd": "MCD",
    "mitra": "Mitra",
    "nettorama": "Nettorama",
    "online-bierwinkel": "Online Bierwinkel",
    "plus": "Plus",
    "poiesz": "Poiesz",
    "sligro": "Sligro",
    "spar-buurt": "Spar Buurt",
    "vomar": "Vomar",
}

SOORTEN = {
    "alcoholarm": "Alcoholarm",
    "alcoholvrij": "Alcoholvrij",
    "ale": "Ale",
    "amber": "Amber",
    "biermix": "Biermix",
    "blond": "Blond",
    "bock": "Bock",
    "cider": "Cider",
    "dortmunder": "Dortmunder",
    "dubbel": "Dubbel",
    "dunkel-weizen": "Dunkel weizen",
    "fruitbier": "Fruitbier",
    "gerstewijn": "Gerstewijn",
    "herfstbok": "Herfstbok",
    "honingbier": "Honingbier",
    "india-pale-ale": "India Pale Ale",
    "kellerbier": "Kellerbier",
    "lager": "Lager",
    "lentebier": "Lentebier",
    "lentebok": "Lentebok",
    "light": "Light",
    "mexicaans-bier": "Mexicaans bier",
    "oud-bruin-bier": "Oud bruin bier",
    "pale-ale": "Pale Ale",
    "pils": "Pils",
    "porter": "Porter",
    "quadrupel": "Quadrupel",
    "radler": "Radler",
    "rose": "Rosé",
    "saison": "Saison",
    "sour": "Sour",
    "stout": "Stout",
    "tequila-bier": "Tequila bier",
    "tripel": "Tripel",
    "weizen": "Weizen",
    "whiskeybier": "Whiskeybier",
    "winterbier": "Winterbier",
    "wit": "Wit",
}

VERPAKKINGEN = {
    "blik-alle": "Alle blikjes",
    "fles-alle": "Alle flessen",
    "krat-alle": "Alle kratten",
    "fust-alle": "Alle fusten",
}

VERPAKKING_PARAMS = {
    "blik-alle": "blikjes",
    "fles-alle": "flessen",
    "krat-alle": "kratten",
    "fust-alle": "fusten",
}

PERCENTAGES = {
    "": "Alle alcoholpercentages",
    "0tm1": "0 tot 1% (alcoholvrij)",
    "0tm3": "0 tot 3%",
    "0tm5": "0 tot 5%",
    "1tm5": "1 tot 5%",
    "5tm10": "5 tot 10%",
}

SORTERINGEN = {
    "literprijs-oplopend": "Literprijs oplopend",
    "literprijs-aflopend": "Literprijs aflopend",
    "prijs-oplopend": "Prijs oplopend",
    "prijs-aflopend": "Prijs aflopend",
    "kortingspercentage-oplopend": "Kortingspercentage oplopend",
    "kortingspercentage-aflopend": "Kortingspercentage aflopend",
}

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)
