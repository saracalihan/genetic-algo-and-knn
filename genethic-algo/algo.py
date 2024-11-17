import random
import copy
from image import write_pgm_from_patches
import config

# Fitness fonksiyonu: Patch sırasının orijinal sıraya yakınlığını hesaplar
def fitness(individual, target_patches):
    score = 0
    for i in range(len(individual)):
        if individual[i] == target_patches[i]:  # Aynı sırada olan patch'ler
            score += 1
    return score / len(target_patches)  # Normalleştirilmiş fitness değeri

# Rastgele popülasyon başlatma: Patch'lerin farklı sıralamalarını içeren popülasyon
def initialize_population(patches, population_size):
    population = []
    for _ in range(population_size):
        individual = copy.deepcopy(patches)
        random.shuffle(individual)
        population.append(individual)
    return population

# Seçim (Roulette Wheel Selection): Fitness değerlerine göre ebeveyn seçimi
def select_parents(population, fitnesses):
    total_fitness = sum(fitnesses)
    selection_probs = [f / total_fitness for f in fitnesses]
    parents = random.choices(population, weights=selection_probs, k=2)
    return parents

# Çaprazlama (Crossover): İki ebeveyn bireyden yeni bireyler oluştur
def crossover(parent1, parent2):
    cut = random.randint(0, len(parent1))
    child1 = parent1[:cut] + [p for p in parent2 if p not in parent1[:cut]]
    child2 = parent2[:cut] + [p for p in parent1 if p not in parent2[:cut]]
    return child1, child2

# Mutasyon: Patch'lerin sırasını rastgele değiştir
def mutate(individual, mutation_rate=config.mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            swap_with = random.randint(0, len(individual) - 1)
            individual[i], individual[swap_with] = individual[swap_with], individual[i]
    return individual

def inject_new_individuals(population, patches, num_new_individuals=5):
    for _ in range(num_new_individuals):
        new_individual = patches[:]
        random.shuffle(new_individual)
        population.append(new_individual)

# Genetik algoritma fonksiyonu
def genetic_algorithm(target_patches, shuffled_patches, patch_size, width, height, max_val, generations=1000, population_size=50):
    # Orijinal hedef patch sırasını kullanarak popülasyon başlatma
    population = initialize_population(shuffled_patches, population_size)
    best_fitness = 0
    best_individual = None

    final_generation=0
    for generation in range(generations):
        fitnesses = [fitness(ind, target_patches) for ind in population]

        # En iyi bireyi bul ve kaydet
        current_best_fitness = max(fitnesses)
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_individual = population[fitnesses.index(best_fitness)]

        print(f'Generation {generation}: Best Fitness = {best_fitness}')
        write_pgm_from_patches(best_individual, patch_size, width, height, max_val, f'Generations/generation_{generation}.pgm')

        # Hedefe ulaşıldıysa dur
        if best_fitness == 1.0:
            final_generation = generation
            break

        # Yeni popülasyon oluşturma
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = select_parents(population, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            new_population.extend([child1, child2])
        population = new_population[:population_size]

    return final_generation  # En iyi patch sıralamasını döndür

# Şimdi genetic_algorithm fonksiyonunu target_patches kullanarak çağırabilirsiniz
