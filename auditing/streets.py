import os
import re

from typing import Optional, Tuple
from xml.etree.cElementTree import Element


def is_street_name(elem: Element) -> bool:
    """
    Checks an OSM XML tag element if it represents a street name.

    :param elem: The element
    :return: True if the tag refers to a street name.
    """

    assert 'k' in elem.attrib and 'v' in elem.attrib
    return elem.attrib['k'] == 'addr:street'


def audit_street_name(name: str) -> Tuple[bool, Optional[str]]:
    """
    Checks a street name for validity and applies fixes where possible.

    :param name: The street name to audit.
    :return: A tuple containing a boolean indicating if the name was corrected, as well as the (corrected) name or
             None if the name does not refer to an actual street.
    """
    assert isinstance(name, str) and not name.endswith(os.linesep)

    # Make sure there are no white spaces around
    name = name.strip()

    # Override checks first
    if name in known_valids:
        return True, name
    elif len(name) == 0:
        return False, None
    elif name in not_a_road:
        return False, None

    # Before applying the regex sledgehammer we try to handle
    # the easier fixes directly
    if name[0].islower():
        return False, name[0].upper() + name[1:]
    elif name.endswith('staße'):
        return False, name[:-5] + 'straße'
    elif name.endswith('promedade'):
        return False, name[:-9] + 'promenade'
    elif name in known_corrections:
        return False, known_corrections[name]

    # Check if any of the positive regexes match.
    ms = [regex.search(name) for regex in valid_street_names]
    if any(m is not None for m in ms):
        return True, name

    # Finally, if the name could not be corrected and didn't check out,
    # we're raising an error. Either the dictionaries/sets need to be
    # fixed or the regexes do not capture all required cases.
    raise ValueError('No correction found for the given street name.')


