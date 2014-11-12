# -*- coding: utf-8 -*-

# This script is pretty terrible. Please don't judge me. :(

import re
import os
from pprint import pprint
from collections import defaultdict

def parse_infobox(page, key):
    m = re.search(r'\n\s*\|\s*%s\s*=\s*?(.*?)?\s*(?:\||\n|}})' % key, page)
    if m:
        value = m.group(1).strip()
        value = re.sub(r'\{\{.*?\}\}', '', value).strip()
        value = re.sub(r'\s*\(.*?\)|http.*? |\<\!.*?\>', '', value).strip()
        value = re.sub(r'\[\[.*?\|(.*?\]\])', r'\1', value).strip()
        value = re.sub(r'\[|\]', '', value).strip()
        value = re.sub(r'<small>.*?</small>', '', value).strip()
        value = re.sub(r'<ref.*?>.*?</ref>', '', value).strip()
        value = re.sub(r"''", '', value).strip()
        value = re.sub(r'"', '', value).strip()
        value = filter(lambda x: bool(x) and not x.lower().startswith('see') and not x.lower().startswith('(see'),
                       map(str.strip, re.split(r'<br\s*\/?\s*>|\s*,\s*', value)))
        return value
    else:        
        return []

# Parsing Wikipedia data sucks. Here's a bunch of stuff I couldn't be bothered to figure out how to parse properly.
bands = {'Metal Church': {'current_members': [], 'past_members': ['William McKay', 'Ed Bull', 'Rick Condrin', 'Steve Hott', 'Rick Wagner', 'Aaron Zimpel', 'Carl Sacco', 'Duke Erickson', 'Craig Wells', 'Mike Murphy', 'Tom Weber', 'Kirk Arrington', 'David Wayne', 'Mark Baker', 'John Marshall', 'Mike Howe', 'Brian Lake', 'Jeff Wade', 'Ronny Munroe', 'Jay Reynolds'], 'label': []},
         'Scorpions': {'current_members': [], 'past_members': ['Achim Kirchoff', 'Lothar Heimberg', 'Francis Buchholz', 'Ralph Rieckermann', 'Ken Taylor', 'Ingo Powitzer', 'Wolfgang Dziony', 'Harald Grosskopf', 'Joe Wyman', 'Werner Lohr', 'Jürgen Rosenthal', 'Jurgen Fechter', 'Rudy Lenners', 'Herman Rarebell', 'Bobby Rondinelli', 'Curt Cress', 'Karl-Heinz Vollmer', 'Ulrich Worobiec', 'Michael Schenker', 'Uli Jon Roth', 'Werner Hoyer', 'Bernd Hegner', 'Achim Kirschning'], 'label': []},
         'Stratovarius': {'current_members': [], 'past_members': ['Tuomo Lassila', 'John Vihervä', 'Staffan Stråhlman', 'Jyrki Lentonen', 'Antti Ikonen', 'Jari Behm', 'Timo Tolkki', 'Jari Kainulainen', 'Jörg Michael', 'Katriina \'Miss K\' Wiiala', 'Sami Kuoppamäki', 'Anders Johansson', 'Alex Landenburg'], 'label': []},
         'Dio': {'current_members': [], 'past_members': ['Ronnie James Dio', 'Craig Goldy', 'Simon Wright', 'Scott Warren', 'Rudy Sarzo', 'Vinny Appice', 'Jimmy Bain', 'Jake E. Lee', 'Vivian Campbell', 'Claude Schnell', 'Rowan Robertson', 'Jens Johansson', 'Teddy Cook', 'Tracy G', 'Jeff Pilson', 'Larry Dennison', 'Doug Aldrich', 'Jerry Best', 'Bob Daisley', 'Chuck Garric', 'James Kottak'], 'label': []},
         'Steel Attack': {'current_members': ['Stefan Westerberg', 'John Allan', 'Dennis Vestman', 'Andreas Vollmer'],
                          'past_members': ['Dick Johnson', 'Ronny Hemlin', 'Simon Johansson', 'Freddie', 'Patrick Späth', 'Anden Andersson', 'Johan Löfgren', 'Andreas de Vera', 'Roger Raw', 'Mike Stark', 'Tony Elfving', 'Peter Morén'], 'label': []},
         'Rainbow': {'current_members': [], 'past_members': ['Ritchie Blackmore', 'Ronnie James Dio', 'Gary Driscoll', 'Craig Gruber', 'Micky Lee Soule', 'Cozy Powell', 'Tony Carey', 'Jimmy Bain', 'David Stone', 'Mark Clarke', 'Bob Daisley', 'Roger Glover', 'Don Airey', 'Graham Bonnet', 'Joe Lynn Turner', 'Bobby Rondinelli', 'David Rosenthal', 'Chuck Burgi', 'Paul Morris', 'Greg Smith', 'Doogie White', 'John O\'Reilly', 'John Micelli'], 'label': []},
         'Conception': {'current_members': [], 'past_members': ['Freddy Samsonstuen', 'Werner Skogli', 'Dag Østby', 'Hans Christian Gjestvang', 'Halvor Holter', 'Lars Christian Narum'], 'label': []},
         'Running Wild': {'current_members': [], 'past_members': ['Uwe Bendig', 'Gerald \'Preacher\' Warnecke', 'Majk Moti', 'Axel Morgan', 'Thilo Hermann', 'Bernd Aufermann', 'Jörg Schwarz', 'Carsten David', 'Matthias Kaufmann', 'Stephan Boriss', 'Jens Becker', 'Thomas Smuszynski', 'Peter Pichl', 'Jan S. Eckert', 'Michael Hoffmann', 'Wolfgang \'Hasche\' Hagemann', 'Stefan Schwarzmann', 'Ian Finlay', 'Jörg Michael', 'Rudiger Dreffein', 'Christos Efthimiadis', 'Angelo Sasso', 'Matthias Liebetruth'], 'label': []},
         'Shadowside': {'current_members': [], 'past_members': ['Ricky Slater', 'Bill Shadow', 'Ricardo Piccoli', 'Arc Ray', 'Lucas de Santis', 'A.S. Rock'], 'label': []},
         'Riot V': {'current_members': [], 'past_members': ['Guy Speranza', 'Rhett Forrester', 'Harry \'The Tyrant\' Conklin', 'Tony Moore', 'Mike DiMeo', 'Mike Tirelli', 'Mark Reale', 'L.A. Kouvaris', 'Rick Ventura', 'Phil Feit', 'Jimmy Iommi', 'Kip Leming', 'Pete Perez', 'Peter Bitelli', 'Sandy Slavin', 'Mark Edwards', 'Bobby Jarzombek', 'John Macaluso', 'Pat Magrath', 'Bobby Rondinelli', 'Randy Coven', 'Gerard T. Trevino', 'Ronnie \'Eggman\' Eggers'], 'label': []},
         'Reverend': {'current_members': [], 'past_members': ['David Wayne', 'Michael Lance', 'Scott Marker', 'Eric \'The Viking\' Wayne', 'Davy Lee', 'Chris Nelson', 'Bill Rhynes', 'Brian Korban', 'Stuart Fujinami', 'Ernesto F. Martinez', 'Jay Wegener', 'John Stahlman', 'Dennis O\'Hara', 'Angelo Espino', 'Pete Perez', 'Brendon Kyle', 'Mike Falletta', 'James Cooper', 'Marco Villarreal', 'Rick Basha', 'Jason Ian Rosenfeld', 'Scott Vogel', 'Todd Stotz', 'Jesse Vara', 'Angel Medellin', 'Dave Galbert'], 'label': []},
         'Cellador': {'current_members': [], 'past_members': ['Sam Chatham', 'Valentin Rakhmanov', 'Dave Dahir', 'Bill Hudson', 'Michael Gremio', 'Rick Halverson', 'Mika Horiuchi', 'Yord'], 'label': []},
         'Dungeon': {'current_members': [], 'past_members': ['\'Lord\' Tim Grose', 'Tim Yatras', 'Stu Marshall', 'Glenn Williams', 'Petar Peric', 'Dale Corney', 'Justin Sayers', 'Steve Moore', 'Brendan McDonald', 'Grahame Goode', 'George Smith', 'Carolyn Boon', 'Stephen Mikulic', 'Andrew Brody', 'Wayne Harris', 'Ian DeBono', 'Eddie Trezise', 'Randall Hocking', 'Dale Fletcher', 'Jason Hansen', 'Darryl Reiss'], 'label': []},
         'Avantasia': {'current_members': [], 'past_members': ['Alex Holzwarth', 'Amanda Somerville', 'Andre Matos', 'Andre Neygenfind', 'Bob Catley', 'Cloudy Yang', 'Eric Martin', 'Eric Singer', 'Felix Bohnke', 'Henjo Richter', 'Jørn Lande', 'Kai Hansen', 'Markus Grosskopf', 'Michael Kiske', 'Miro', 'Oliver Hartmann', 'Robert Hunecke-Rizzo', 'Ronnie Atkins', 'Sascha Paeth', 'Thomas Rettke', 'Tobias Sammet', ], 'label': []},
         'Paragon': {'current_members': [], 'past_members': ['Chris Barena', 'Kay Carstens', 'Frank Hellweg', 'Marcus Cremer', 'Wolfgang \'Woko\' Köhler', 'Tommy Eichstädt', 'Daniel Görner', 'Claudius Cremer', 'Günny Kruse', 'Dirk Sturzbecher', 'Uwe Wessel', 'Kay Blanke', 'Dirk Seifert', 'Kay Neuse', 'Markus Corby'], 'label': []},
         'Rage': {'current_members': [], 'past_members': ['Alf Meyerratken', 'Thomas Grüning', 'Jochen Schröder', 'Jörg Michael', 'Rudi Graf', 'Manni Schmidt', 'Chris Efthimiadis', 'Ulli Cohler', 'Spiros Efthimiadis', 'Sven Fischer', 'Christian Wolff', 'Mike Terrana'], 'label': []},
         'Wuthering Heights': {'current_members': [], 'past_members': ['John Sønder', 'Morten Birch', 'Kenneth Saandvig', 'Martin Røpcke', 'Jannik B. Larsen', 'Troels Liebgott', 'Tim Christensen', 'Tim Mogensen', 'Rune S. Brink', 'Morten Nødgaard', 'Kasper Gram', 'Kristian Andrén', 'Peter Jensen', 'Lorenzo Dehò', 'Henrik Flyman', 'Eric Grandin'], 'label': []},
         'Iced Earth': {'current_members': [], 'past_members': ['Richard Bateman', 'Bill Owen', 'Greg Seymour', 'Gene Adam', 'Dave Abell', 'Randall Shawver', 'Mike McGill', 'John Greely', 'Rick Secchiari', 'Rodney Beasley', 'Matt Barlow', 'Mark Prator', 'James MacDonough', 'Larry Tarnowski', 'Steve DiGiorgio', 'Richard Christy', 'Ralph Santolla', 'Tim \'Ripper\' Owens', 'Bobby Jarzombek', 'Ernie Carletti', 'James \'Bo\' Wallace', 'Tim Mills', 'Dennis Hayes', 'Freddie Vidales', 'Brent Smedley', 'Raphael Saini'], 'label': []},
         'Savage Grace': {'current_members': ['Christian Logue', 'Mark \'Chase\' Marshall', 'Derek Peace', 'Mark Marcum'], 'past_members': ['Kenny Powell', 'Brian \'Beast\' East', 'John Birk', 'Mike Smith', 'Dan Finch III', 'Dwight Cliff'], 'label': []},
         'Aquaria': {'current_members': [], 'past_members': [], 'label': ['Avalon', 'Scarecrow Records']},
         'Circle II Circle': {'current_members': [], 'past_members': ['Matt LaPorte', 'John Zahner', 'Kevin Rothney', 'Christopher Kinder', 'Tom Drennan', 'Evan Christopher', 'Lisa Lusby', 'Oliver Palotai', 'Johnny Osborn', 'Rollie Feldman', 'Andy Lee', 'Jayson Moore', 'Bill Hudson'], 'label': []},
         'Lost Horizon': {'current_members': [], 'past_members': ['Daniel Heiman', 'Fredrik Olsson', 'Jeremy Neal Hoffman', 'Christopher Andres Schimke'], 'label': []},
         'X Japan': {'current_members': [], 'past_members': ['Yuji \'Terry\' Izumisawa', 'Tomoyuki \'Tomo\' Ogata', 'Atsushi Tokuo', 'Kenichi \'Eddie Van\' Koide', 'Yoshifumi \'Hally\' Yoshida', 'Mita \'Zen/Xenon\' Kazuaki', 'Hisashi \'Jun/Shu\' Takai', 'Hikaru Utaka', 'Masanori \'Kerry\' Takahashi', 'Satoru Inoue', 'Isao Hori', 'Taiji', 'hide'], 'label': []},
}

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('txt'):
            with open(f) as fh:
                contents = fh.read()
            name = parse_infobox(contents, 'name')
            if len(name) > 0:
                name = name[0]
            else:
                continue
            data = bands.get(name) or defaultdict(list)
            for key in ('current_members', 'past_members', 'label'):
                if not data[key]:
                    data[key] = parse_infobox(contents, key)
            bands[name] = data

band_created = {}
member_created = {}
label_created = {}

def print_member(member, band, color):
    if not band_created.get(band):
        print '"{band}_band" [label="{band}" color="blue"];'.format(band=band)
        band_created[band] = True
    if not member_created.get(member):
        print '"{member}_member" [label="{member}" color="green"];'.format(member=member)
        member_created[member] = True
    print '"{band}_band" -> "{member}_member" [color="{color}"];'.format(band=band, member=member, color=color)

def print_label(label, band):
    if not band_created.get(band):
        print '"{band}_band" [label="{band}" color="blue"];'.format(band=band)
        band_created[band] = True
    if not label_created.get(label):
        print '"{label}_label" [label="{label}" color="yellow"];'.format(label=label)
        label_created[label] = True
    print '"{label}_label" -> "{band}_band";'.format(band=band, label=label)

def print_dot():
    print 'digraph G {'
    for band, data in bands.items():
        members = []
        if data.get('current_members'):
            for member in data['current_members']:
                print_member(member, band, 'green')
        if data.get('past_members'):
            for member in data['past_members']:
                print_member(member, band, 'red')
        if data.get('label'):
            for label in data['label']:
                print_label(label, band)
    print '}'

print_dot()
