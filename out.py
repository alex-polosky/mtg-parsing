from datetime import date
from uuid import UUID


class Card():
    arena_id: int
    '''This card's Arena ID, if any. A large percentage of cards are not available on Arena and do not have this ID.'''
    id: UUID
    '''A unique ID for this card in Scryfall's database.'''
    lang: str
    '''A language code for this printing.'''
    mtgo_id: int
    '''This card's Magic Online ID (also known as the Catalog ID), if any. A large percentage of cards are not available on Magic Online and do not have this ID.'''
    mtgo_foil_id: int
    '''This card's foil Magic Online ID (also known as the Catalog ID), if any. A large percentage of cards are not available on Magic Online and do not have this ID.'''
    multiverse_ids: list[int]
    '''This card's multiverse IDs on Gatherer, if any, as an array of integers. Note that Scryfall includes many promo cards, tokens, and other esoteric objects that do not have these identifiers.'''
    tcgplayer_id: int
    '''This card's ID on TCGplayer's API, also known as the productId.'''
    tcgplayer_etched_id: int
    '''This card's ID on TCGplayer's API, for its etched version if that version is a separate product.'''
    cardmarket_id: int
    '''This card's ID on Cardmarket's API, also known as the idProduct.'''
    object: str
    '''A content type for this object, always card.'''
    layout: str
    '''A code for this card's layout.'''
    oracle_id: UUID
    '''A unique ID for this card's oracle identity. This value is consistent across reprinted card editions, and unique among different cards with the same name (tokens, Unstable variants, etc). Always present except for the reversible_card layout where it will be absent; oracle_id will be found on each face instead.'''
    prints_search_uri: str
    '''A link to where you can begin paginating all re/prints for this card on Scryfall's API.'''
    rulings_uri: str
    '''A link to this card's rulings list on Scryfall's API.'''
    scryfall_uri: str
    '''A link to this card's permapage on Scryfall's website.'''
    uri: str
    '''A link to this card object on Scryfall's API.'''

class CardGameplay():
    all_parts: list['CardRelatedCard']
    '''If this card is closely related to other cards, this property will be an array with Related Card Objects.'''
    card_faces: list['CardFace']
    '''An array of Card Face objects, if this card is multifaced.'''
    cmc: float
    '''The card's mana value. Note that some funny cards have fractional mana costs.'''
    color_identity: list[str]
    '''This card's color identity.'''
    color_indicator: list[str]
    '''The colors in this card's color indicator, if any. A null value for this field indicates the card does not have one.'''
    colors: list[str]
    '''This card's colors, if the overall card has colors defined by the rules. Otherwise the colors will be on the card_faces objects, see below.'''
    defense: str
    '''This face's defense, if any.'''
    edhrec_rank: int
    '''This card's overall rank/popularity on EDHREC. Not all cards are ranked.'''
    hand_modifier: str
    '''This card's hand modifier, if it is Vanguard card. This value will contain a delta, such as -1.'''
    keywords: list[str]
    '''An array of keywords that this card uses, such as 'Flying' and 'Cumulative upkeep'.'''
    legalities: dict
    '''An object describing the legality of this card across play formats. Possible legalities are legal, not_legal, restricted, and banned.'''
    life_modifier: str
    '''This card's life modifier, if it is Vanguard card. This value will contain a delta, such as +2.'''
    loyalty: str
    '''This loyalty if any. Note that some cards have loyalties that are not numeric, such as X.'''
    mana_cost: str
    '''The mana cost for this card. This value will be any empty string "" if the cost is absent. Remember that per the game rules, a missing mana cost and a mana cost of {0} are different values. Multi-faced cards will report this value in card faces.'''
    name: str
    '''The name of this card. If this card has multiple faces, this field will contain both names separated by ␣//␣.'''
    oracle_text: str
    '''The Oracle text for this card, if any.'''
    penny_rank: int
    '''This card's rank/popularity on Penny Dreadful. Not all cards are ranked.'''
    power: str
    '''This card's power, if any. Note that some cards have powers that are not numeric, such as *.'''
    produced_mana: list[str]
    '''Colors of mana that this card could produce.'''
    reserved: bool
    '''True if this card is on the Reserved List.'''
    toughness: str
    '''This card's toughness, if any. Note that some cards have toughnesses that are not numeric, such as *.'''
    type_line: str
    '''The type line of this card.'''

