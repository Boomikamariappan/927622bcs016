# mock server 

# from flask import Flask, jsonify
# import random

# app = Flask(_name_)

# def generate_numbers(numberid):
#     if numberid == 'p':  
#         return [2, 3, 5, 7, 11, 13, 17]
#     elif numberid == 'f':  
#         return [0, 1, 1, 2, 3, 5, 8]
#     elif numberid == 'e':  
#         return [2, 4, 6, 8, 10]
#     elif numberid == 'r':  
#         return random.sample(range(1, 100), 5)
#     else:
#         return []

# @app.route("/test/numbers/<numberid>", methods=["GET"])
# def serve_numbers(numberid):
#     nums = generate_numbers(numberid)
#     return jsonify({"numbers": nums})

# if _name_ == "_main_":
#     app.run(port=5001)


from flask import Flask, jsonify
import random
import time

app = Flask(_name_)
last_even_number_generated = 0

all_primes = [
2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
    157, 163, 167, 173, 179, 181, 191, 193, 197, 199
]
last_prime_index_generated = -1
def generate_numbers(numberid):
    global last_even_number_generated, last_prime_index_generated

    if numberid == 'p':
        num_to_generate = 5 
        new_primes = []
        if last_prime_index_generated + num_to_generate < len(all_primes):
            start_index = last_prime_index_generated + 1
            end_index = start_index + num_to_generate
            new_primes = all_primes[start_index:end_index]
            last_prime_index_generated = end_index - 1
        else:

            start_index = last_prime_index_generated + 1
            new_primes = all_primes[start_index:]
            last_prime_index_generated = len(all_primes) - 1

        if not new_primes and last_prime_index_generated == len(all_primes) - 1:
            return []
        return new_primes

elif numberid == 'f':
        return [0, 1, 1, 2, 3, 5, 8]
    elif numberid == 'e':
        num_to_generate = 5
        new_even_numbers = []
        if last_even_number_generated == 0:
            new_even_numbers = [2, 4, 6, 8]
            last_even_number_generated = 8
        else:
            for _ in range(num_to_generate):
                last_even_number_generated += 2
                new_even_numbers.append(last_even_number_generated)
        return new_even_numbers
    elif numberid == 'r':
      
        return random.sample(range(1, 100), 5)
    else:
        return []

@app.route("/test/numbers/<numberid>", methods=["GET"])
def serve_numbers(numberid):
   
    nums = generate_numbers(numberid)
    return jsonify({"numbers": nums})

@app.route("/test/reset_even_numbers", methods=["POST"])
def reset_even_numbers():
    
    global last_even_number_generated
    last_even_number_generated = 0
    return jsonify({"message": "Even number sequence reset successfully!"})

@app.route("/test/reset_prime_numbers", methods=["POST"])
def reset_prime_numbers():
    
    global last_prime_index_generated
    last_prime_index_generated = -1
    return jsonify({"message": "Prime number sequence reset successfully!"})


if _name_ == "_main_":
    app.run(port=5001, debug=True)
