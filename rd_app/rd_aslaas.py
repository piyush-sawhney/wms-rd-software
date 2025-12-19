from rd_app.portal import GlobalState
from rd_app.portal.aslaas import update_card_on_portal
from rd_app.portal.login import login_to_portal
from rd_app.portal.navigation import navigate_to_aslaas
from rd_app.wms.processor import get_non_updated_card_list, update_card_on_wms


def process_aslaas_update():
    non_updated_card_list_dict = get_non_updated_card_list()
    print(f"Total Records fetched for non updated cards: {len(non_updated_card_list_dict)}")
    if non_updated_card_list_dict:
        if not GlobalState.is_logged_in:
            login_to_portal()
        navigate_to_aslaas()
        for item in non_updated_card_list_dict:
            if update_card_on_portal(rd_account_number=item['rd_account_number'], card_number=item['final_card_number']):
                update_card_on_wms(rd_account_number=item['rd_account_number'], card_number=item['final_card_number'])