class CardPrint():
    artist: str
    '''The name of the illustrator of this card. Newly spoiled cards may not have this field yet.'''
    artist_ids: list[UUID]
    '''The IDs of the artists that illustrated this card. Newly spoiled cards may not have this field yet.'''
    attraction_lights: list
    '''The lit Unfinity attractions lights on this card, if any.'''
    booster: bool
    '''Whether this card is found in boosters.'''
    border_color: str
    '''This card's border color: black, white, borderless, silver, or gold.'''
    card_back_id: UUID
    '''The Scryfall ID for the card back design present on this card.'''
    collector_number: str
    '''This card's collector number. Note that collector numbers can contain non-numeric characters, such as letters or ★.'''
    content_warning: bool
    '''True if you should consider avoiding use of this print downstream.'''
    digital: bool
    '''True if this card was only released in a video game.'''
    finishes: list[str]
    '''An array of computer-readable flags that indicate if this card can come in foil, nonfoil, or etched finishes.'''
    flavor_name: str
    '''The just-for-fun name printed on the card (such as for Godzilla series cards).'''
    flavor_text: str
    '''The flavor text, if any.'''
    frame_effects: list[str]
    '''This card's frame effects, if any.'''
    frame: str
    '''This card's frame layout.'''
    full_art: bool
    '''True if this card's artwork is larger than normal.'''
    games: list[str]
    '''A list of games that this card print is available in, paper, arena, and/or mtgo.'''
    highres_image: bool
    '''True if this card's imagery is high resolution.'''
    illustration_id: UUID
    '''A unique identifier for the card artwork that remains consistent across reprints. Newly spoiled cards may not have this field yet.'''
    image_status: str
    '''A computer-readable indicator for the state of this card's image, one of missing, placeholder, lowres, or highres_scan.'''
    image_uris: dict
    '''An object listing available imagery for this card. See the Card Imagery article for more information.'''
    oversized: bool
    '''True if this card is oversized.'''
    prices: dict
    '''An object containing daily price information for this card, including usd, usd_foil, usd_etched, eur, eur_foil, eur_etched, and tix prices, as strings.'''
    printed_name: str
    '''The localized name printed on this card, if any.'''
    printed_text: str
    '''The localized text printed on this card, if any.'''
    printed_type_line: str
    '''The localized type line printed on this card, if any.'''
    promo: bool
    '''True if this card is a promotional print.'''
    promo_types: list[str]
    '''An array of strings describing what categories of promo cards this card falls into.'''
    purchase_uris: dict
    '''An object providing URIs to this card's listing on major marketplaces. Omitted if the card is unpurchaseable.'''
    rarity: str
    '''This card's rarity. One of common, uncommon, rare, special, mythic, or bonus.'''
    related_uris: dict
    '''An object providing URIs to this card's listing on other Magic: The Gathering online resources.'''
    released_at: date
    '''The date this card was first released.'''
    reprint: bool
    '''True if this card is a reprint.'''
    scryfall_set_uri: str
    '''A link to this card's set on Scryfall's website.'''
    set_name: str
    '''This card's full set name.'''
    set_search_uri: str
    '''A link to where you can begin paginating this card's set on the Scryfall API.'''
    set_type: str
    '''The type of set this printing is in.'''
    set_uri: str
    '''A link to this card's set object on Scryfall's API.'''
    set: str
    '''This card's set code.'''
    set_id: UUID
    '''This card's Set object UUID.'''
    story_spotlight: bool
    '''True if this card is a Story Spotlight.'''
    textless: bool
    '''True if the card is printed without text.'''
    variation: bool
    '''Whether this card is a variation of another printing.'''
    variation_of: UUID
    '''The printing ID of the printing this card is a variation of.'''
    security_stamp: str
    '''The security stamp on this card, if any. One of oval, triangle, acorn, circle, arena, or heart.'''
    watermark: str
    '''This card's watermark, if any.'''
    # preview.previewed_at: date
    # '''The date this card was previewed.'''
    # preview.source_uri: str
    # '''A link to the preview for this card.'''
    # preview.source: str
    # '''The name of the source that previewed this card.'''

class CardFace():
    artist: str
    '''The name of the illustrator of this card face. Newly spoiled cards may not have this field yet.'''
    artist_id: UUID
    '''The ID of the illustrator of this card face. Newly spoiled cards may not have this field yet.'''
    cmc: float
    '''The mana value of this particular face, if the card is reversible.'''
    color_indicator: list[str]
    '''The colors in this face's color indicator, if any.'''
    colors: list[str]
    '''This face's colors, if the game defines colors for the individual face of this card.'''
    defense: str
    '''This face's defense, if the game defines colors for the individual face of this card.'''
    flavor_text: str
    '''The flavor text printed on this face, if any.'''
    illustration_id: UUID
    '''A unique identifier for the card face artwork that remains consistent across reprints. Newly spoiled cards may not have this field yet.'''
    image_uris: dict
    '''An object providing URIs to imagery for this face, if this is a double-sided card. If this card is not double-sided, then the image_uris property will be part of the parent object instead.'''
    layout: str
    '''The layout of this card face, if the card is reversible.'''
    loyalty: str
    '''This face's loyalty, if any.'''
    mana_cost: str
    '''The mana cost for this face. This value will be any empty string "" if the cost is absent. Remember that per the game rules, a missing mana cost and a mana cost of {0} are different values.'''
    name: str
    '''The name of this particular face.'''
    object: str
    '''A content type for this object, always card_face.'''
    oracle_id: UUID
    '''The Oracle ID of this particular face, if the card is reversible.'''
    oracle_text: str
    '''The Oracle text for this face, if any.'''
    power: str
    '''This face's power, if any. Note that some cards have powers that are not numeric, such as *.'''
    printed_name: str
    '''The localized name printed on this face, if any.'''
    printed_text: str
    '''The localized text printed on this face, if any.'''
    printed_type_line: str
    '''The localized type line printed on this face, if any.'''
    toughness: str
    '''This face's toughness, if any.'''
    type_line: str
    '''The type line of this particular face, if the card is reversible.'''
    watermark: str
    '''The watermark on this particulary card face, if any.'''

class CardRelatedCard():
    id: UUID
    '''An unique ID for this card in Scryfall's database.'''
    object: str
    '''A content type for this object, always related_card.'''
    component: str
    '''A field explaining what role this card plays in this relationship, one of token, meld_part, meld_result, or combo_piece.'''
    name: str
    '''The name of this particular related card.'''
    type_line: str
    '''The type line of this card.'''
    uri: str
    '''A URI where you can retrieve a full object describing this card on Scryfall's API.'''

