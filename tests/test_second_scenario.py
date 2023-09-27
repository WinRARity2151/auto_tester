from auto_tester.pages.sbis_page import SBISPage


def test_second_scenario():
    sbis = SBISPage()
    sbis.open_contacts()
    sbis.region_check("Тюменская")
    sbis.partners_check()
    sbis.change_region()
    sbis.region_check("Камчатский")
    sbis.change_check()
    sbis.url_title_check()
