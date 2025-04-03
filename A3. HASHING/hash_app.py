import xxhash
import os
import sys

def get_bucket_filename(base_name, overflow_index):
    """Generate a bucket file name with overflow handling."""
    return f"{base_name}_overflow_{overflow_index}.txt" if overflow_index > 0 else f"{base_name}.txt"

def find_last_overflow_file(base_name):
    """Find the last overflow file for a given base name."""
    overflow_index = 0
    while os.path.exists(get_bucket_filename(base_name, overflow_index)):
        overflow_index += 1
    return get_bucket_filename(base_name, overflow_index - 1 if overflow_index > 0 else 0)

def write_to_bucket(bucket_num, text, max_size):
    """Write the given text to the correct bucket file, handling overflow."""
    base_name = str(bucket_num)
    filename = find_last_overflow_file(base_name)
    
    while True:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                current_size = len(f.read())
        else:
            current_size = 0
        
        if current_size + len(text) > max_size:
            overflow_index = int(filename.split("_overflow_")[-1].split(".")[0]) + 1 if "_overflow_" in filename else 1
            filename = get_bucket_filename(base_name, overflow_index)
        else:
            break
    
    with open(filename, "a") as f:
        f.write(text + "\n")
    print(f"{text} added to {os.path.basename(filename)}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python hash_app.py <n> <s>")
        sys.exit(1)
    
    n = int(sys.argv[1])
    s = int(sys.argv[2])
    
    try:
        while True:
            try:
                text = input("Please enter the string: ").strip()
                if not text:
                    continue
                
                if len(text) > s:
                    print(f"Error: Input length ({len(text)}) exceeds max bucket size ({s}). Moving to an overflow file.")
                    hash_value = xxhash.xxh32(text).intdigest()
                    bucket_num = (hash_value % n) + 1
                    filename = get_bucket_filename(str(bucket_num), 1)
                    with open(filename, "a") as f:
                        f.write(text + "\n")
                    print(f"{text} added to {filename}")
                    continue
                
                hash_value = xxhash.xxh32(text).intdigest()
                bucket_num = (hash_value % n) + 1  # Buckets are 1-indexed
                write_to_bucket(bucket_num, text, s)
            except Exception as e:
                print(f"An error occurred: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()
