from datetime import date, datetime
from uuid import uuid4

types = {
    'Array': 'list',
    'Boolean': 'bool',
    'Colors': 'list[str]',
    'Date': 'date',
    'Decimal': 'float',
    'Integer': 'int',
    'Object': 'dict',
    'String': 'str',
    'URI': 'str',
    'UUID': 'uuid4'
}

props_Core = '''\
arena_id 	Integer 	Nullable 	This card’s Arena ID, if any. A large percentage of cards are not available on Arena and do not have this ID.
id 	UUID 		A unique ID for this card in Scryfall’s database.
lang 	String 		A language code for this printing.
mtgo_id 	Integer 	Nullable 	This card’s Magic Online ID (also known as the Catalog ID), if any. A large percentage of cards are not available on Magic Online and do not have this ID.
mtgo_foil_id 	Integer 	Nullable 	This card’s foil Magic Online ID (also known as the Catalog ID), if any. A large percentage of cards are not available on Magic Online and do not have this ID.
multiverse_ids 	Array 	Nullable 	This card’s multiverse IDs on Gatherer, if any, as an array of integers. Note that Scryfall includes many promo cards, tokens, and other esoteric objects that do not have these identifiers.
tcgplayer_id 	Integer 	Nullable 	This card’s ID on TCGplayer’s API, also known as the productId.
tcgplayer_etched_id 	Integer 	Nullable 	This card’s ID on TCGplayer’s API, for its etched version if that version is a separate product.
cardmarket_id 	Integer 	Nullable 	This card’s ID on Cardmarket’s API, also known as the idProduct.
object 	String 		A content type for this object, always card.
layout 	String 		A code for this card’s layout.
oracle_id 	UUID 	Nullable 	A unique ID for this card’s oracle identity. This value is consistent across reprinted card editions, and unique among different cards with the same name (tokens, Unstable variants, etc). Always present except for the reversible_card layout where it will be absent; oracle_id will be found on each face instead.
prints_search_uri 	URI 		A link to where you can begin paginating all re/prints for this card on Scryfall’s API.
rulings_uri 	URI 		A link to this card’s rulings list on Scryfall’s API.
scryfall_uri 	URI 		A link to this card’s permapage on Scryfall’s website.
uri 	URI 		A link to this card object on Scryfall’s API.'''

props_Gameplay = '''\
all_parts 	Array 	Nullable 	If this card is closely related to other cards, this property will be an array with Related Card Objects.
card_faces 	Array 	Nullable 	An array of Card Face objects, if this card is multifaced.
cmc 	Decimal 		The card’s mana value. Note that some funny cards have fractional mana costs.
color_identity 	Colors 		This card’s color identity.
color_indicator 	Colors 	Nullable 	The colors in this card’s color indicator, if any. A null value for this field indicates the card does not have one.
colors 	Colors 	Nullable 	This card’s colors, if the overall card has colors defined by the rules. Otherwise the colors will be on the card_faces objects, see below.
defense 	String 	Nullable 	This face’s defense, if any.
edhrec_rank 	Integer 	Nullable 	This card’s overall rank/popularity on EDHREC. Not all cards are ranked.
hand_modifier 	String 	Nullable 	This card’s hand modifier, if it is Vanguard card. This value will contain a delta, such as -1.
keywords 	Array 		An array of keywords that this card uses, such as 'Flying' and 'Cumulative upkeep'.
legalities 	Object 		An object describing the legality of this card across play formats. Possible legalities are legal, not_legal, restricted, and banned.
life_modifier 	String 	Nullable 	This card’s life modifier, if it is Vanguard card. This value will contain a delta, such as +2.
loyalty 	String 	Nullable 	This loyalty if any. Note that some cards have loyalties that are not numeric, such as X.
mana_cost 	String 	Nullable 	The mana cost for this card. This value will be any empty string "" if the cost is absent. Remember that per the game rules, a missing mana cost and a mana cost of {0} are different values. Multi-faced cards will report this value in card faces.
name 	String 		The name of this card. If this card has multiple faces, this field will contain both names separated by ␣//␣.
oracle_text 	String 	Nullable 	The Oracle text for this card, if any.
penny_rank 	Integer 	Nullable 	This card’s rank/popularity on Penny Dreadful. Not all cards are ranked.
power 	String 	Nullable 	This card’s power, if any. Note that some cards have powers that are not numeric, such as *.
produced_mana 	Colors 	Nullable 	Colors of mana that this card could produce.
reserved 	Boolean 		True if this card is on the Reserved List.
toughness 	String 	Nullable 	This card’s toughness, if any. Note that some cards have toughnesses that are not numeric, such as *.
type_line 	String 		The type line of this card.'''

