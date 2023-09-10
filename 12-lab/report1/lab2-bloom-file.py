from pybloom_live import BloomFilter

# Create sets for two participants
alice_set = set([1, 2, 3, 4, 5])
bob_set = set([3, 4, 5, 6, 7])

print("alice_set", alice_set)
print("bob_set", bob_set)

# Create a Bloom Filter and add Alice's set elements
bloom_filter = BloomFilter(capacity=1000, error_rate=0.001)
for item in alice_set:
    bloom_filter.add(item)

# Initialize the intersection set
intersection = set()

# Check if Bob's elements exist in the Bloom Filter
for item in bob_set:
    if item in bloom_filter:
        intersection.add(item)

print("Intersection: ", intersection)
