import requests
import json
import helpers
from bs4 import BeautifulSoup
import gsheets_helper

'''
    Helper functions to parse log data into usable info
'''

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

# Admin info
API_KEY_WCLOGS = "9dbc4ede5797bd2399cacf1655735919"
API_KEY_BLIZZARD = "u77x867vyhu2uzbeufvht52fzyey2b8g"

# Fie info
FILE_ZONES = "zones.txt"
FILE_CLASSES = "classes.txt"
FILE_USER_REPORTS = "user_reports.txt"
FILE_GUILD_REPORTS = "guild_reports.txt"

# Url info
URL_ZONES = "https://www.warcraftlogs.com/v1/zones?api_key={}".format(API_KEY_WCLOGS)
URL_CLASSES = "https://www.warcraftlogs.com/v1/classes?api_key={}".format(API_KEY_WCLOGS)
URL_USER_REPORTS = "https://www.warcraftlogs.com/v1/reports/user/{}?api_key={}".format(user_name, API_KEY_WCLOGS)
URL_GUILD_REPORTS = "https://www.warcraftlogs.com/v1/reports/guild/{}/{}/{}?api_key={}".format(player_guild,
                                                                                               player_server,
                                                                                               player_region,
                                                                                               API_KEY_WCLOGS)

URL_WOWANALYZER = "https://wowanalyzer.com/report/{}/{}/{}/player-log-data".format(report_code_temp, 2, player_name)


def read_zones(force_update=False):
    # Reads zone info from file, creates and downloads info
    _zones = []

    if force_update:
        _zones = requests.get(url=URL_ZONES).json()
        f = open(FILE_ZONES, mode="w+")
        for z in _zones:
            f.write(json.dumps(z) + "\n")

        return _zones

    try:
        f = open(FILE_ZONES, mode="r")

        for line in f:
            _zones.append(json.loads(line))

    except FileNotFoundError:
        f = open(FILE_ZONES, mode="w+")
        _zones = requests.get(url=URL_ZONES).json()
        for z in _zones:
            f.write(json.dumps(z) + "\n")

    f.close()

    return _zones


def read_classes(force_update=False):
    # Reads class info from file, creates and downloads info
    _classes = []

    if force_update:
        _classes = requests.get(url=URL_CLASSES).json()
        f = open(FILE_CLASSES, mode="w+")
        for c in _classes:
            f.write(json.dumps(c) + "\n")

        return _classes

    try:
        f = open(FILE_CLASSES, mode="r")

        for line in f:
            _classes.append(json.loads(line))

    except FileNotFoundError:
        f = open(FILE_CLASSES, mode="w+")
        _classes = requests.get(url=URL_CLASSES).json()
        for c in _classes:
            f.write(json.dumps(c) + "\n")

    f.close()

    return _classes


def read_user_reports(force_update=False, url=None):
    # Reads user reports from file, creates and downloads info
    _reports = []

    if force_update or url is not None:
        _reports = requests.get(url=URL_USER_REPORTS if url is None else url).json()
        f = open(FILE_USER_REPORTS, mode="w+")
        for c in _reports:
            f.write(json.dumps(c) + "\n")

    else:

        try:
            f = open(FILE_USER_REPORTS, mode="r")

            for line in f:
                _reports.append(json.loads(line))

        except FileNotFoundError:
            f = open(FILE_USER_REPORTS, mode="w+")
            _reports = requests.get(url=URL_USER_REPORTS).json()
            for c in _reports:
                f.write(json.dumps(c) + "\n")

    f.close()

    return _reports


def read_guild_reports(force_update=False, url=None):
    # Reads guild reports from file, creates and downloads info
    _reports = []

    if force_update or url is not None:
        _reports = requests.get(url=URL_GUILD_REPORTS if url is None else url).json()
        f = open(FILE_GUILD_REPORTS, mode="w+")
        for c in _reports:
            f.write(json.dumps(c) + "\n")

        return _reports

    try:
        f = open(FILE_GUILD_REPORTS, mode="r")

        for line in f:
            _reports.append(json.loads(line))

    except FileNotFoundError:
        f = open(FILE_GUILD_REPORTS, mode="w+")
        _reports = requests.get(url=URL_GUILD_REPORTS).json()
        for c in _reports:
            f.write(json.dumps(c) + "\n")

    f.close()

    return _reports


