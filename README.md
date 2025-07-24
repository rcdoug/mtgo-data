# mtgo-data


## SQL Database Table Declarations
```
create table players
(
	player_id serial primary key,
	username varchar(15) unique
);

create table formats
(
	format_id serial primary key,
	name varchar(30) unique
);

create table cards
(
	card_id serial primary key,
	name varchar(50) unique
);

create table event_types
(
	event_type_id serial primary key,
	name varchar(40) unique
);

create table archetypes
(
	archetype_id serial primary key,
	format_id int references formats(format_id),
	name varchar(30),
	parent_archetype_id int references archetypes(archetype_id),
	unique(format_id, name)
);

create table events
(
	event_id serial primary key,
	format_id int references formats(format_id),
	type varchar(30),
	played_on DATE,
	entries int,
	mtgo_event_id int unique
);

create table decks
(
	decklist_id serial primary key,
	event_id int references events(event_id),
	player_id int references players(player_id),
	archetype_id int references archetypes(archetype_id),
	placement int,
	unique(event_id, player_id)
);

create table deck_contents
(
	decklist_id int references decks(decklist_id),
	card_id int references cards(card_id),
	num_main int,
	num_side int,
	primary key (decklist_id, card_id)
);

create table played_matches
(
	match_id serial primary key,
	event_id int references events(event_id),
	decklist_one_id int references decks(decklist_id),
	decklist_two_id int references decks(decklist_id),
	decklist_winner_id int references decks(decklist_id),
	game_results varchar(7),
	round int,
	unique (event_id, decklist_one, decklist_two, round)
);
```