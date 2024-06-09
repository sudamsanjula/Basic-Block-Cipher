# Sudam Sanjula 
# Block cipher

#Function for left-shifting characters in a block by 1
def block_permutation(block):
    # Perform a left shift by 1 on the characters in the block
    permuted_block = block[1:] + [block[0]]
    return permuted_block

#Function for left-shifting ASCII values in a block by 1
def left_shift_permutation(block):
    # Perform left shift permutation by 1 on ASCII values of the block
    shifted_block = [(val * 2) % 256 for val in block]
    return shifted_block

#Function for adding key values to block values
def key_addition(block, key_block):
    # Add key value to the block values
    result_block = [(val + key_block[i % len(key_block)]) % 256 for i, val in enumerate(block)]
    return result_block

#Function for encrypting a block using block permutation and key addition
def encrypt_block(plaintext_block, key_block):
    # Block Permutation (Left Shift by 1)
    permuted_block = block_permutation(plaintext_block)
    
    # Key Addition
    result_block = key_addition(permuted_block, key_block)
    
    return result_block

# Define a function for decrypting a block using reverse key addition and reverse block permutation
def decrypt_block(ciphertext_block, key_block):
    # Reverse Key Addition
    result_block = [(val - key_block[i % len(key_block)]) % 256 for i, val in enumerate(ciphertext_block)]
    
    # Reverse Block Permutation (Right Shift by 1)
    original_block = [result_block[-1]] + result_block[:-1]
    
    return original_block

# Define a function for encrypting a plaintext using block encryption and multiple rounds
def encrypt(plaintext, key, rounds=5):
    block_size = 8
    key_block = [ord(char) for char in key]

# Initialize ciphertext with plaintext
    ciphertext = plaintext

# Perform encryption for the specified number of rounds
    for _ in range(rounds):
        encrypted_text = ''
        previous_block = [0] * block_size

# Process blocks of plaintext
        for i in range(0, len(ciphertext), block_size):
            block = ciphertext[i:i+block_size]

            # Convert block characters to ASCII values
            block = [ord(char) for char in block]

            # Pad the block if its size is less than block_size
            block += [0] * (block_size - len(block))

            # CBC: XOR with the previous block
            block = [block[j] ^ previous_block[j] for j in range(block_size)]

            # Encrypt the block
            result_block = encrypt_block(block, key_block)

            # Save the result block for the next iteration
            previous_block = result_block.copy()

            # Convert ASCII values back to characters
            encrypted_block = ''.join(chr(val) for val in result_block)
            encrypted_text += encrypted_block

# Update ciphertext for the next round
        ciphertext = encrypted_text

    return ciphertext

# Define a function for decrypting a ciphertext using block decryption and multiple rounds
def decrypt(ciphertext, key, rounds=5):
    block_size = 8
    key_block = [ord(char) for char in key]

# Initialize decrypted text with ciphertext
    decrypted_text = ciphertext

# Perform decryption for the specified number of rounds
    for _ in range(rounds):
        decrypted_text_round = ''
        previous_block = [0] * block_size

# Process blocks of ciphertext
        for i in range(0, len(decrypted_text), block_size):
            block = decrypted_text[i:i+block_size]

            # Convert block characters to ASCII values
            block = [ord(char) for char in block]

            # Pad the block if its size is less than block_size
            block += [0] * (block_size - len(block))

            # Decrypt the block
            result_block = decrypt_block(block, key_block)

            # XOR with the previous block
            result_block = [result_block[j] ^ previous_block[j] for j in range(block_size)]

            # Save the result block for the next iteration
            previous_block = block.copy()

            # Convert ASCII values back to characters
            decrypted_block = ''.join(chr(val) for val in result_block)
            decrypted_text_round += decrypted_block

        decrypted_text = decrypted_text_round

    return decrypted_text

while True:
    # Ask the user what operation to perform
    operation = input("Do you want to encrypt or decrypt? (e/d): ")

    # Depending on the user's choice, perform encryption or decryption
    if operation.lower() == 'e':
        plaintext = input("Enter the plaintext: ")
        key = input("Enter the key: ")
        encrypted_text = encrypt(plaintext, key)
        print("Encrypted text:", encrypted_text)
    elif operation.lower() == 'd':
        ciphertext = input("Enter the encrypted text: ")
        key = input("Enter the key: ")
        decrypted_text = decrypt(ciphertext, key)
        print("Decrypted text:", decrypted_text)
    else:
        print("Invalid choice. Please enter 'e' for encrypt or 'd' for decrypt.")
        continue

    # Ask the user if they want to perform more operations
    more_choice = input("Do you want to do more? (y/n): ")
    if more_choice.lower() != 'y':
        break
