"""Convert mouse sensitivity between games so aiming feels identical.

Every game turns the camera by  counts x sensitivity x yaw  degrees, where
'counts' come from the mouse (DPI = counts per inch) and 'yaw' is a constant
baked into the game. Matching degrees-per-inch across games = same feel.

usage:
  python sens.py cs2 valorant 1.6 --dpi 800
  python sens.py cs2 all 1.6 --dpi 800
  python sens.py cs2 valorant 1.6 --dpi 800 --to-dpi 1600
"""
import argparse

# degrees turned per mouse count at sensitivity 1.0 (hipfire, 1:1 zoom sens)
YAW = {
    "cs2": 0.022,
    "valorant": 0.07,
    "apex": 0.022,
    "tf2": 0.022,
    "overwatch2": 0.0066,
    "cod": 0.0066,        # MW / Warzone / BO6, "legacy" sensitivity setting
    "fortnite": 0.005555,  # slider shown as a percentage
}
NAMES = {"cs2": "Counter-Strike 2", "valorant": "Valorant", "apex": "Apex Legends", "tf2": "Team Fortress 2",
         "overwatch2": "Overwatch 2", "cod": "Call of Duty", "fortnite": "Fortnite"}
DECIMALS = {"valorant": 3, "overwatch2": 2, "fortnite": 1, "cod": 2}  # what the in-game box accepts
DEFAULT_DECIMALS = 4  # cs2 / apex / tf2 accept long decimals via console or config


def convert(sens, src, dst, dpi=800, to_dpi=None):
    to_dpi = to_dpi or dpi
    return sens * YAW[src] * dpi / (YAW[dst] * to_dpi)


def cm_per_360(sens, game, dpi):
    """Mouse travel for one full turn: the universal way to compare sensitivity."""
    counts = 360 / (sens * YAW[game])
    return counts / dpi * 2.54


def edpi(sens, dpi):
    return sens * dpi


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", choices=YAW)
    ap.add_argument("dst", choices=[*YAW, "all"])
    ap.add_argument("sens", type=float)
    ap.add_argument("--dpi", type=int, default=800)
    ap.add_argument("--to-dpi", type=int)
    a = ap.parse_args()
    if a.sens <= 0 or a.dpi <= 0 or (a.to_dpi is not None and a.to_dpi <= 0):
        ap.error("sensitivity and DPI must be positive")

    to_dpi = a.to_dpi or a.dpi
    base = cm_per_360(a.sens, a.src, a.dpi)
    print(f"Source: {NAMES[a.src]} {a.sens} @ {a.dpi} DPI  ->  {base:.2f} cm/360 ({base / 2.54:.2f} in), eDPI {edpi(a.sens, a.dpi):.0f}\n")
    print(f"{'Game':<18}{'Exact sens':>12}{'Type in-game':>14}{'cm/360':>9}{'Error':>9}")
    print("-" * 62)
    for g in (YAW if a.dst == "all" else [a.dst]):
        exact = convert(a.sens, a.src, g, a.dpi, to_dpi)
        typed = round(exact, DECIMALS.get(g, DEFAULT_DECIMALS))
        cm = cm_per_360(typed, g, to_dpi)
        print(f"{NAMES[g]:<18}{exact:>12.4f}{typed:>14}{cm:>9.2f}{(cm - base) / base:>+9.2%}")
    if to_dpi != a.dpi:
        print(f"\n(converted for a new mouse DPI of {to_dpi})")


if __name__ == "__main__":
    main()
