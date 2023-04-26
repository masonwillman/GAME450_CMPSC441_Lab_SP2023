## Abstract

There are many different aspects to a game. The map, player interactions, and more all have to be addressed during development. By using artificial intelligence, or A.I., these aspects can be tackled much easier. To generate a landscape with hills and oceans, perlin noise can aid in landscape generation. The randomness of perlin noise allows a landscape to be unique and realistic each time the game is played. To generate realistic cities with balanced distances and elevations, a genetic algorithm could be used to find a good layout. Through fitness tests and multiple iterations, it could find a city layout that best matche the criteria. Finally, for the player to be able to customize themselves and their enemies, text-to-speech generation allows for customized sprites. This allows the player to customize their game and experience in a fun way. While there are other ways to solve these problems, A.I. allows for unique, interesting, and efficent solutions. 

## List of AI Components

The AI components that were developed for the game are as follows: a genetic algorithm, perlin noise, and text-to-image generation

## Problems Solved

### Genetic Algorithm

**Problem:** When the game starts, the cities are randomly spread throughout the landscape. Because it is random, cities can be placed right next to each other or extremely far away from each other. They can also be placed directly on top of mountains or in oceans. This makes the map look unrealistic, so what can be used to spread the cities in a realistic manner? 

**Solution:** A genetic algorithm was the solution that was used. It mimics real life evolution to develop an optimal population. First, the program will plot an initial set of ten cities randomly. Then, based on the elevation and distance of the cities, that population is given a fitness. This repeats multiple times to create multiple populations with different fitnesses. Those that are more fit will breed, produce offspring (sets of cities), and those offspring will be given a fitness value. As this cycle continues, a better and better set of cities will be created. Once the program is finished running, it will return the final set of cities. Important to note, a genetic algorithm is only as good as its fitness function. If the program cannot determine the fitness of the population properly, then it will never return a good population. 

**Function Description:** This is located within the lab7 game_fitness function. This has the parameters cities, idx, elevation, and size. Cities is a list of the cities for the game. The idx variable is not used, so it can be ignored. Elevation is a numpy np array that has the elevations for each coordinate on the landscape. Size is the tuple of two ints representing the size of the map. The function starts by getting the cordinates for each city (this is the initial population). Then, for each city, the elevation at the city location is checked. If it is greater than or less than 0.5, then the fitness is decreased by the first fitness scale factor (the value of the elevation). This makes the target fitness the middle elevation, preventing cities from forming in the water or mountains. Then, the program checks the neighboring cities of the current city (1 city and 9 others). The maximium distance is calculated using the size of the map and distance formula, and that is divided by four to get a target distance. Next, the distances between the different cities is calculated using the distance formula. If the distance is above or below the target distance, then the fitness is decreased by the second fitness scale factor (the current distance divided by the maximum distnace). Fitness starts at 1 and is multiplied by both fitness factors to continually decrease it. The closer to 1 the higher the fitness. After all cities are checked, the function will return the fitness value for that population. 

### Perlin Noise

**Problem:** The game takes place on a map. This map should have a landscape with hills, valleys, rivers, and lakes within it. Each time the game begins, a unique landscape should be generated with these features. So the question becomes, how to generate a natural looking landscape for each game iteration?

**Solution:** The perlin_noise library within python gives us this functionality. Think of perlin noise as a static television screen. Some areas are bright white, others are a mute grey, and some are a dark black, and each time a television generates static, it is completely different from the previous time. This is exactly what perlin noise is, and since it is very random, it looks very realistic. 
Applying this to the game, the landscape can be directly generated using perlin noise. From the static television example earlier, white spots can be assigned as low elevation, grey areas as medium elevation, and black areas as high elevation. By doing this, you can have a diverse map of hills, valleys, rivers, and oceans that looks realistic. 

**Function Description:** This is done in the landscape.py get_elevation function. The function takes the size of the map as a tuple of 2 ints and the octaves that will be used for the perlin noise (this is set to 9 by default). First, the x and y values for the size are stored. Then, by using the PerlinNoise function from perlin_noise, the function can generate perlin noise for the landscape. Next, np is used from the nump library to store the noise as an np array called elevation. Essentially, this array will have an elevation value for each coordinate possible for the map size. Finally, the function will return this list of elevations. 

### Text-To-Image Generation

**Problem:** The game must contain a unique A.I. component that was developed by the student. It was recommended to use a hugging face model and create something that would help gameplay and enhance. For example, a journal that could log the adventure of the player charater. The problem has two parts: which A.I. component to use, and how to implement it. 