def fetch_fight_info(report_code=report_code_temp):
    # Returns list of boss fights
    url_report = "https://www.warcraftlogs.com:443/v1/report/fights/{}?api_key={}".format(report_code, API_KEY_WCLOGS)

    _report = requests.get(url_report).json()
    _report = [x for x in _report["fights"] if x["boss"] != 0]  # Filters out trash fights

    return _report


def fetch_fight_table(report_code=report_code_temp, report_metric=report_metric_temp, **kwargs):
    url_report_table = "https://www.warcraftlogs.com:443/v1/report/tables/{}/{}?api_key={}".format(report_metric,
                                                                                                   report_code,
                                                                                                   API_KEY_WCLOGS)
    for k, v in kwargs.items():
        url_report_table += "&{}={}".format(k, v)

    table = requests.get(url_report_table).json()
    return table


def fetch_player_stats(report_code=report_code_temp, **kwargs):
    url_report_table = "https://www.warcraftlogs.com:443/v1/report/events/{}?api_key={}".format(report_code,
                                                                                                API_KEY_WCLOGS)
    for k, v in kwargs.items():
        url_report_table += "&{}={}".format(k, v)

    table = requests.get(url_report_table).json()
    return table


# Creates base urls to use for fetching log data
def create_urls(username=None, character_name=None, character_region=None, character_server=None, character_guild=None,
                report_code=None, report_metric=None):
    """
    :param username: Warcraftlogs account name
    :param character_name: in-game character name
    :param character_region: character server region (US, EU, KR...)
    :param character_server: character server name as returned in Blizzard's slug field (eitrigg, shuhalo...)
    :param character_guild: character guild name, case sensitive
    :param report_code: Warcraftlogs report code (https://www.warcraftlogs.com/reports/FjdTC968vwxRaPMG -> FjdTC968vwxRaPMG)
    :param report_metric: Table type to be returned (Supported values are 'damage-done', 'damage-taken', 'healing', 'casts', 'summons', 'buffs', 'debuffs', 'deaths', 'survivability', 'resources' and 'resources-gains')

    :return: dictionary of urls to be used with GET (user_logs, guild_logs, fight_info, fight_table, )
    """

    _urls = {}
    # User reports
    if username:
        _urls["user_logs"] = "https://www.warcraftlogs.com/v1/reports/user/{}?api_key={}".format(to_slug(username),
                                                                                                 API_KEY_WCLOGS)

    # guild reports
    if None not in [character_guild, character_server, character_region]:
        _urls["guild_logs"] = "https://www.warcraftlogs.com/v1/reports/guild/{}/{}/{}?api_key={}".format(
            to_slug(player_guild),
            to_slug(player_server),
            player_region,
            API_KEY_WCLOGS)

    # list of fights given report code
    if report_code:
        _urls["fight_info"] = "https://www.warcraftlogs.com:443/v1/report/fights/{}?api_key={}".format(report_code,
                                                                                                       API_KEY_WCLOGS)

    # players by report metric todo: use fight_info to pull specific fights
    if None not in [report_code, report_metric]:
        _urls["fight_table"] = "https://www.warcraftlogs.com:443/v1/report/tables/{}/{}?api_key={}".format(
            report_metric, report_code, API_KEY_WCLOGS)

    # wowanalyzer url before fight_id is inserted
    if None not in [report_code, character_name]:
        _urls["wowanalyzer"] = "https://wowanalyzer.com/report/{}/{{}}/{}/player-log-data".format(report_code,
                                                                                                  player_name)

    return _urls


# Converts a string into a format usable in urls, etc.
def to_slug(name):
    name = name.lower()
    name = name.strip("-_',\"")
    return name


# Returns useful stats from combatantinfo event at start of fight
def parse_stats_from_event(event: dict) -> dict:
    USEFUL_STATS = ["strength", "agility", "intellect", "stamina", "critMelee", "hasteMelee", "mastery",
                    "versatilityDamageDone"]
    stats = {k: v for k, v in event.items() if k in USEFUL_STATS}

    # Rename stats
    stats["crit"] = stats.pop("critMelee")
    stats["haste"] = stats.pop("hasteMelee")
    stats["versatility"] = stats.pop("versatilityDamageDone")

    return stats


