from projects.classes.charts import Chart
from projects.constants import PALETTE
from projects.dfs import get_amount_per_day_df, get_total_amount_per_field_manager_df, \
    get_total_amount_per_supervisor_df, get_total_amount_per_activity_df


def get_days_of_the_week_chart(wage_bill):
    days_amount_per_day = get_amount_per_day_df(wage_bill)
    bar_chart = Chart('bar', 'Total Payment Per Day', chart_id='bar01', palette=PALETTE)
    bar_chart.from_df(days_amount_per_day, values=['Amount'],
                      labels=["Days"])
    return bar_chart


def get_total_amount_per_field_manager_chart(wage_bill):
    amount_per_field_manager_df = get_total_amount_per_field_manager_df(wage_bill)
    bar_chart = Chart('doughnut', 'Total Amount Per Field Manager', chart_id='doughnut01', palette=PALETTE)
    bar_chart.from_df(amount_per_field_manager_df, values=['Amount'],
                      labels=["Field Managers"])
    return bar_chart


def get_total_amount_per_supervisor_chart(wage_bill):
    amount_per_supervisor_df = get_total_amount_per_supervisor_df(wage_bill)
    chart = Chart('bar', 'Total Amount Per Supervisor', chart_id='pie01', palette=PALETTE)
    chart.from_df(amount_per_supervisor_df, values=['Amount'],
                  labels=["Supervisors"])
    return chart


def get_total_amount_per_activity_chart(wage_bill):
    amount_per_activity_df = get_total_amount_per_activity_df(wage_bill)
    chart = Chart('polarArea', 'Total Payment Per Activity', chart_id='polar01', palette=PALETTE)
    chart.from_df(amount_per_activity_df, values=['Payment(UGX)'],
                  labels=["Activity"])
    return chart


def get_charts(wage_bill):
    charts = []
    bar_chart = get_days_of_the_week_chart(wage_bill)
    doughnut_cart = get_total_amount_per_field_manager_chart(wage_bill)
    supervisor_chart = get_total_amount_per_supervisor_chart(wage_bill)
    payment_per_activity_chart = get_total_amount_per_activity_chart(wage_bill)
    charts.append(bar_chart.get_presentation())
    charts.append(doughnut_cart.get_presentation())
    charts.append(supervisor_chart.get_presentation())
    charts.append(payment_per_activity_chart.get_presentation())
    return charts
