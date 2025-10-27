import os
#Helper functions to add to flask app
#Can use them when manipulating db

def load_blog(user):
    path = f"Data/{user}"
    if os.path.exists(path) and os.path.isdir(path):
        text = ""
        for file in os.listdir(path):
            x = open(f"{path}/{file}")
            text+= x.read() + "\n\n"
        return text
    else:
        return None
    
def create_blog(txt, user):
    path = f"Data/{user}"
    if os.path.exists(path) and os.path.isdir(path):
        with open(f"{path}/{len(os.listdir(path))}.txt", "w") as file:
            file.write(txt)
    else:
        os.mkdir(path)
        with open(f"{path}/0.txt", "w") as file:
            file.write(txt)        

def get_entry(user, id):
    path = f"Data/{user}/{id}.txt"
    if os.path.exists(path):
        x = open(path)
        return x.read()
    else:
        return None
    
def edit_blog(txt, user, id):
    path = f"Data/{user}"
    if os.path.exists(path) and os.path.isdir(path):
        with open(f"{path}/{id}.txt", "w") as file:
            file.write(txt)
    else:
        return None

create_blog("skbidi", "Andrew Tsai")
print(load_blog("Andrew Tsai"))