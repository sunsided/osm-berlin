import os
import re

from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument('file', default='street_names.txt', nargs='?', help='The street name file to use.')
    args = parser.parse_args()

    if not os.path.exists(args.file) or not os.path.isfile(args.file):
        parser.error(f'The specified argument is not a valid file: {args.file}')
        exit(1)

    valid_street_names = [
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
    ]

    # Set of names that are not a way:
    not_a_road = {'U-Bahnhof Alt-Tempelhof',
                  'Allee der Kosmonauten/ Märkische Allee'
                  }

    # Mapping of known errors to their fixes.
    known_corrections = {'Bernauer street': 'Bernauer Straße',
                         'Thomas-Müntzer Straße': 'Thomas-Müntzer-Straße',
                         # It is in the map exactly as written, however that violates the rule, so we fix it.
                         'Klein Schönebecker Straße': 'Klein-Schönebecker Straße'
                         }

    # Mapping of special names that are allowed.
    known_valids = {'Neu Zittauer Straße',
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

    with open(args.file, 'r', encoding='utf-8') as f:
        for line in f:
            name = line.rstrip(os.linesep)

            # Override checks first
            if name in known_valids:
                continue

            if len(name) == 0:
                print('Skipping street: Zero-length name.')
                continue

            if name in not_a_road:
                print('Skipping street: Name does not refer to an actual road: "{name}".')
                continue

            ms = [regex.search(name) for regex in valid_street_names]
            if any(m is not None for m in ms):
                continue

            # Apply the street name fixes:
            if name[0].islower():
                fixed = name[0].upper() + name[1:]
            elif name.endswith('staße'):
                fixed = name[:-5] + 'straße'
            elif name.endswith('promedade'):
                fixed = name[:-9] + 'promenade'
            elif name in known_corrections:
                fixed = known_corrections[name]
            else:
                assert False, 'No correction found for the given street name.'

            print(f'Correcting "{name}" to "{fixed}".')


if __name__ == '__main__':
    main()
