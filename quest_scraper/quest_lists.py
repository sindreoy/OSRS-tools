def get_pure_quest_list() -> list[str]:
    # Replace with your full quest list (use exact wiki page titles)
    CHUNK_ONE = [
        "Rune Mysteries",
        "The Restless Ghost",
        "Imp catcher",
        "Witch's potion",
        "Doric's quest",
        "Goblin Diplomacy",
        "Witch's house",
        "Druidic Ritual",
        "Death plateau",
        "The knight's sword",
        "Gertrude's cat",
        "Vampyre slayer",
        "Ernest the chicken",
        "The Tourist Trap",
        "Dwarf Cannon",
        "Waterfall Quest",
        "Monk's Friend",
        "Fight Arena",
        "Tree Gnome Village",
    ]

    # 30 Firemaking
    CHUNK_TWO = [
        "Sea slug",
        "Plague city",
        "Biohazard",
        "Fishing contest",
        "Demon slayer",
        "Cook's assistant",
        "Recipe for Disaster/Another Cook's Quest",
        "Recipe for Disaster/Freeing the Goblin generals",
        "Recipe for Disaster/Freeing the Mountain Dwarf",
        "Murder Mystery",
        "Hazeel Cult",
        "X Marks the Spot",
        "Client of Kourend",
        "The Queen of Thieves",
        "Tribal Totem",
        "The Lost Tribe",
        "Death to the Dorgeshuun",
        "Children of the Sun",
        "Shield of Arrav",
        "Ethically Acquired Antiquities",
        "The Feud",
        "Death on the Isle",
        "Jungle Potion",
    ]

    # 10 herblore
    CHUNK_THREE = [
        "The Dig Site",
        "Mountain Daughter",
        "The Giant Dwarf",
        "Priest in Peril",
        "Ghosts Ahoy",
        "Making History",
        "Horror from the Deep",
        "Elemental Workshop I",
        "The golem",
        "Elemental Workshop II",  # optional, start while at Dig Site in The Golem quest,
        "Sleeping Giants",  # optional
        "Shades of Mort'ton",  # optional
        "Shadow of the storm",
        "Recipe for Disaster/Freeing Evil Dave",
    ]

    # 30 cooking
    CHUNK_FOUR = [
        "Big Chompy Bird Hunting",
        "Tai Bwo Wannai Trio",
        "Recipe for Disaster/Freeing Pirate Pete",
    ]

    # 41 cooking
    CHUNK_FIVE = [
        "Recipe for Disaster/Freeing Skrach Uglogwee",
        "Another Slice of H.A.M",  # optional
    ]

    # 40 mining
    CHUNK_SIX = [
        "Watchtower",  # optional
        "Icthlarin's Little Helper",  # optional
        "Contact!",  # optional, also hard without prayer
        "Twilight's Promise",
        "A Porcine of Interest",
    ]

    # 35 woodcutting
    CHUNK_SEVEN = [
        "Animal Magnetism",
        "Lost City",
        "The Forsaken Tower",  # optional
        "Troll Stronghold",
    ]

    # 31 herblore
    CHUNK_NINE = [
        "Eadgar's Ruse",
        "Troll Romance",
        "Haunted Mine",
        "Underground Pass",  # optional, gives attack xp
    ]

    # 26 construction
    CHUNK_TEN = [
        "Getting Ahead",  # optional
        "Shilo Village",  # optional
        "Family Crest",  # optional
        "Scorpion Catcher",
        "Desert Treasure",
        "Curse of the Empty Lord",
    ]

    # 60 magic
    CHUNK_ELEVEN = ["Mage Arena I"]

    QUESTS = (
        CHUNK_ONE
        + CHUNK_TWO
        + CHUNK_THREE
        + CHUNK_FOUR
        + CHUNK_FIVE
        + CHUNK_SIX
        + CHUNK_SEVEN
        + CHUNK_NINE
        + CHUNK_TEN
        + CHUNK_ELEVEN
    )
    return QUESTS
