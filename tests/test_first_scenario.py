from auto_tester.pages.sbis_page import SBISPage
from auto_tester.pages.tensor_page import TensorPage


def test_first_scenario():
    sbis = SBISPage()
    tensor = TensorPage()
    sbis.open_contacts()
    sbis.open_banner()
    sbis.open_tenz()
    tensor.find_block()
    tensor.find_about()
    tensor.check_img()
