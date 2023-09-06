# -*- coding: utf-8 -*-
import random ; import numpy 

max_cost = numpy.sum(c)

#It calculates the  wAd (Probability of watching the Ad) 
def wAd_segment(t, P, x, seg):
    if (len(t) == 1) and (x[t[0]] == 1):
        return P[seg][t[0]]
    if (len(t) == 1) and (x[t[0]] == 0):
        return 0
    if (t[0] == 'inc') and (x[t[2][0]] == 1):
        return P[seg][t[2][0]]
    
    if (t[0] == 'inc') and (x[t[2][0]] == 0):
        return wAd_segment(t[1], P, x, seg)
    if t[0] == 'exc':
        summation = 0
        for i in range(1, len(t)):
            summation += wAd_segment(t[i], P, x, seg)
        return summation
    if t[0] == 'ind':
        producer = 1
        for i in range(1, len(t)):
            producer *= (1 - wAd_segment(t[i], P, x, seg)) 
        return (1 - producer)
    
#We see how much is left to be covered
def yetToBeCovered(chromosome):
    yetToBeCovered = []
    for i in range(n_segments):
        yetToBeCovered.append(mP[i] - wAd_segment(t[i], P, chromosome, i))
    yetToBeCovered_total = 0
    for i in range(n_segments):
        if yetToBeCovered[i] <= 0:
            yetToBeCovered[i] = 0
        yetToBeCovered_total += yetToBeCovered[i]
    return yetToBeCovered_total

#It calculates the cost
def calculate_cost(chromosome):
    cost = 0
    for i in range(n_media):
        if chromosome[i] == 1:
            cost += c[i]
    return cost

#We create the initial population
def create_initial_population():
    population = []
    for i in range(population_size-1): 
        chromosome = []
        for j in range(n_media):
            chromosome.append(random.randint(0, 1))
        population.append(chromosome)
    population.append(greedy_solution)
    return population

#It sorts the population based on their fitness
def fitness(population):
    fitnesses = []
    for chromosome in population: 
        yetToBeCovered_total = yetToBeCovered(chromosome)
        if yetToBeCovered_total > 0:
            cost = max_cost + (yetToBeCovered_total*1000)
        else:
            cost = calculate_cost(chromosome)   
        fitnesses.append([cost, chromosome])
    fitnesses.sort()
    population = [row[1] for row in fitnesses]
    return population

#Uniform crossing
def uniform_crossover(chromosome1, chromosome2):
    chromosome_new = []
    for i in range(n_media):
        chromosome_new.append(random.choice([chromosome1[i], chromosome2[i]]))
    return chromosome_new

#One-Point crossing
def one_point_crossover(chromosome1, chromosome2):
    n = len(chromosome1)
    point_of_crossover = random.randint(1, n - 1)

    chromosome_new = chromosome1[:point_of_crossover] + chromosome2[point_of_crossover:]
    return chromosome_new
    
#Two-Point crossing
def two_point_crossover(chromosome1, chromosome2):
    n = len(chromosome1)
    point1 = random.randint(1, n - 2)
    point2 = random.randint(point1 + 1, n - 1)

    chromosome_new = chromosome1[:point1] + chromosome2[point1:point2] + chromosome1[point2:]
    return chromosome_new

#We create the roulette that we will use for the crossing
roulette = []
for k in range(0,population_size):
    roulette += [k]*(population_size-k)

#Roulette selection and crossing it's applied
def roulette_selection_and_crossing(population):
    previous_fittest=[]
    for i in range(n_media):
        previous_fittest.append(population[0][i])
    #SELECTION
    order = []  
    for _ in range(n_chromosomes_for_reproduction): 
        order.append(random.choice(roulette))
    #CROSSING
    chromosomes_new_list= []        
    for j in range(n_chromosomes_for_reproduction//2): 
        chromosome_new = uniform_crossover(population[order[2*j]], population[order[2*j+1]])
        chromosomes_new_list.append(chromosome_new)
    for _ in range(n_chromosomes_for_reproduction//2):
        population.pop() #We eliminate the worst of the population
    population += chromosomes_new_list 
    population = fitness(population)
    return population, previous_fittest

#Truncation selection and crossing it's applied
def truncation_selection_and_crossing(population):
    previous_fittest=[]
    for i in range(n_media):
        previous_fittest.append(population[0][i])
    #SELECTION
    order = range((population_size//2)+1)
    #CROSSING
    chromosomes_new_list= []        
    for j in range(n_chromosomes_for_reproduction//2): 
        chromosome_new = uniform_crossover(population[order[2*j]], population[order[2*j+1]])
        chromosomes_new_list.append(chromosome_new)
    for _ in range(n_chromosomes_for_reproduction//2):
        population.pop() #We eliminate the worst of the population
    population += chromosomes_new_list 
    population = fitness(population)
    return population, previous_fittest

#Tournament selection and crossing it's applied
def tournament_selection_and_crossing(population):
    previous_fittest=[]
    for i in range(n_media):
        previous_fittest.append(population[0][i])
    #SELECTION
    order=[]
    for _ in range(n_chromosomes_for_reproduction):
        batch = [random.choice(population‎) for _ in range(int(0.1*population_size)]
        best_in_batch = max(map(calculate_cost, batch))
        order.append(batch.index(best_in_batch))
    
    #CROSSING
    chromosomes_new_list= []        
    for j in range(n_chromosomes_for_reproduction//2): 
        chromosome_new = uniform_crossover(population[order[2*j]], population[order[2*j+1]])
        chromosomes_new_list.append(chromosome_new)
    for _ in range(n_chromosomes_for_reproduction//2):
        population.pop() #We eliminate the worst of the population
    population += chromosomes_new_list 
    population = fitness(population)
    return population, previous_fittest

#Mutation and Elitism it's applied
def mutation(population, previous_fittest):
    for j in range(population_size): 
        if random.randint(1, 100) <= mutation_probability:
            for _ in range(1,random.randint(1, max_genes_mutated)):
                number = random.randint(0, n_media-1)
                if population[j][number] == 1:
                    population[j][number] = 0
                else:
                    population[j][number] = 1
    population = fitness(population)
    if calculate_cost(population[0]) > calculate_cost(previous_fittest):
        population.pop()
        population = [previous_fittest] + population
    return population

#We apply all the previous functions
population = create_initial_population()
population = fitness(population)

for i in range(iterations):
    population, previous_fittest = roulette_selection_and_crossing(population)
    population = mutation(population, previous_fittest)
    
print(population[0])
print(calculate_cost(population[0]))
