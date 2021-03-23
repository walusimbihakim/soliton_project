from projects.models import WageSheet


def retract(wage_sheet: WageSheet):
    wage_sheet.approved = False
    wage_sheet.rejected = False
    wage_sheet.gm_status = None
    wage_sheet.gm_comment = ""
    wage_sheet.manager_status = None
    wage_sheet.manager_comment = ""
    wage_sheet.project_manager_status = None
    wage_sheet.project_manager_comment = ""
    wage_sheet.is_submitted = False
    wage_sheet.save()

