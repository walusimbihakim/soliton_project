from projects.models.boqs import BOQ


def create_boq_from_survey(survey):
    try:
        boq = BOQ.objects.create(
            survey=survey
        )
    except Exception:
        boq = survey.boq
    return boq