**Solution:** Text-to-image generation was selected as the individual A.I. component. This would enable the player freedom to choose their player character and opponent character, making the gameplay feel more personal. Text-to-image generation works by taking in a prompt entered by the user. Then, a model will generate an image based on this prompt. Models will be trained on hundreds of thousands of different images. This training allows the model to associate shapes, colors, and more to specific image descriptions. For example, a model will start to understand the general structure of a horse when fed hundreds of horse images, but if only fed one image of a computer, it would have a very surface level understanding. That is why hugging face models were recommended since they are free, reputable pre-trained models that are used in many different areas. 

**Function Description:** This function is called create_image and it is found within lab11 to_image_generation.py. The function takes two string inputs: prompt and image_path. Prompt specifies the decription of the image being generated and image_path specifies the file path for saving the image. Next, the model is set to a stable-diffusion model found on hugging face. Then, a pipe is created that gets the model from the diffuser library. Specifically, the function StableDiffiusionPipline.from_pretrained needs the model from earlier as a parameter. Finally, the prompt is given to the model and the image is saved. There is no technical variable return for this function (it is void), but it will save an image to the approriate file path. 

## Appendix

Mason: get_landscape = lambda pixel_map: elevation_to_rgba(get_elevation(pixel_map)) how can I edit this to also get the value from get_elevation

ChatGPT: To get both the elevation value and the landscape image, you can modify the lambda function as follows:

`get_landscape = lambda pixel_map: (get_elevation(pixel_map), elevation_to_rgba(get_elevation(pixel_map)))`

In this modified version, the lambda function returns a tuple containing two values: the elevation value obtained from `get_elevation(pixel_map)` and the landscape image obtained by passing the elevation value to `elevation_to_rgba()`.

You can now use `get_landscape(pixel_map)` to obtain both the elevation value and the corresponding landscape image for a given pixel map.

Mason: landscape = get_landscape(size) how would that change this piece of code

ChatGPT: If you update the `get_landscape` function as mentioned in my previous answer, you can use it to obtain both the elevation value and the corresponding landscape image as a tuple.

So, if you want to obtain the landscape image and the elevation value for a given `size`, you can use the following code:

`elevation, landscape = get_landscape(size)`

This will assign the elevation value to the variable `elevation` and the landscape image to the variable `landscape`.

Note that you can use any variable names instead of `elevation` and `landscape` as long as you maintain the order of the returned values in the tuple.

Mason: get_landscape = lambda pixel_map: (get_elevation(pixel_map), elevation_to_rgba(get_elevation(pixel_map))) in this code, I want the get_elevation(pixel_map) to be the same value. This means that it cannot be called twice, since this will cause two values to be generated

ChatGPT: If you want to avoid calling `get_elevation(pixel_map)` twice, you can store the result of the function call in a variable and use that variable in both places where the elevation value is needed.

Here's an updated version of the lambda function that stores the result of `get_elevation(pixel_map)` in a variable `elevation` and then returns a tuple containing `elevation` and the corresponding RGBA color value obtained by passing `elevation` to `elevation_to_rgba()`:

`get_landscape = lambda pixel_map: (elevation := get_elevation(pixel_map), elevation_to_rgba(elevation))`

In this version, the `:=` operator is used to assign the result of `get_elevation(pixel_map)` to the variable `elevation` and also use the same value of `elevation` for the call to `elevation_to_rgba()`.

By using this updated version, `get_elevation(pixel_map)` will only be called once, and the same value will be used in both places where the elevation value is needed.

-----------------------------------------------------------------------------

Mason: from diffusers import StableDiffusionPipeline import torch model_id = "runwayml/stable-diffusion-v1-5" pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16) pipe = pipe.to("cuda") prompt = "a photo of an astronaut riding a horse on mars" image = pipe(prompt).images[0] image.save("astronaut_rides_horse.png") How can I edit this code to use the CPU instead of cuda?

ChatGPT: To use the CPU instead of CUDA, you can simply remove the `to("cuda")` method call, like this:

`from diffusers import StableDiffusionPipeline import torch  model_id = "runwayml/stable-diffusion-v1-5" pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)  prompt = "a photo of an astronaut riding a horse on mars" image = pipe(prompt).images[0]        image.save("astronaut_rides_horse.png")`

This will run the model on the CPU by default, without any additional changes needed.

Mason: I am getting an error because of torch.float16, do you know why?

ChatGPT: Yes, the error may occur because some models may not support the `torch.float16` data type. In this case, you can try changing the data type to `torch.float32` instead.

Here's how you can modify the code to use `torch.float32` instead of `torch.float16`:

`from diffusers import StableDiffusionPipeline import torch  model_id = "runwayml/stable-diffusion-v1-5" pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)  prompt = "a photo of an astronaut riding a horse on mars" image = pipe(prompt).images[0]        image.save("astronaut_rides_horse.png")`

This should fix the error you are seeing with `torch.float16`.

