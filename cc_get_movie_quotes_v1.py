import csv

file = open("movie_quotes.csv", "r")
all_movie = list(csv.reader(file, delimiter=","))
file.close()

# remove the first row (header values)
all_movie.pop(0)

# get the first 50 rows (used to develop colour
# buttons for play GUI)
print(all_movie[:50])

print("Length: {}".format(len(all_movie)))
