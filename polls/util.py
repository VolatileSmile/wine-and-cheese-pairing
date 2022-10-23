import string, random

def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))