"""Regenerate the README charts in docs/."""
import matplotlib.pyplot as plt

from sens import DECIMALS, DEFAULT_DECIMALS, NAMES, YAW, cm_per_360, convert

# 1. equivalent sensitivity per game for CS2 1.6 @ 800
src, sens, dpi = "cs2", 1.6, 800
vals = {NAMES[g]: convert(sens, src, g, dpi) for g in YAW}
fig, ax = plt.subplots(figsize=(9, 4.5))
bars = ax.barh(list(vals), list(vals.values()), color="#3a6ea5")
ax.bar_label(bars, fmt="%.3f", padding=4)
ax.set_xscale("log")
ax.set_title(f"Same aim feel ({cm_per_360(sens, src, dpi):.1f} cm/360): CS2 {sens} @ {dpi} DPI in every game")
ax.set_xlabel("In-game sensitivity value (log scale)")
fig.tight_layout(); fig.savefig("docs/equivalents.png", dpi=110)

# 2. cm/360 vs DPI: why DPI and sens trade off
fig, ax = plt.subplots(figsize=(9, 4.5))
dpis = list(range(400, 3300, 100))
for s in (0.8, 1.2, 1.6, 2.4):
    ax.plot(dpis, [cm_per_360(s, "cs2", d) for d in dpis], label=f"CS2 sens {s}")
ax.set(title="Higher DPI or higher sens = less mouse travel per 360° turn", xlabel="Mouse DPI", ylabel="cm per 360°")
ax.grid(alpha=0.3); ax.legend()
fig.tight_layout(); fig.savefig("docs/cm360_vs_dpi.png", dpi=110)

# 3. rounding error from the in-game settings box
fig, ax = plt.subplots(figsize=(9, 4.5))
sens_range = [x / 1000 for x in range(500, 4001, 7)]
for g in ("valorant", "overwatch2", "fortnite"):
    err = []
    for s in sens_range:
        exact = convert(s, "cs2", g)
        typed = round(exact, DECIMALS.get(g, DEFAULT_DECIMALS))
        err.append(abs(cm_per_360(typed, g, 800) / cm_per_360(s, "cs2", 800) - 1) * 100)
    ax.plot(sens_range, err, label=NAMES[g], lw=0.9)
ax.set(title="Error from rounding to what the game's settings box accepts", xlabel="CS2 sensitivity", ylabel="Feel error (%)")
ax.grid(alpha=0.3); ax.legend()
fig.tight_layout(); fig.savefig("docs/rounding_error.png", dpi=110)
