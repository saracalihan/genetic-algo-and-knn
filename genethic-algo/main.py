from image import read_pgm, split_into_patches, shuffle_patches, write_pgm, write_pgm_from_patches
from algo import genetic_algorithm
from zip import compress_to_zip
import config
import copy

if(config.patch_size % 2 != 0):
    print(f'ERROR: Patch size must be even! current value is {config.patch_size}.')
    exit()


original_image, width, height, max_val = read_pgm('original.pgm')

if(width%2 !=0):
    print(f"ERROR: Image width({width}px) must be even!")
    exit()


if(height%(config.patch_size//2)!=0):
    print(f"Error: Image height({height}px) is not divisible by ('patch_size/2' => {config.patch_size}/2 => {config.patch_size//2})")
    exit()

config.patch_size = config.patch_size//2

patches = split_into_patches(original_image, config.patch_size)
shuffled_image, rand_patch = shuffle_patches(copy.deepcopy(patches), config.patch_size, width, height)
write_pgm_from_patches(rand_patch, config.patch_size, width, height, max_val,'shuffled.pgm')

# genetic_algorithm(original_image, shuffled_image,  width, height, max_val)

generation = genetic_algorithm(patches, rand_patch, config.patch_size, width, height, max_val, config.generations, config.population_size)
compress_to_zip("Generations", "Generations.zip")
print("'Generations' folder compressed")
config.patch_size = config.patch_size*2

print()
print()
print('\tParameters')
print(f'Patch Size: {config.patch_size}\nImage Size: {width}x{height}\nGenerations: {config.generations}\nPopulations: {config.population_size}\nGeneration Number of Solition: {generation if generation !=0 else "---" }')

