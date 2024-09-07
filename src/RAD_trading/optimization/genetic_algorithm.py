# src\RAD_trading\optimization\genetic_algorithm.py
import random
import numpy as np
from deap import base, creator, tools, algorithms
from ..backtester import Backtester
def genetic_algorithm(strategy_class, param_ranges, data, initial_balance, population_size=50, generations=10):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    for i, (param_name, (low, high)) in enumerate(param_ranges.items()):
        toolbox.register(f"attr_{i}", random.uniform, low, high)
    toolbox.register("individual", tools.initCycle, creator.Individual,
                     (getattr(toolbox, f"attr_{i}") for i in range(len(param_ranges))),
                     n=1)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    def evaluate(individual):
        param_dict = dict(zip(param_ranges.keys(), individual))
        strategy = strategy_class(**param_dict)
        backtester = Backtester()
        backtester.set_starting_balance(initial_balance)
        backtester.set_historical_data(data)
        backtester.set_on_bar(strategy.on_bar)
        trades = backtester.run_backtest()
        sharpe_ratio = backtester.calculate_sharpe_ratio()
        return (sharpe_ratio,)
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)
    population = toolbox.population(n=population_size)
    result, log = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=generations, verbose=True)
    best_individual = tools.selBest(result, k=1)[0]
    best_params = dict(zip(param_ranges.keys(), best_individual))
    return best_params, best_individual.fitness.values[0]
