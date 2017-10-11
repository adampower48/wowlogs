from log_reader import *

# Player info
user_name = "adamthedash"
player_name = "adamthesmash"
player_class = "monk"
player_spec = "mistweaver"
player_region = "US"
player_server = "eitrigg"
player_server_alt = "Shuhalo"
player_guild = "HEATHENS"

# Temp report info
report_code_temp = "FjdTC968vwxRaPMG"
report_metric_temp = "healing"

# Temporary code todo: clean up and relocate reading and parsing code
if __name__ == "__main__":
    # Fetch data #
    urls = create_urls(username=user_name, character_name=player_name, character_guild=player_guild,
                       character_server=player_server, character_region=player_region, report_code=report_code_temp,
                       report_metric=report_metric_temp)
    # static info
    zones = read_zones(force_update=False)
    classes = read_classes(force_update=False)

    # Dynamic play/guild info

    user_reports = read_user_reports(url=urls["user_logs"]) if "user_logs" in urls else []
    guild_reports = read_guild_reports(url=urls["guild_logs"]) if "guild_logs" in urls else []

    # Print data
    # print(*zones, sep="\n")
    #
    # print()
    # print(*classes, sep="\n")

    print()
    print(*[r for r in user_reports if r["zone"] == 13], sep="\n")

    print()
    print(*[r for r in guild_reports if r["zone"] == 13 and r["owner"] == user_name], sep="\n")

    print()
    fights = fetch_fight_info()
    print("FIGHTS:", *fights, sep="\n")
    print()

    # print()
    # fight = fetch_fight_table(start=fights[0]["start_time"], end=fights[0]["end_time"])
    # print("FIGHT ENTRIES:", *sorted(fight["entries"], key=lambda p: p["id"]), sep="\n")

    # print()
    # player_fight_data = [x for x in fight["entries"] if x["name"].lower() == player_name][0]
    # print("PLAYER FIGHT DATA:", *["{}: {}".format(k, v) for k, v in player_fight_data.items()], sep="\n")
    #
    # print()
    # print("Name:", player_fight_data["name"])
    # print("Class:", player_fight_data["icon"])
    # print("Dps:", player_fight_data["total"] // (player_fight_data["activeTime"] // 1000))
    # # print(*player_fight_data["gear"], sep="\n")

    # print()

    # Link player stats to player
    # player_stats_event = [x for x in initial_player_data if x["sourceID"] == player_fight_data["id"]][0]
    # print()
    # print("PLAYER STATS:", *["{}: {}".format(k, v) for k, v in parse_stats_from_event(player_stats_event).items()],
    #       sep="\n")  # only required stats
    # print("PLAYER STATS:", *["{}: {}".format(k, v) for k, v in player_stats_event.items()], sep="\n")  # all stats

    for f in fights[0:1]:
        print(f["name"])
        ft = fetch_fight_table(start=f["start_time"], end=f["end_time"], sourceid="6")
        ft["entries"].sort(key=lambda x: x["total"], reverse=True)
        # print(*["{}: {}".format(k, v) for k, v in ft["entries"][0].items()], sep="\n")
        # print(*sorted(ft["entries"], key=lambda x: x["total"], reverse=True), sep="\n")
        stats = fight_to_stats(f)
        print(helpers.print_dict(stats))
        print()

        print("SPELL BREAKDOWN:")
        bd = fight_to_spell_breakdown(f)
        print(*bd, sep="\n")
        print()

        print("Player log")
        player_log = get_player_log(f, report_code_temp)
        print(helpers.print_dict(player_log))

        vals = spell_breakdown_to_value_array(bd)
        # print(*vals, sep="\n")

        # Spell breakdown
        # gsheets_helper.update_cells("1-xuSFM6xgMFxgC_r_nca7WQ1UyTSJIghwPw_Ncj__vE", "Player Log!D14:L43", vals)

        # Player log from wowanalyzer
        player_log_data = fetch_wowanalyzer_log(urls["wowanalyzer"], f["id"])

        print()
