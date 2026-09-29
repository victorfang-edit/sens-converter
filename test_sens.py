from sens import YAW, cm_per_360, convert


def test_known_cs_to_valorant_ratio():
    # community-standard ratio: valorant = cs / 3.181818...
    assert abs(convert(1.0, "cs2", "valorant") - 0.022 / 0.07) < 1e-12


def test_round_trip():
    for a in YAW:
        for b in YAW:
            assert abs(convert(convert(2.5, a, b), b, a) - 2.5) < 1e-9


def test_same_feel_means_same_cm360():
    s = convert(1.6, "cs2", "overwatch2", 800)
    assert abs(cm_per_360(1.6, "cs2", 800) - cm_per_360(s, "overwatch2", 800)) < 1e-9


def test_doubling_dpi_halves_sens():
    assert abs(convert(2.0, "cs2", "cs2", 800, 1600) - 1.0) < 1e-12


def test_cs2_reference_value():
    # 1.0 sens @ 800 dpi in CS is ~51.95 cm/360 (widely published figure)
    assert abs(cm_per_360(1.0, "cs2", 800) - 51.95) < 0.01


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"):
            f()
    print("all tests passed")
