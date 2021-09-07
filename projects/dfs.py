from projects.classes.charts import objects_to_df
from projects.models import Wage, Activity
from projects.models.wage_bills import ConsolidatedWageBillPayment
import pandas as pd

from projects.selectors import wage_bill_selectors
from projects.selectors.wage_bill_selectors import get_wage_bill_sheets


def get_amount_per_day_df(wage_bill):
    df = objects_to_df(ConsolidatedWageBillPayment, wage_bill=wage_bill)
    days_df = df[['tuesday_total_amount', 'wednesday_total_amount', 'thursday_total_amount',
                  'friday_total_amount', 'saturday_total_amount', 'sunday_total_amount',
                  'monday_total_amount'
                  ]]
    days_df.columns = ['Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday']
    days_df_melt = pd.melt(days_df, var_name="Days", value_name="Amount")
    days_amount_per_day = days_df_melt.groupby(["Days"]).sum()
    order = ['Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday']
    days_amount_per_day = days_amount_per_day.reindex(order)
    days_amount_per_day["Days"] = days_amount_per_day.index
    days_amount_per_day.reset_index(drop=True, inplace=True)
    days_amount_per_day.index += 1
    return days_amount_per_day[["Days", "Amount"]]


def get_total_amount_per_field_manager_df(wage_bill):
    df = objects_to_df(ConsolidatedWageBillPayment, wage_bill=wage_bill)
    df["amount"] = df["total_wages"] + df["total_complaints"] - df["total_deductions"]
    payments = df[['field_manager', 'amount']]
    payments.columns = ["Field Manager", "Amount"]
    amount_per_field_manager = payments.groupby(["Field Manager"]).sum()
    amount_per_field_manager["Field Managers"] = amount_per_field_manager.index
    amount_per_field_manager.reset_index(drop=True, inplace=True)
    amount_per_field_manager.sort_values(by=["Amount"], axis=0, ascending=False, inplace=True)
    amount_per_field_manager.index += 1
    return amount_per_field_manager[["Field Managers", "Amount"]]


def get_total_amount_per_supervisor_df(wage_bill):
    df = objects_to_df(ConsolidatedWageBillPayment, wage_bill=wage_bill)
    df["amount"] = df["total_wages"] + df["total_complaints"] - df["total_deductions"]
    payments = df[['supervisor', 'amount']]
    payments.columns = ["Supervisors", "Amount"]
    amount_per_supervisor = payments.groupby(["Supervisors"]).sum()
    amount_per_supervisor["Supervisors"] = amount_per_supervisor.index
    amount_per_supervisor.sort_values(by=["Amount"], axis=0, ascending=False, inplace=True)
    amount_per_supervisor.reset_index(drop=True, inplace=True)
    amount_per_supervisor.index += 1
    return amount_per_supervisor[["Supervisors", "Amount"]]


def get_total_amount_per_activity_df(wage_bill):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)
    df = objects_to_df(Wage, wage_sheet__in=wage_bill_sheets,
                       is_gm_approved=True)
    activity_df = objects_to_df(Activity)
    df = pd.merge(df, activity_df, how="inner", left_on="activity",
                  right_on="id")
    df = df[["name", "quantity", "payment"]]
    payment_per_activity = df.groupby(["name"]).sum()
    payment_per_activity["Activity"] = payment_per_activity.index
    payment_per_activity.sort_values(by=["name"], axis=0, ascending=False, inplace=True)
    payment_per_activity.columns = ["Quantity(Units)", "Payment(UGX)", "Activity"]
    payment_per_activity.reset_index(drop=True, inplace=True)
    payment_per_activity.index += 1
    return payment_per_activity[["Activity", "Quantity(Units)", "Payment(UGX)"]]
