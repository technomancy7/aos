import pokebase as pb
import os
def action_data():
    return {
    "name": "pokedex",
    "author": "Kaiser",
    "version": "0",
    "features": [],
    "group": "utility",
}
LANGUAGE = ["en"]

def on_help(ctx):
    return """
    Commands:
        pkmn | pokemon | p <name or id>
            Flags:
                    show types: -t
                    show evolves from: -ef
                    show evolution chain: -ev
                    show games: -g
                    show locations: -l
                    show abilities: -a
                    show held items: -hi
                    show stats: -s
                    show all: -all

                    open sprite: --sprite
                    other flags: --back --official --female --other

        item | i <name or id>

        type | t <name or id>

        nature | n <name or id>
    """


def link(ctx, evolution):
    out = ""
    out += f"* [blue]{evolution.species}[/blue] while"

    outr = []
    for req_type in evolution.evolution_details:
        if req_type.gender: outr.append(f"while gender [yellow]{req_type.gender}[/yellow]")
        if req_type.held_item: outr.append(f"holding [yellow]{req_type.held_item}[/yellow]")
        if req_type.item: outr.append(f"using item [yellow]{req_type.item}[/yellow]")
        if req_type.known_move: outr.append(f"knowing move [yellow]{req_type.known_move}[/yellow]")
        if req_type.known_move_type: outr.append(f"knowing move of type [yellow]{req_type.known_move_type}[/yellow]")
        if req_type.location: outr.append(f"at [yellow]{req_type.location}[/yellow]")
        if req_type.min_affection: outr.append(f"affection over [yellow]{req_type.min_affection}[/yellow]")
        if req_type.min_beauty: outr.append(f"beauty over [yellow]{req_type.min_beauty}[/yellow]")
        if req_type.min_happiness: outr.append(f"happiness over [yellow]{req_type.min_happiness}[/yellow]")
        if req_type.min_level: outr.append(f"level over [yellow]{req_type.min_level}[/yellow]")
        if req_type.needs_overworld_rain: outr.append(f"raining [yellow]{req_type.needs_overworld_rain}[/yellow]")
        if req_type.party_species: outr.append(f"party species [yellow]{req_type.party_species}[/yellow]")
        if req_type.party_type: outr.append(f"party type [yellow]{req_type.party_type}[/yellow]")
        if req_type.relative_physical_stats: outr.append(f"stats [yellow]{req_type.relative_physical_stats}[/yellow]")
        if req_type.time_of_day: outr.append(f"time of day is [yellow]{req_type.time_of_day}[/yellow]")
        if req_type.trade_species: outr.append(f"trade species of [yellow]{req_type.trade_species}[/yellow]")
        if req_type.turn_upside_down: outr.append(f"turned upside down [yellow]{req_type.geturn_upside_downnder}[/yellow]")
        out = f"{out} {', '.join(outr)}"
        ctx.writeln(out)
        if(evolution.evolves_to):
            ctx.writeln("")
            ctx.writeln(f"[blue]{evolution.species}[/blue] evolves in to...")
            for sublink in evolution.evolves_to:
                link(ctx, sublink)