# Takes basic fight info and returns useful player stats
def fight_to_stats(fight: dict, name: str = player_name) -> dict:
    fight_table = fetch_fight_table(start=fight["start_time"], end=fight["end_time"])
    player_id = next(x for x in fight_table["entries"] if x["name"].lower() == name)["id"]
    initial_events = fetch_player_stats(start=fight["start_time"], end=fight["start_time"] + 1000)
    # print(initial_events, initial_events["events"])
    player_combatantinfo_event = next(
        x for x in initial_events["events"] if x["type"] == "combatantinfo" and x["sourceID"] == player_id)
    return parse_stats_from_event(player_combatantinfo_event)


# Returns spell breakdown in json format
def fight_to_spell_breakdown(fight: dict) -> list:
    USEFUL_STATS = ["name", "total", "uptime", "overheal", "uses", "tickCount", "critHitCount", "critTickCount"]
    _ft = fetch_fight_table(start=fight["start_time"], end=fight["end_time"],
                            sourceid="6")  # todo: variable for sourceid
    fight_time = fight["end_time"] - fight["start_time"]

    spell_breakdown = []

    for spell in sorted(_ft["entries"], key=lambda x: x["total"], reverse=True):
        breakdown_reduced = {}
        # print(spell)

        breakdown_reduced["name"] = spell["name"] if "Chi-Ji" not in spell[
            "name"] else "Invoke Chi-Ji"  # fixes spell name to work with spreadsheet

        if "overheal" in spell:  # Some spells dont have this stat
            overheal_per = spell["overheal"] / (spell["total"] + spell["overheal"])
            breakdown_reduced["overheal"] = helpers.percentage_formatted(overheal_per)

        breakdown_reduced["amount"] = spell["total"]

        if "uses" in spell:
            breakdown_reduced["casts"] = spell["uses"]
            breakdown_reduced["avg_cast"] = spell["total"] // spell["uses"]

        breakdown_reduced["hits"] = spell["tickCount"] + spell["hitCount"]
        breakdown_reduced["avg_hit"] = spell["total"] // breakdown_reduced["hits"]

        breakdown_reduced["crit_percentage"] = helpers.percentage_formatted(
            (spell["critTickCount"] + spell["critHitCount"]) / (breakdown_reduced["hits"]))

        if "uptime" in spell:
            breakdown_reduced["uptime_percentage"] = helpers.percentage_formatted(spell["uptime"] / fight_time)

        spell_breakdown.append(breakdown_reduced)

        # todo: Check if csv file can be requested through api

    # return sorted(ft["entries"], key=lambda x: x["total"], reverse=True)
    return sorted(spell_breakdown, key=lambda x: x["amount"], reverse=True)


# Parses spell breakdown from json format to array directly usable in spreadsheet
def spell_breakdown_to_value_array(breakdown: list) -> list:
    # cell range: D14:L43, 9x30
    cell_height = 30
    cell_width = 9
    headers = ["name", "amount", "casts", "avg_cast", "hits", "avg_hit", "crit_percentage", "uptime_percentage",
               "overheal"]
    values = []

    for spell in breakdown:
        values.append([spell[h] if h in spell else "-" for h in headers])

    for _ in range(cell_height - len(values)):  # Fill empty cells
        values.append([""] * cell_width)

    return values


def fetch_wowanalyzer_log(url, fight_id):
    url_wowanalyzer = url.format(fight_id)

    page = requests.get(url_wowanalyzer)
    soup = BeautifulSoup(page.content, "html.parser")


# Temporary code todo: clean up and relocate reading and parsing code
if __name__ == "__main__":
    # Fetch data #
    urls = create_urls(username=user_name, character_name=player_name, character_guild=player_guild,
                       character_server=player_server, character_region=player_region, report_code=report_code_temp,
                       report_metric=report_metric_temp)
    # static info
    zones = read_zones()
    classes = read_classes()

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
    # start_events = fetch_player_stats(start=fights[0]["start_time"], end=fights[0]["start_time"] + 1)
    # initial_player_data = [x for x in start_events["events"] if x["type"] == "combatantinfo"]
    # print("PLAYER DATA:", *sorted(initial_player_data, key=lambda p: p["sourceID"]), sep="\n")

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

        vals = spell_breakdown_to_value_array(bd)
        print(*vals, sep="\n")

        # Spell breakdown
        # gsheets_helper.update_cells("1-xuSFM6xgMFxgC_r_nca7WQ1UyTSJIghwPw_Ncj__vE", "Player Log!D14:L43", vals)

        # Player log from wowanalyzer
        player_log_data = fetch_wowanalyzer_log(urls["wowanalyzer"], f["id"])

        print()
