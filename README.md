# Kazdream 
Technical interview for Kazdream

## Getting ready.

First, clone this repository to your local machine:

```bash
git clone https://github.com/TheRadioDept/shop-parser.git
```
Then navigate into cloned repository:
```bash
cd kazdream
```

To install all the requirements - execute:
```bash
pip install -r requirements.txt
```

## Running the project.

1. First, you need to run `sqliteConn.py` in order to create/connect to SQLite Databae and create rabbitMQ channel to store data into the database.
2. Second, navigate to `spiders` directory, and execute the following command:
```bash
scrapy runspider web_parses.py
```
After you've completed these steps, `sqliteConn.py` will start storing all the data parsed from [Shop.kz](https://shop.kz/) into our created database.


## Loading all parsed items into a .Json file.

You can store all parsed items into .Json file. Follow steps bellow to do so:

1. Navigate into ``spiders`` directory.
2. Execute the following command to parse all categorised items from [Shop.kz](https://shop.kz/) into .JSON file:

```bash
scrapy runspider web_parses.py -o categories.json
```



