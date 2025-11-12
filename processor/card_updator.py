from processor.portal.aslass_module import get_non_updated_card_records, update_card_on_portal, \
    update_card_status_to_wms
from processor.portal.navigation_module import navigate_to_aslaas


def update_card_flow():
    non_updated_card_list = get_non_updated_card_records()
    if non_updated_card_list and len(non_updated_card_list) > 0:
        print(non_updated_card_list)
        navigate_to_aslaas()
        for account_no, card_number in non_updated_card_list:
            if update_card_on_portal(account_no, card_number):
                update_card_status_to_wms(account_no)


