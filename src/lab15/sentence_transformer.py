'''
Lab15:

Ask ChatGPT a question. Copy the response into a string. Regenerate the response.

(2pts) Split both the text into sentences. Compare the sentences across the two responses for similarity using sentence transformers. 

Sentence transformer's sentence similarity will give you a score for similarity between two sentences in the range of [0, 1].

(3pts) Come up with a metric to assess overall similarity between the two texts. Best answer is unknown. Please describe the metric you came up with comments.
'''

# Imports necessary packages
from sentence_transformers import SentenceTransformer, util
import nltk
nltk.download('punkt')


'''
Question asked: Why is the sky blue?

This code uses the sentence-transformer hugging face documentation and ChatGPT to create this program
1. The code has two responses that were generated from ChatGPT
2. These text blocks are split into individual sentences using nltk
3. Then, the first, second, third, fourth, and fifth sentences in each response are compared to one another

'''

if __name__ == "__main__":

    # Keeps track of scores
    scores = []

    # Responses recieved from ChatGPT
    response1 = "The sky appears blue because of a phenomenon called Rayleigh scattering. When sunlight enters the Earth's atmosphere, it collides with gas molecules, such as nitrogen and oxygen, which scatter the light in all directions. Blue light has a shorter wavelength and higher energy than other colors of light, so it is scattered more easily than other colors. This means that more blue light is scattered in all directions, giving the sky a blue hue. At sunset or sunrise, the sun is lower on the horizon and the light must travel through more of the Earth's atmosphere, which scatters even more of the blue light, making the sky appear more red or orange."
    response2 = "The blue color of the sky is due to a phenomenon called Rayleigh scattering. When sunlight enters the Earth's atmosphere, it collides with gas molecules, such as nitrogen and oxygen, and scatters in all directions. Blue light has a shorter wavelength and is more easily scattered than other colors, which is why the sky appears blue to our eyes. As the sunlight continues to travel through the atmosphere, the blue light continues to scatter, making the sky appear blue from all directions. At sunrise and sunset, when the sunlight must travel through more of the Earth's atmosphere to reach our eyes, the shorter blue wavelengths are scattered even more, leaving mostly longer wavelength colors like red and orange, giving us the beautiful colors we see during these times."

    # Splits the responses into individual sentences
    response1_sentences = nltk.sent_tokenize(response1)
    response2_sentences = nltk.sent_tokenize(response2)

    # Prints the responses
    print("###############################################################################################################")

    # Prints the sentences of the first response
    for sentence in response1_sentences:
        print(sentence)

    print("\n")

    # Prints the sentences of the second response
    for sentence in response2_sentences:
        print(sentence)

    print("###############################################################################################################\n\n")

    # Loads a pre-trained model 
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Encodes the models into vectors
    embeddings1 = model.encode(response1_sentences, convert_to_tensor=True)
    embeddings2 = model.encode(response2_sentences, convert_to_tensor=True)

    # Calculate cosine similarity between the two sentences
    cos_sim = util.pytorch_cos_sim(embeddings1, embeddings2)

    print("###############################################################################################################")

    for i in range(len(response1_sentences)):
        print(f"Similarity score {i}: {cos_sim[i][i].item()}")
        scores.append(cos_sim[i][i].item())

    print("###############################################################################################################\n\n")

    print("###############################################################################################################")

    '''
    For this metric, we take the scores that were recieved before and calculate the average similarity score for the sentences
    Then, we take this average and see if its within the similarity threshold that would constitute that the responses are similar or not
    This seems to be the simpliest way to approach the problem
    '''
    print("Metric 1: Calculate the average similarity")
    
    avg_sim = sum(scores) / len(scores)

    print("The average similarity score is: ", avg_sim)

    if (avg_sim < .8):
        print("Since the score is below 0.8, the responses are not similar")
    else:
        print("Since the score is greater than or equal to 0.8, the responses are similar")

    print("###############################################################################################################\n\n")