props_Print = '''\
artist 	String 	Nullable 	The name of the illustrator of this card. Newly spoiled cards may not have this field yet.
artist_ids 	Array 	Nullable 	The IDs of the artists that illustrated this card. Newly spoiled cards may not have this field yet.
attraction_lights 	Array 	Nullable 	The lit Unfinity attractions lights on this card, if any.
booster 	Boolean 		Whether this card is found in boosters.
border_color 	String 		This card’s border color: black, white, borderless, silver, or gold.
card_back_id 	UUID 		The Scryfall ID for the card back design present on this card.
collector_number 	String 		This card’s collector number. Note that collector numbers can contain non-numeric characters, such as letters or ★.
content_warning 	Boolean 	Nullable 	True if you should consider avoiding use of this print downstream.
digital 	Boolean 		True if this card was only released in a video game.
finishes 	Array 		An array of computer-readable flags that indicate if this card can come in foil, nonfoil, or etched finishes.
flavor_name 	String 	Nullable 	The just-for-fun name printed on the card (such as for Godzilla series cards).
flavor_text 	String 	Nullable 	The flavor text, if any.
frame_effects 	Array 	Nullable 	This card’s frame effects, if any.
frame 	String 		This card’s frame layout.
full_art 	Boolean 		True if this card’s artwork is larger than normal.
games 	Array 		A list of games that this card print is available in, paper, arena, and/or mtgo.
highres_image 	Boolean 		True if this card’s imagery is high resolution.
illustration_id 	UUID 	Nullable 	A unique identifier for the card artwork that remains consistent across reprints. Newly spoiled cards may not have this field yet.
image_status 	String 		A computer-readable indicator for the state of this card’s image, one of missing, placeholder, lowres, or highres_scan.
image_uris 	Object 	Nullable 	An object listing available imagery for this card. See the Card Imagery article for more information.
oversized 	Boolean 		True if this card is oversized.
prices 	Object 		An object containing daily price information for this card, including usd, usd_foil, usd_etched, eur, eur_foil, eur_etched, and tix prices, as strings.
printed_name 	String 	Nullable 	The localized name printed on this card, if any.
printed_text 	String 	Nullable 	The localized text printed on this card, if any.
printed_type_line 	String 	Nullable 	The localized type line printed on this card, if any.
promo 	Boolean 		True if this card is a promotional print.
promo_types 	Array 	Nullable 	An array of strings describing what categories of promo cards this card falls into.
purchase_uris 	Object 	Nullable 	An object providing URIs to this card’s listing on major marketplaces. Omitted if the card is unpurchaseable.
rarity 	String 		This card’s rarity. One of common, uncommon, rare, special, mythic, or bonus.
related_uris 	Object 		An object providing URIs to this card’s listing on other Magic: The Gathering online resources.
released_at 	Date 		The date this card was first released.
reprint 	Boolean 		True if this card is a reprint.
scryfall_set_uri 	URI 		A link to this card’s set on Scryfall’s website.
set_name 	String 		This card’s full set name.
set_search_uri 	URI 		A link to where you can begin paginating this card’s set on the Scryfall API.
set_type 	String 		The type of set this printing is in.
set_uri 	URI 		A link to this card’s set object on Scryfall’s API.
set 	String 		This card’s set code.
set_id 	UUID 		This card’s Set object UUID.
story_spotlight 	Boolean 		True if this card is a Story Spotlight.
textless 	Boolean 		True if the card is printed without text.
variation 	Boolean 		Whether this card is a variation of another printing.
variation_of 	UUID 	Nullable 	The printing ID of the printing this card is a variation of.
security_stamp 	String 	Nullable 	The security stamp on this card, if any. One of oval, triangle, acorn, circle, arena, or heart.
watermark 	String 	Nullable 	This card’s watermark, if any.
preview.previewed_at 	Date 	Nullable 	The date this card was previewed.
preview.source_uri 	URI 	Nullable 	A link to the preview for this card.
preview.source 	String 	Nullable 	The name of the source that previewed this card.'''

