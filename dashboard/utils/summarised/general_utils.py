from lenga.settings.local import NO_PATNER_IDS


def get_no_partners():
    no_partner_ids = ""
    for w in NO_PATNER_IDS:
        no_partner_ids += "'{}',".format(w)

    no_partner_ids = no_partner_ids[1:-2]
    no_partner_ids_list = no_partner_ids.split()

    return no_partner_ids, no_partner_ids_list


def get_module_english_name(module_number):
    module_number = int(module_number)

    if module_number == 1:
        return "Track your money"
    elif module_number == 2:
        return "Make a budget"
    elif module_number == 3:
        return "Make a savings plan"
    elif module_number == 4:
        return "Saving in a group"
    elif module_number == 5:
        return "Saving in a financial institution or mobile service"
    elif module_number == 6:
        return "Prepare to borrow"

