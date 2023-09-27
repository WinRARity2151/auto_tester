from auto_tester.pages.sbis_page import SBISPage


def test_third_scenario():
    sbis = SBISPage()
    sbis.footer_find()
    sbis.download_link()
    sbis.download_plugin()
    sbis.check_file()
