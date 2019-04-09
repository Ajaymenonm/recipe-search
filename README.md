# Recipe-Search
A python executable to search for tasty recipes with the ingredients you have

### Installation

1. Install python. <br /> https://docs.python.org/3/using/index.html

2. Download Recipe-Search code. <br />
  `$ https://github.com/Ajaymenonm/recipe-search.git` <br />
  `$ cd recipe-search`

3. Install dependency packages <br />
  `$ pip install -r requirements.txt`

4. Create an account on food2fork <br />
   https://www.food2fork.com/about/api <br /> Copy the API KEY

5. Set environment variables ****(Either of two)****
    * Load from Secrets file <br /> Paste the above copied API key to `secrets.yml`

    * Load from Bash <br /> 
    ** Open .bashrc file using vi editor in insert mode. `vi ~/.bashrc`<br />
    ** Add `export KEY=xxxxxxxxxxxx`<br />
    ** Source the file. `source ~/.bashrc`

6. Project Setup Done!

---------------------------

### End User

1. Open Terminal / Console <br />

2. Run the python executable with the below command <br />
  `$ python3 recipe.py` 
  
3. Options: <br />
![alt text](https://s3.amazonaws.com/recipe-search/recipe_ing.png) <br /><br />
** Enter Ingredients one at a time <br />
** Enter `1` to exit the application

4. Search for recipe: <br />
![alt text](https://s3.amazonaws.com/recipe-search/search_rec.png) <br /><br />
** Enter `2` to search recipe

5. Get most popular recipe and missing ingredients <br />
![alt text](https://s3.amazonaws.com/recipe-search/recipe.png) <br /><br />

6. Enter `ctrl + c` to exit program <br />

