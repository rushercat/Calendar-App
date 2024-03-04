def test_next_month():
    global monthGlobal, yearGlobal
    monthGlobal = 12
    yearGlobal = 2023
    next_month()
    assert monthGlobal == 1
    assert yearGlobal == 2024

    monthGlobal = 6
    yearGlobal = 2022
    next_month()
    assert monthGlobal == 7
    assert yearGlobal == 2022