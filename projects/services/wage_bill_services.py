from projects.selectors import wage_bill_selectors


def set_current_wage_bill_status_to_done() -> bool:
    current_wage_bill = wage_bill_selectors.get_current_wage_bill()
    if current_wage_bill:
        current_wage_bill.status = "Done"
        current_wage_bill.save()
        return True
    else:
        return False
