from rd_app.portal import GlobalState
from rd_app.portal.login import login_to_portal
from rd_app.portal.master import process_rd_accounts
from rd_app.portal.navigation import navigate_to_accounts
from rd_app.wms.processor import get_last_run_details


def process_rd_master(is_rerun=None):
    row, page_number = 0, 1
    if is_rerun:
        row, page_number = get_last_run_details()

    if not GlobalState.is_logged_in:
        login_to_portal()
    navigate_to_accounts()
    process_rd_accounts(row, page_number)