def on_load(ctx): 
    cmd = ctx.get_string_ind(0) 
    ctx.update_response(object_type = cmd)
    match cmd:
        case "ability" | "a":
            name = ctx.get_string()[len(cmd)+1:]
            if name.isdigit(): name = int(name)
            ability = pb.ability(name)

            if not hasattr(ability, "id"):
                ability = None
                for item in pb.APIResourceList("ability"):
                    if name.lower() in item['name']:
                        ability = pb.APIResource('ability', item['name'])
                        break

                if ability == None:
                    return ctx.writeln(f"Ability {name} not found.")
 
            ctx.writeln(f"#{ability.id} {ability.name}")
            for effect in ability.effect_entries:  
                if str(effect.language) in LANGUAGE: ctx.writeln(f"{effect.effect}")

        case "item" | "i":
            name = ctx.get_string()[len(cmd)+1:]
            if name.isdigit(): name = int(name)
            item = pb.item(name)
            if not hasattr(item, "id"):
                item = None
                for sitem in pb.APIResourceList("item"):
                    if name.lower() in sitem['name']:
                        item = pb.APIResource('item', sitem['name'])
                        break

                if item == None:
                    return ctx.writeln(f"Item {name} not found.")

            attribs = []
            for attrib in item.attributes: attribs.append(str(attrib))       
            ctx.writeln(f"#{item.id} {item.name} in {item.category}")
            ctx.writeln(f"Attributes: {', '.join(attribs)}")
            for effect in item.effect_entries:  
                if str(effect.language) in LANGUAGE: ctx.writeln(f"{effect.effect}")

        case "nature" | "n":
            name = ctx.get_string()[len(cmd)+1:]
            if name.isdigit(): name = int(name)
            nature = pb.nature(name)
            ctx.writeln(f"#{nature.id} {name}")
            ctx.writeln(f"- strong in {nature.increased_stat}")
            ctx.writeln(f"- weak in {nature.decreased_stat}")

        case "type" | "t":
            name = ctx.get_string()[len(cmd)+1:]
            if name.isdigit(): name = int(name)
            t = pb.type_(name)
            ctx.writeln(f" - {t.name}")
            
            out = []
            for item in t.damage_relations.double_damage_from:
                out.append(str(item))
            
            ctx.writeln(f" - - Takes double damage from: {' '.join(out)}")

            out = []
            for item in t.damage_relations.double_damage_to:
                out.append(str(item))
            ctx.writeln(f" - - Deals double damage to: {' '.join(out)}")

            out = []
            for item in t.damage_relations.half_damage_from:
                out.append(str(item))
            ctx.writeln(f" - - Takes half damage from: {' '.join(out)}")

            out = []
            for item in t.damage_relations.half_damage_to:
                out.append(str(item))
            ctx.writeln(f" - - Deals half damage to: {' '.join(out)}")

        case "pkmn" | "pokemon" | "p":
            c = ctx.touch_config
            show_types = c("pokedex.types") or ctx.has_flag("t")
            show_evolves_from = c("pokedex.evolves") or ctx.has_flag("ef")
            show_evolutions = c("pokedex.evolution") or ctx.has_flag("ev")
            show_games = c("pokedex.games") or ctx.has_flag("g")
            show_locations = c("pokedex.locations") or ctx.has_flag("l")
            show_abilities = c("pokedex.abilities") or ctx.has_flag("a")
            show_held_items = c("pokedex.items") or ctx.has_flag("hi")
            show_stats = c("pokedex.stats") or ctx.has_flag("s")
            show_all = c("pokedex.all") or ctx.has_flag("all")

            name = ctx.get_string()[len(cmd)+1:]
            if name.isdigit(): name = int(name)
            pkmn = pb.pokemon(name)

            if not hasattr(pkmn, "id"):
                pkmn = None
                for pokemon in pb.APIResourceList("pokemon"):
                    if name.lower() in pokemon['name']:
                        pkmn = pb.APIResource('pokemon', pokemon['name'])
                        break

                if pkmn == None:
                    return ctx.writeln(f"Pokemon {name} not found.")

            if ctx.has_flag("sprite"):
                spr = pb.SpriteResource('pokemon', pkmn.id, 
                other=ctx.has_flag("other"),
                official_artwork=ctx.has_flag("official"),
                back=ctx.has_flag("back"),
                female=ctx.has_flag("female"))


                print(spr.path)
                cmdln = ctx.touch_config("apps.image", "xdg-open '$P'")
                os.system(cmdln.replace("$P", spr.path))
                return

            special_tags = []
            special = ""
            if pkmn.species.is_legendary: special_tags.append("L")
            if pkmn.species.is_mythical: special_tags.append("M")
            if pkmn.species.is_baby: special_tags.append("B")
            if len(special_tags) > 0: special = f"[{'|'.join(special_tags)}]"
            ctx.writeln(f"{special}{pkmn.id}: [blue]{pkmn.name}[/blue]")
            ctx.writeln(pkmn.species.generation)
            if show_stats or show_all: 
                ctx.writeln(f"Capture Rate: {pkmn.species.capture_rate} / Height: {pkmn.height} / Weight: {pkmn.weight}")

            if show_types or show_all:
                ctx.writeln("")
                ctx.writeln("Types:")
                for _type in pkmn.types:
                    t = pb.type_(str(_type.type))
                    ctx.writeln(f" - {t.name}")
                    
                    out = []
                    for item in t.damage_relations.double_damage_from:
                        out.append(str(item))
                    
                    ctx.writeln(f" - - Takes double damage from: {' '.join(out)}")

                    out = []
                    for item in t.damage_relations.double_damage_to:
                        out.append(str(item))
                    ctx.writeln(f" - - Deals double damage to: {' '.join(out)}")

                    out = []
                    for item in t.damage_relations.half_damage_from:
                        out.append(str(item))
                    ctx.writeln(f" - - Takes half damage from: {' '.join(out)}")

                    out = []
                    for item in t.damage_relations.half_damage_to:
                        out.append(str(item))
                    ctx.writeln(f" - - Deals half damage to: {' '.join(out)}")

            if((show_evolves_from or show_all) and pkmn.species.evolves_from_species):
                ctx.writeln(f"* Evolves from [blue]{pkmn.species.evolves_from_species}[/blue].")

            evol_chain = pkmn.species.evolution_chain.chain

            if (show_evolutions or show_all) and evol_chain.evolves_to:
                ctx.writeln("")
                ctx.writeln(f"[blue]{evol_chain.species}[/blue] evolves in to...")
                for sublink in evol_chain.evolves_to:
                    link(ctx, sublink)

            if (show_locations or show_all) and len(pkmn.location_area_encounters) > 0:
                ctx.writeln("")
                for encounter in pkmn.location_area_encounters:
                    ctx.writeln(f"* Encountered in {encounter.location_area.name.replace('-', ' ')}")
                    for version in encounter.version_details:
                        vers_str = f"  * {version.version}"
                        #ctx.writeln(f"  * {version.version}")
                        for enc in version.encounter_details:
                            vers_str += f" / [Lv. {enc.min_level}-{enc.max_level}] {enc.method} ({enc.chance}%)"
                            for item in enc.condition_values:
                                vers_str += f" while {item.name}"
                        ctx.writeln(vers_str)


            if show_games or show_all:
                ctx.writeln("")
                games_strings = []
                for game in pkmn.game_indices:
                    games_strings.append(f"[blue]{game.version.name.replace('-', ' ')}[/blue]")
                ctx.writeln(f'Available in {", ".join(games_strings)}')

    return ctx

def on_exit(ctx):
    ctx.delete_text_file() 
