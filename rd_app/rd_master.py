from rd_app.portal import GlobalState
from rd_app.portal.common import navigate_to_page
from rd_app.portal.login import login_to_portal
from rd_app.portal.master import process_rd_accounts
from rd_app.portal.navigation import navigate_to_accounts
from rd_app.wms.processor import get_last_run_details


def process_rd_master(is_rerun=None):
    row, page_number = 0, 1
    if is_rerun:
        row, page_number = get_last_run_details()
        print(f"Page Number: {page_number}, Row: {row}")

    if not GlobalState.is_logged_in:
        login_to_portal()
    navigate_to_accounts()
    if is_rerun:
        navigate_to_page(page_number)
    process_rd_accounts(row, page_number)
