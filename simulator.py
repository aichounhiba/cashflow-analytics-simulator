import numpy as np
import pandas as pd

class CashFlowSimulator:
    def __init__(self, initial_cash, monthly_fixed_costs, avg_monthly_revenue, revenue_volatility):
        self.initial_cash = initial_cash
        self.fixed_costs = monthly_fixed_costs
        self.avg_revenue = avg_monthly_revenue
        self.volatility = revenue_volatility

    def run_simulation(self, months=12, simulations=100):
        np.random.seed(42) 
        cash_paths = np.zeros((months + 1, simulations))
        cash_paths[0, :] = self.initial_cash
        
        for t in range(1, months + 1):
            simulated_revenues = np.random.normal(
                loc=self.avg_revenue, 
                scale=self.avg_revenue * self.volatility, 
                size=simulations
            )
            net_cash_flow = simulated_revenues - self.fixed_costs
            cash_paths[t, :] = cash_paths[t - 1, :] + net_cash_flow
            
        return cash_paths

    def calculate_metrics(self, cash_paths):
        median_path = np.median(cash_paths, axis=1)
        pessimistic_path = np.percentile(cash_paths, 5, axis=1)
        optimistic_path = np.percentile(cash_paths, 95, axis=1)
        
        runway_months = None
        for month, cash in enumerate(median_path):
            if cash <= 0:
                runway_months = month
                break
                
        return {
            "median": median_path,
            "pessimistic": pessimistic_path,
            "optimistic": optimistic_path,
            "runway": runway_months if runway_months is not None else "Stable (+12 mois)"
        }