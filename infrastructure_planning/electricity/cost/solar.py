from ...production import adjust_for_losses, prepare_actual_system_capacity


def estimate_panel_cost(
        maximum_consumption_in_kwh_per_year,
        peak_hours_of_sun_per_year,
        system_loss_as_percent_of_total_production,
        panel_table):
    # Estimate desired capacity
    maximum_production_in_kwh_per_year = adjust_for_losses(
        maximum_consumption_in_kwh_per_year,
        system_loss_as_percent_of_total_production / 100.)
    desired_system_capacity_in_kw = maximum_production_in_kwh_per_year / float(
        peak_hours_of_sun_per_year)
    # Choose panel type
    return prepare_actual_system_capacity(
        desired_system_capacity_in_kw, panel_table, 'capacity_in_kw')


def estimate_battery_cost(
        panel_actual_system_capacity_in_kw,
        battery_kwh_per_panel_kw,
        battery_installation_lm_cost_per_battery_kwh,
        battery_maintenance_lm_cost_per_kwh_per_year,
        battery_lifetime_in_years):
    battery_storage_in_kwh = panel_actual_system_capacity_in_kw * \
        battery_kwh_per_panel_kw
    installation_lm_cost = battery_storage_in_kwh * \
        battery_installation_lm_cost_per_battery_kwh
    d = {}
    d['installation_lm_cost'] = installation_lm_cost
    d['maintenance_lm_cost_per_year'] = battery_storage_in_kwh * \
        battery_maintenance_lm_cost_per_kwh_per_year
    d['replacement_lm_cost_per_year'] = installation_lm_cost / float(
        battery_lifetime_in_years)
    return d


def estimate_balance_cost(
        panel_actual_system_capacity_in_kw,
        balance_installation_lm_cost_per_panel_kw,
        balance_maintenance_lm_cost_per_panel_kw_per_year,
        balance_lifetime_in_years):
    installation_lm_cost = panel_actual_system_capacity_in_kw * \
        balance_installation_lm_cost_per_panel_kw
    d = {}
    d['installation_lm_cost'] = installation_lm_cost
    d['maintenance_lm_cost_per_year'] = \
        panel_actual_system_capacity_in_kw * \
        balance_maintenance_lm_cost_per_panel_kw_per_year
    d['replacement_lm_cost_per_year'] = installation_lm_cost / float(
        balance_lifetime_in_years)
    return d