login_elements = {'username': 'AuthenticationFG.USER_PRINCIPAL', 'password': 'AuthenticationFG.ACCESS_CODE',
                  'login': 'VALIDATE_RM_PLUS_CREDENTIALS_CATCHA_DISABLED', 'logout_1': 'HREF_Logout',
                  'logout_2': 'LOG_OUT', 'captcha_box': 'AuthenticationFG.VERIFICATION_CODE'}

navigation_elements = {'accounts': 'Accounts', 'deposit_accounts': 'Agent Enquire & Update Screen',
                       'fetch': 'Button3087042', 'page_next': "Action.AgentRDActSummaryAllListing.GOTO_NEXT__",
                       'back_button': "backButton",
                       'next_select_account': "Action.AgentRDActSummaryAllListing.GOTO_NEXT__",
                       'next_add_account': "Action.SelectedAgentRDActSummaryListing.GOTO_NEXT__",
                       'add_account_page_number': "CustomAgentRDAccountFG.SelectedAgentRDActSummaryListing_REQUESTED_PAGE_NUMBER",
                       'add_account_go': "Action.SelectedAgentRDActSummaryListing.GOTO_PAGE__", 'reports': "Reports",
                       'agent_id': "HREF_OutputTextbox12662076", 'aslaas_update': "Update ASLAAS Number"}

reports_download = {'start_date': 'CustomAgentRDAccountFG.REPORT_DATE_FROM',
                    'end_date': 'CustomAgentRDAccountFG.REPORT_DATE_TO',
                    'schedule_number': 'CustomAgentRDAccountFG.EBANKING_REF_NUMBER', 'search_button': 'SearchBtn'}

schedule_download = {'download_file': 'GENERATE_REPORT',
                     'schedule_number': 'HREF_CustomAgentRDAccountFG.EBANKING_REF_NUMBER_ARRAY',
                     'account_number': 'HREF_CustomAgentRDAccountFG.SAVED_ACCOUNT_NUMBER_ARRAY',
                     'deposit_amount': 'HREF_CustomAgentRDAccountFG.SAVED_RD_INSTALLMENT_AMOUNT_ARRAY',
                     'no_of_installment': 'HREF_CustomAgentRDAccountFG.NO_OF_INSTALLMENT_ARRAY',
                     'rebate': 'HREF_CustomAgentRDAccountFG.RD_REBATE_ARRAY',
                     'default_fee': 'HREF_CustomAgentRDAccountFG.RD_DEFAUT_FEE_ARRAY',
                     'date_time': 'HREF_CustomAgentRDAccountFG.LAST_CREATE_DATE_ARRAY',
                     'page_input': 'CustomAgentRDAccountFG.RecurringInstallmentReportScreenListing_REQUESTED_PAGE_NUMBER',
                     'go_to_page': 'Action.RecurringInstallmentReportScreenListing.GOTO_PAGE__',
                     'go_to_next': 'Action.RecurringInstallmentReportScreenListing.GOTO_NEXT__',
                     'schedule_number_input':'CustomAgentRDAccountFG.EBANKING_REF_NUMBER'}

schedule_elements = {'search': 'CustomAgentRDAccountFG.ACCOUNT_NUMBER_FOR_SEARCH',
                     'account_no_check_box': 'CustomAgentRDAccountFG.SELECT_INDEX_ARRAY',
                     'save_accounts': 'Button26553257', 'no_of_installment': 'CustomAgentRDAccountFG.RD_INSTALLMENT_NO',
                     'rebate_default_button': 'Button22426525', 'rebate': 'HREF_CustomAgentRDAccountFG.REBATE',
                     'default': 'HREF_CustomAgentRDAccountFG.DEFAULT_FEE',
                     'cheque_no': 'CustomAgentRDAccountFG.RD_CHEQUE_NO',
                     'cheque_acc_no': 'CustomAgentRDAccountFG.RD_ACCOUNT_NUMBER_FOR_PAYMENT',
                     'card_number_input': 'CustomAgentRDAccountFG.ASLAAS_NO', 'save_modification': 'Button11874602',
                     'modified_status': 'HREF_CustomAgentRDAccountFG.MODIFIED_ARRAY',
                     'pay_schedule': 'PAY_ALL_SAVED_INSTALLMENTS', 'reference_no': 'errorlink1'}

schedule_update_elements = {'account_no': 'HREF_CustomAgentRDAccountFG.ACCOUNT_NUMBER_ARRAY'}

account_details = {'account_no_summary': 'HREF_CustomAgentRDAccountFG.ACCOUNT_NUMBER_ALL_ARRAY',
                   'account_no': 'HREF_CustomAgentRDAccountFG.ACCOUNT_NUMBER',
                   'account_name': 'HREF_CustomAgentRDAccountFG.ACCOUNT_NICKNAME',
                   'account_opening_date': 'HREF_CustomAgentRDAccountFG.RD_ACCOUNT_OPEN_DATE',
                   'denomination': 'HREF_CustomAgentRDAccountFG.RD_DESPOSIT_AMOUNT',
                   'total_deposit_amount': 'HREF_CustomAgentRDAccountFG.RD_TOTAL_DESPOSIT_AMOUNT',
                   'month_paid_upto': 'HREF_CustomAgentRDAccountFG.MONTH_PAID_UPTO_BASIC',
                   'next_installment_date': 'HREF_CustomAgentRDAccountFG.NEXT_RD_INSTALLMENT_DATE',
                   'last_date_of_deposit': 'HREF_CustomAgentRDAccountFG.DATE_OF_LAST_DEPOSIT',
                   'rebate': 'HREF_CustomAgentRDAccountFG.REBATE',
                   'default_fee': 'HREF_CustomAgentRDAccountFG.DEFAULT_FEE',
                   'pending_installment': 'HREF_CustomAgentRDAccountFG.PENDING_INSTALLMENT',
                   'default_installments': 'HREF_CustomAgentRDAccountFG.DEFAULT_INSTALLMENT'}

aslaas_update = {'account_no': 'CustomAgentAslaasNoFG.RD_ACC_NO', 'aslaas_number': 'CustomAgentAslaasNoFG.ASLAAS_NO',
                 'continue': 'LOAD_CONFIRM_PAGE', 'add': 'ADD_FIELD_SUBMIT', 'success': 'errorlink1'}