# The following set contains all rules gathered during initial screening
# of the dataset. If any of the rules evaluates positively, we assume
# the street name is correct.
# Each rule is commented with examples for street names they capture.
valid_street_names = {
        # Einheit
        # Hüsung
        # Siedlung
        # Zehnruthen
        # Seematen
        # Quermathe
        re.compile(r'^[A-Z][a-zäöüß]+(th?en?|heit|mat|ung|bad|hag)$', re.UNICODE),
        # Am Anger
        # Am Krögel
        # Im Hufenschlag
        re.compile(r'^[AI]m\s[A-Z][a-zäöüß]+$', re.UNICODE),
        # Am Feuchten Winkel
        # Am Köllnischen Park
        # Am alten Gaswerk
        # Im Schönower Park
        re.compile(r'^[AI]m\s[A-Za-z][a-zäöüß]+(en|er|hof|platz)\s[A-Z][a-zäöüß]+$', re.UNICODE),
        # An den Achterhöfen
        # An der alten Post
        # An der Kieler Brücke
        # Hinter dem Kurpark
        # Hinter der Katholischen Kirche
        re.compile(r'^(An|Auf|Hinter)\s(der|dem)(\s[A-Za-zäöüß]+)?\s[A-Z][a-zäöüß]+$', re.UNICODE),
        # An den Hubertshäusern
        # An den Eldenaer Höfen
        # Zum Ruhlsdorfer Feld
        # Zur Alten Flussbadeanstalt
        # Zur Buckstammhütung
        # In den Floragärten
        # In der Aue
        # Unter den Linden
        # Vor dem Schlesischen Tor
        # Bei den Wörden
        re.compile(r'^((An|Zu|In|Unter|Vor|Bei)\sde[rnm]|Zur|Zum)(\s[A-Za-zäöüß]+(er|en))?\s[A-Z][a-zäöüß]+$',
                   re.UNICODE),
        # Üderseestraße
        # Buchholzweg
        # Wilhelmsaue
        # Andréezeile
        # Waldwinkel
        # Vogelsang
        # Verlängerte Koloniestraße
        # Umgehungsstraße Seefeld
        # Albrechts Teerofen
        # Gendarmenmarkt
        # Landrèstraße
        re.compile(r'^([A-ZÄÖÜ][a-zäöüß]+(s|e[rs])?\s)?[A-ZÄÖÜ][a-zäöüßáéè]+(straße|weg|allee|platz|aue|gestell|ufer|'
                   r'hof|steg|ring|damm|zeile|park|gasse|hain|grund|stieg|steig|pfad|tal|horst|promenade|schlag|rain|'
                   r'kiez|korso|enden|marken|winkel|sang|trift|werk|feld|bahn|höhe|stern|passage|chaussee|siedlung|'
                   r'garten|blick|kamp|bogen|hafen|schanze|zug|grabern|kehre|beize|sprung|schneise|gang|hahn|ruf|anger|'
                   r'fang|tisch|wechsel|berg|graben|balz|ofen|heide|linde|eck|plan|busch|segen|dreesch|mühle|markt|'
                   r'insel|fichten|bau|wald|berge|hang|rode|wöhrde|dorf)$', re.UNICODE),
        # Straße 52b
        # Straße 577
        # Straße G
        re.compile(r'^Straße\s([0-9]+[a-z]?|[A-Z])$', re.UNICODE),
        # Altglienicker Grund
        # Zossener Straße
        # Angerburger Allee
        # Lange Brücke
        # Hallesches Ufer
        # Groß-Ziethener Straße
        # Marzahner Promenade
        # Prenzlauer Berg
        # Darßer Bogen
        # Märkische Heide
        # Klein-Ziethener Weg
        re.compile(r'^([A-ZÄÖÜ][a-zäöüß]+(e[rs]?\s|ß-)|Groß-|Klein-)?[A-ZÄÖÜ][a-zäöüß]+(e[rs]?|hof)\s(Straße|Weg|Allee|'
                   r'Platz|Ufer|Damm|Chaussee|Ring|Winkel|Pfad|Dreieck|Zeile|Grund|Markt|Steig|Promenade|Eck|Berg|'
                   r'Gasse|Trift|Ster|Anger|Welt|Wiesen|Enden|Brücke|Stücken|Park|Weiche|Bogen|Kiefer|Ähren|Birken|'
                   r'Gehren|Heide|Spitze)$', re.UNICODE),
        # Siegmunds Hof
        # Großer Stern
        # Eigene Scholle
        re.compile(r'^[A-ZÄÖÜ][a-zäöüß]+(s|er?)\s[A-ZÄÖÜ][a-zäöüß]+$', re.UNICODE),
        # AEG-Siedlung Heimat
        # VEG-Siedlung
        # Parksiedlung Spruch
        re.compile(r'^([A-Z]+-S|[A-Z][a-zäöüß]+s)iedlung(\s[A-ZÄÖÜ][a-zäöüß]+)?$', re.UNICODE),
        # Gewerbegebiet zum Wasserwerk
        # Industriegelände
        # Siedlung am Fließ
        re.compile(r'^(Gewerbegebiet|Industriegelände|Siedlung)(\s([a-zäöüß]+\s)[A-ZÄÖÜ][a-zäöüß]+?)?$', re.UNICODE),
        # Alma-Straße
        # Justus-von-Liebig-Straße
        # Kaiserin-Augusta-Allee
        # William-H.-Tunner-Straße
        # Billy-Wilder-Promenade
        # McDonald's-Straße
        # Van't-Hoff-Straße
        # McNair-Promenade
        # Dr.-Albert-Schweitzer-Straße
        # Orenstein-&-Koppel-Straße
        re.compile(r'^[A-ZÄÖÜ][a-zäöüßéDN\.]+(\'[st])?-((&-)?[A-Za-zäöüßé]+\.?-)*(Straße|Weg|Allee|Platz|Ufer|Damm|'
                   r'Chaussee|Ring|Winkel|Siedlung|Promenade|Park|Steig|Zeile|Pfad)$', re.UNICODE),
        # Allée St. Exupéry
        # Allee der Kosmonauten
        re.compile(r'^All[ée]e\s(am|der|nach|St\.)\s[A-Z][a-zäöüßé]+$', re.UNICODE),
        # Straße am Flugplatz
        # Straße der Freundschaft
        # Straße der Pariser Kommune
        # Straße des 17. Juni
        # Straße zum Weißen Schwan
        # Straße zum FEZ
        # Platz des 4. Juli
        # Platz der Vereinten Nationen
        # Weg ins Feld
        # Ring am Feld
        # Glück im Winkel
        re.compile(r'^((Straße|Glück|Platz)\s(der|des|im|am|vor|vor dem|zum)|Weg\sins|Ring\sam)\s([A-Z][a-zäöüßé]+\s|'
                   r'[1-9][0-9]*\.\s)?([A-Z][a-zäöüßé]+|[A-Z]+)$', re.UNICODE),
        # Rue Doret
        # Rue Henri Guillaumet
        # Rue Marin la Meslée
        # Rue du Capitaine Jean Maridor
        # Avenue Jean Mermoz
        # Via Tilia
        re.compile(r'^(Rue|Avenue|Via)(\s((du|le|la|et)\s)?[A-Z][a-zé]+)+$', re.UNICODE),
        # Alt-Friedrichsfelde
        # Alt Großziethen
        re.compile(r'^Alt[-\s][A-Z][a-zäöüß]+$', re.UNICODE),
        # Alte Gärtnerei
        # Altes Forsthaus
        # Alte Potsdamer Landstraße
        re.compile(r'^Alte[rs]?\s([A-Z][a-z]+\s)?[A-Z][a-zäöüß]+$', re.UNICODE),
    }


# Mapping of special names that are allowed. These do not fit in
# with the rules above and are simply accepted as-is.
known_valids = {'Neu Zittauer Straße',
                'Klein Schönebecker Straße',
                'Otto\'s Weg',
                'Hanne Nüte',
                'Stern-Center',
                'Esplanade',
                'Scholle',
                'Hempstücken',
                'Ausbau Mühle',
                'Grüne Trift am Walde',
                'Heide in den Bergen',
                'Renate-Privatstraße'
                }

# Set of names that are known not to be a road (in Berlin).
not_a_road = {'U-Bahnhof Alt-Tempelhof',
              'Allee der Kosmonauten/ Märkische Allee'
              }

# Mapping of known errors to their fixes.
known_corrections = {'Bernauer street': 'Bernauer Straße',
                     'Thomas-Müntzer Straße': 'Thomas-Müntzer-Straße'
                     }
