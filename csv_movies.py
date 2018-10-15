#Daniel Mevs
import csv

#returns a list of top rated films
def get_rating_list(rating_list):
    
    with open('imdb-top-rated.csv', 'r', encoding='utf-8') as rating_file:
        file_content = csv.reader(rating_file)
        next(file_content)
        temp_tup = ()
        
        for row in file_content:
            temp_tup = temp_tup + (int(row[0]), row[1], int(row[2]), float(row[3]),)
            rating_list.append(temp_tup)
            temp_tup = ()

    return rating_list

#returns a list of top grossing films
def get_gross_list(gross_list):  
    with open('imdb-top-grossing.csv', 'r', encoding='utf-8') as gross_file:
        file_content = csv.reader(gross_file)
        next(file_content)
        temp_tup = ()

        for row in file_content:
            temp_tup = temp_tup + (int(row[0]), row[1], int(row[2]), float(row[3]),)
            gross_list.append(temp_tup)
            temp_tup = ()

    return gross_list

#returns a list of cast members
def get_cast_list(cast_list):          
    with open('imdb-top-casts.csv', 'r', encoding='utf-8') as cast_file:
        file_content = csv.reader(cast_file)
        next(file_content)
        temp_tup = ()
        for row in file_content:
            temp_tup = tuple(row) 
            #print("\n",temp_tup)
            cast_list.append(temp_tup)
            temp_tup = ()
                
    return cast_list

#returns a dictionary of top rated films
def get_rating_dict(rating_list):
    rating_dict = {}
    rating_dict = {(column[1], column[2]) : (column[0],column[3]) for column in rating_list}
    return rating_dict

#returns a dictionary of top grossing films
def get_gross_dict(gross_list):
    gross_dict = {(column[1], column[2]) : (column[0], column[3]) for column in gross_list}
    return gross_dict

#returns a dictionary of a cast
def get_cast_dict(cast_list):
    
    cast_dict = {(column[0], int(column[1])) : (column[2:]) for column in cast_list}
    return cast_dict


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
    temp_list = []
    for name, number in count.items():
        temp_list.append((number, name))
    director_list = sorted(temp_list, reverse=True)
    print(director_list)
    return director_list

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
    temp_list = []
    for name, number in count.items():
        temp_list.append((number, name))
        #print(temp_list)
    actor_rating_list = sorted(temp_list, reverse=True)

    return actor_rating_list



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
    temp_list = []
    
    for amt, actr in actor_gross.items():
        temp_list.append((actr, amt))
            
    actor_grossing_list = sorted(temp_list, reverse=True)

    return actor_grossing_list
    

def print_director_rating(directors):
    print('Directors with most movies in top-rated list')
    top_border = '-'*50
    print(top_border)
    print('{:<20s} | {:<5s}'.format('Directors', 'Count'))
    print('{:<20s} | {:<5s}'.format('-'*20, '-'*5))
    for i, row in enumerate(directors):
        print(i+1, ' ', '{:<20s} | {:<5d}'.format(row[1], row[0]))
        if i == 5:  #condition that will allow only the top 5 to be printed
            break
    print('\n\n')

def print_director_grossing(directors):
    print('Directors with most movies in top-grossing list')
    top_border = '-'*50
    print(top_border)
    print('{:<20s} | {:<5s}'.format('Directors', 'Count'))
    print('{:<20s} | {:<5s}'.format('-'*20, '-'*5))
    for i, row in enumerate(directors):
        print(i+1, ' ', '{:<20s} | {:<5d}'.format(row[1], row[0]))
        if i == 5:  #condition that will allow only the top 5 to be printed
            break
    print('\n\n')

def print_actor_grossings(actors):

    print('Actors with most gross-earnings in top-grossing list')
    top_border = '-'*50
    title_border = '-'*20
    print(top_border)

    print('{:<20s} | {:<5s}'.format('Actor', 'Amount Grossed'))
    print('{:<20s} | {:<20s}'.format(title_border, title_border))
    
    for i, row in enumerate(actors):
        print(i+1, ' ', '{:<20s} | {:<20.2f}'.format(row[1], row[0]))
        if i == 5:  #condition that will allow only the top 5 to be printed
            break

    print('\n\n')

def print_actor_rating(actors):
    print('Actors with most movies in top-rated list')
    top_border = '-'*50
    title_border = '-'*20
    print(top_border)

    print('{:<20s} | {:<5s}'.format('Actor', 'Appearances in top-rated'))
    print('{:<20s} | {:<5s}'.format(title_border, title_border))

    for i, row in enumerate(actors):
        print(i+1, ' ', '{:<20s} | {:<5d}'.format(row[1], row[0]))
        if i == 5:  #condition that will allow only the top 5 to be printed
            break

    print('\n\n')
           

def main():
    
    rating_list = []
    rating_list = get_rating_list(rating_list)
    #print(rating_list)
    gross_list = []
    gross_list = get_gross_list(gross_list)
    #print(gross_list)
    cast_list = []
    cast_list = get_cast_list(cast_list)
    #print(cast_list)
    rating_dict = get_rating_dict(rating_list)
    print(rating_dict)
    gross_dict = get_gross_dict(gross_list) 
    #print(gross_dict)
    cast_dict = get_cast_dict(cast_list)
    #print(cast_dict)
    

    top_rated_director = director_count(cast_dict, rating_dict) #creates a dictionary of top-rated directors
    top_grossing_director = director_count(cast_dict, gross_dict) #creates a dictionary of top-rated directors
    
    
    actor_dict = get_actor_dict(cast_dict) #creates a dictionary of actors
    

    top_rated_actors = actor_rating_count(actor_dict, rating_dict)
    top_grossing_actors = actor_grossing_count(gross_dict, cast_dict)

    #print(top_rated_actors)
    print_director_rating(top_rated_director)
    
    print_director_grossing(top_grossing_director)
    
    print_actor_rating(top_rated_actors)
    
    print_actor_grossings(top_grossing_actors)


if __name__ == '__main__':
    main()
