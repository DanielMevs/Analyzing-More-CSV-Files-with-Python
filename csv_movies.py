#Daniel Mevs
import csv


#helper function for get_lists(), tailored to top-rated/top-grossing file columns
def parse_file(f):
    appended_list = []
    file_content = csv.reader(f)
    next(file_content)
    temp_tup = ()
    for row in file_content:
        temp_tup = temp_tup + (int(row[0]), row[1], int(row[2]), float(row[3]),)
        appended_list.append(temp_tup)
        temp_tup = ()
            
    return appended_list

#helper function for get_lists(), tailored to top-cast file columns
def parse_file2(f):
    appended_list = []
    file_content = csv.reader(f)
    next(file_content)
    temp_tup = ()
    for row in file_content:
        temp_tup = tuple(row) 
        #print("\n",temp_tup)
        appended_list.append(temp_tup)
        temp_tup = ()
            
    return appended_list
    
#returns lists based on values of csv files
def get_lists():
    
    rating_list, gross_list, cast_list = [],[],[]
    
    with open('imdb-top-rated.csv', 'r', encoding='utf-8') as rating_file:
        rating_list = parse_file(rating_file)
            
    with open('imdb-top-grossing.csv', 'r', encoding='utf-8') as gross_file:
        gross_list = parse_file(gross_file)
            
    with open('imdb-top-casts.csv', 'r', encoding='utf-8') as cast_file:
        cast_list = parse_file2(cast_file)
        
            
    return rating_list, gross_list, cast_list


def get_dicts(rating_list, gross_list, cast_list):
    rating_dict = {(column[1], column[2]) : (column[0],column[3]) for column in rating_list}
    gross_dict = {(column[1], column[2]) : (column[0], column[3]) for column in gross_list}
    cast_dict = {(column[0], int(column[1])) : (column[2:]) for column in cast_list}
    
    return rating_dict, gross_dict, cast_dict




def director_count(cast_dict, rating_dict):     #rating_dict can apply to top-rated as well as top-grossing dictionaries
    count = {}
    rating_keys = set(rating_dict.keys()) #gets the keys for rating
    for key in rating_keys:
        try:
            name = cast_dict[key][0] #gets the name of the director
        except KeyError:
            continue
        #print(name)
        count[name] = count.get(name, 0) + 1 #second parameter of .get() method specifies the value returned if the value if key is not found.
        #in this way, it counts how many times a director is mentioned by assigning a value and incrimenting 
       # print(count[name])
    return sorted([(number, name) for name, number in count.items()], reverse=True)

def get_actor_dict(cast_dict):
    actor_dict = {} #dictionary with actor as key and movie(s) as value
    for movie, cast in cast_dict.items():
        for actor in cast[1:]:  #starts at [1:] because starting at [0:] would give you directors
            if actor in actor_dict:
                actor_dict[actor].append(movie) #this condition runs if there are already actors in the dictionary and it appends new ones
            else:
                actor_dict[actor] = [movie] #this condtion runs if there are no known actors in the list and it add is to the dictionary

    return actor_dict

def actor_rating_count(actors_dict, rating_dict): #counts the number of times a given actor appears in top-rated movies 
    count = {}
    rating_keys = set(rating_dict.keys()) #gets keys to rating
    for (actor, movies) in actors_dict.items():
        for movie in movies:
            if movie in rating_keys:
                count[actor] = count.get(actor, 0) + 1
    return sorted([(number, name) for name, number in count.items()], reverse=True)



def actor_grossing_count(gross_dict, cast_dict):
    actor_gross = {}
    for movie in gross_dict.keys():
        try:
            gross_amount = gross_dict[movie][1]
        except IndexError:
            continue     
        try:
            actors = cast_dict[movie][1:]
        except KeyError:
            continue
        cast_length = len(actors)
        for i, actor in enumerate(actors):
            actor_gross[actor] = actor_gross.get(actor, 0) + (((2**(cast_length-i))* gross_amount) / 31) #formula to allocate earnings per actor
    return (sorted([(actr, amt) for amt, actr in actor_gross.items()], reverse=True))

def print_directors(directors):
    print('-'*50)
    print('{:<20s} | {:<5s}'.format('Directors', 'Count'))
    print('{:<20s} | {:<5s}'.format('-'*20, '-'*5))
    for i, row in enumerate(directors):
        print('{:<20s} | {:<5d}'.format(row[1], row[0]))
        if i == 5:  #condition that will allow only the top 5 to be printed
            break
    print('\n\n')


def print_actors(actors, value):
    print('-'*50)
    print('{:<20s} | {:<5s}'.format('Actor', value))
    if value == 'Count':
        print('{:<20s} | {:<5s}'.format('-'*20, '-'*20))
    else: #value is 'Amount'
        print('{:<20s} | {:<20s}'.format('-'*20, '-'*20))
    for i, row in enumerate(actors):
        if value == 'Count':
            print('{:<20s} | {:<5d}'.format(row[1], row[0]))
        else:   #value is 'Gross Amount'
            print('{:<20s} | {:<20.2f}'.format(row[1], row[0]))
        if i == 5:  #condition that will allow only the top 5 to be printed
            break
    print('\n\n')


def main():
    rating_list, gross_list, cast_list = get_lists()
    #print(rating_list)
    rating_dict, gross_dict, cast_dict = get_dicts(rating_list, gross_list, cast_list)
    #print(rating_dict)
    #print(cast_dict)
    #print(gross_dict)

    top_rated_director = director_count(cast_dict, rating_dict) #creates a dictionary of top-rated directors
    top_grossing_director = director_count(cast_dict, gross_dict) #creates a dictionary of top-rated directors
    
    
    actor_dict = get_actor_dict(cast_dict) #creates a dictionary of actors
    

    top_rated_actors = actor_rating_count(actor_dict, rating_dict)
    top_grossing_actors = actor_grossing_count(gross_dict, cast_dict)

    #print(top_grossing_actors)
    print('Directors with most movies in top-rated list')
    print_directors(top_rated_director)

    print('Directors with most movies in top-grossing list')
    print_directors(top_grossing_director)

    print('Actors with most movies in top-rated list')
    print_actors(top_rated_actors, 'Count')

    print('Actors with most gross-earnings in top-grossing list')
    print_actors(top_grossing_actors, 'Gross Amount')
    

if __name__ == '__main__':
    main()
