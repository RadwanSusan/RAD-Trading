# src/RAD_trading/backtesting/optimization.py
import numpy as np
from deap import base, creator, tools, algorithms
import random
import multiprocessing

# Create DEAP classes only once at the module level
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)


def evaluate(
    individual,
    engine,
    strategy_class,
    symbol,
    timeframe,
    start_date,
    end_date,
    initial_balance,
    param_ranges,
    optimization_metric,
):
    param_dict = dict(zip(param_ranges.keys(), individual))
    results = engine.run_backtest(
        strategy_class,
        symbol,
        timeframe,
        start_date,
        end_date,
        initial_balance,
        param_dict,
    )

    # Check if the optimization metric is available, otherwise use a default metric
    if optimization_metric in results["metrics"]:
        return (results["metrics"][optimization_metric],)
    else:
        print(
            f"Warning: {optimization_metric} not found in metrics. Using total_return instead."
        )
        return (results["metrics"]["total_return"],)


def optimize_strategy(
    engine,
    strategy_class,
    symbol,
    timeframe,
    start_date,
    end_date,
    initial_balance,
    param_ranges,
    optimization_metric="sharpe_ratio",
):
    toolbox = base.Toolbox()

    # Define genes
    for i, (param_name, (low, high)) in enumerate(param_ranges.items()):
        if param_name in ["short_period", "long_period"]:
            toolbox.register(f"attr_{i}", random.randint, int(low), int(high))
        else:
            toolbox.register(f"attr_{i}", random.uniform, low, high)

    # Define individual and population
    toolbox.register(
        "individual",
        tools.initCycle,
        creator.Individual,
        (getattr(toolbox, f"attr_{i}") for i in range(len(param_ranges))),
        n=1,
    )
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    # Evaluation function
    toolbox.register(
        "evaluate",
        evaluate,
        engine=engine,
        strategy_class=strategy_class,
        symbol=symbol,
        timeframe=timeframe,
        start_date=start_date,
        end_date=end_date,
        initial_balance=initial_balance,
        param_ranges=param_ranges,
        optimization_metric=optimization_metric,
    )
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)
    # Parallel evaluation
    pool = multiprocessing.Pool()
    toolbox.register("map", pool.map)
    # Run optimization
    population = toolbox.population(n=50)
    ngen = 10
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    try:
        algorithms.eaSimple(
            population,
            toolbox,
            cxpb=0.5,
            mutpb=0.2,
            ngen=ngen,
            stats=stats,
            verbose=True,
        )
    finally:
        pool.close()
        pool.join()
    best_individual = tools.selBest(population, k=1)[0]
    best_params = dict(zip(param_ranges.keys(), best_individual))
    best_metric = best_individual.fitness.values[0]
    return best_params, best_metric
