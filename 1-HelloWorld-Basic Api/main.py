
#  1-HelloWorld-Basic Api
from fastapi import FastAPI
from pydantic import constr
app= FastAPI()


#EP1
@app.get("/")
def home_route():
    return {"message_key1":"Welcome to home page"}

#EP2
@app.get("/home2") #static route
def home_route():
    return {"Welcome to home page2"}

#EP3
@app.get("/cats/{breed}") #path params used in route
def cats(breed :str):
    return {f"This cat is of breed {breed}"}

#EP4
@app.get("/kittens/{breed_type}") #now query params added
def cats(breed_type :str, color :str="orange", age: int|None = None):
    return {f"This cat is of breed {breed_type} and color {color}. \n It's age is {age}."}

'''
In ep4 above, if in url user passed color=7 still it would not raise error as json validation would convert
int 7 to string 7 and 7 would still be accepted as str only. But if say we had constraint for int and user 
passes abc then error would be raised cause while the prev conversion is possible 7-> "7", "abc" to int 
is not possible.

But if you want to handle 7->"7" more strictly and not allow it then you can do 3 ways:
1. Use enum [most professional]: make an enum class of all possible values and use it.

2. use Regex constraint  in the line:- color: constr(regex="^[A-Za-z]+$") & add from pydantic import constr



in new pydantic version regex keyword is updated by "pattern" - SUPPPPPER IMP

means that only letters are allowed in color.
3. Manually put condition inside function before returning result: eg: if condition etc...

eg:shown in ep 5,6,7
'''

#EP5
#Regex handling for author name - cna be done for path param and query param both
@app.get("/route5/{book_name}/{author}")
def fn5 (book_name: str, author: constr(pattern="^[A-Za-z]+$"), page: int=1):
    return{"Book Name: ": book_name,
           "Author: ": author,
           "page: ": page
           }


'''
To remove the yellow line warning (it is not error) from regex, add this line above the roots decorator 
and then use the alias varible in func definition

author_type= constr(pattern="^[A-Za-z]+$")

@app.get...etc route5

def fn5 (book_name: str, author: author_type, page: int=1):
    return{"Book Name: ": book_name,
           "Author: ": author,
           "page: ": page
           }

'''

'''
If you want any param to be optional - make it query param
if want it to be required field, make it path param
Regex applicable for both'''