props_CardFace = '''\
artist 	String 	Nullable 	The name of the illustrator of this card face. Newly spoiled cards may not have this field yet.
artist_id 	UUID 	Nullable 	The ID of the illustrator of this card face. Newly spoiled cards may not have this field yet.
cmc 	Decimal 	Nullable 	The mana value of this particular face, if the card is reversible.
color_indicator 	Colors 	Nullable 	The colors in this face’s color indicator, if any.
colors 	Colors 	Nullable 	This face’s colors, if the game defines colors for the individual face of this card.
defense 	String 	Nullable 	This face’s defense, if the game defines colors for the individual face of this card.
flavor_text 	String 	Nullable 	The flavor text printed on this face, if any.
illustration_id 	UUID 	Nullable 	A unique identifier for the card face artwork that remains consistent across reprints. Newly spoiled cards may not have this field yet.
image_uris 	Object 	Nullable 	An object providing URIs to imagery for this face, if this is a double-sided card. If this card is not double-sided, then the image_uris property will be part of the parent object instead.
layout 	String 	Nullable 	The layout of this card face, if the card is reversible.
loyalty 	String 	Nullable 	This face’s loyalty, if any.
mana_cost 	String 		The mana cost for this face. This value will be any empty string "" if the cost is absent. Remember that per the game rules, a missing mana cost and a mana cost of {0} are different values.
name 	String 		The name of this particular face.
object 	String 		A content type for this object, always card_face.
oracle_id 	UUID 	Nullable 	The Oracle ID of this particular face, if the card is reversible.
oracle_text 	String 	Nullable 	The Oracle text for this face, if any.
power 	String 	Nullable 	This face’s power, if any. Note that some cards have powers that are not numeric, such as *.
printed_name 	String 	Nullable 	The localized name printed on this face, if any.
printed_text 	String 	Nullable 	The localized text printed on this face, if any.
printed_type_line 	String 	Nullable 	The localized type line printed on this face, if any.
toughness 	String 	Nullable 	This face’s toughness, if any.
type_line 	String 	Nullable 	The type line of this particular face, if the card is reversible.
watermark 	String 	Nullable 	The watermark on this particulary card face, if any.'''

props_RelatedCard = '''\
id 	UUID 		An unique ID for this card in Scryfall’s database.
object 	String 		A content type for this object, always related_card.
component 	String 		A field explaining what role this card plays in this relationship, one of token, meld_part, meld_result, or combo_piece.
name 	String 		The name of this particular related card.
type_line 	String 		The type line of this card.
uri 	URI 		A URI where you can retrieve a full object describing this card on Scryfall’s API.'''


def convert_out(data, cls_name):
    print(f'class {cls_name}():')
    for line in data.split('\n'):
        prop, typ, atn, details = [x.strip().replace('’', "'") for x in line.split('\t')]
        typ = types.get(typ, f'UNKNOWN<{typ}>')
        print(f"    {prop}: {typ}")
        print(f"    '''{details}'''")
    print()


print('from datetime import date')
print('from uuid import uuid4')
print()
print()
for cls_name, data in {
    'Card': props_Core,
    'CardGameplay': props_Gameplay,
    'CardPrint': props_Print,
    'CardFace': props_CardFace,
    'CardRelatedCard': props_RelatedCard,
}.items():
    convert_out(data, cls_name)
