[![GitHub license](https://img.shields.io/github/license/WesleyKambale/Ug-Universities-Api)](https://github.com/WesleyKambale/Ug-Universities-Api/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/WesleyKambale/Ug-Universities-Api)](https://github.com/WesleyKambale/Ug-Universities-Api/issues)
[![GitHub watchers](https://img.shields.io/github/watchers/WesleyKambale/Ug-Universities-Api)](https://github.com/WesleyKambale/Ug-Universities-Api/watchers)
[![GitHub forks](https://img.shields.io/github/forks/WesleyKambale/Ug-Universities-Api)](https://github.com/WesleyKambale/Ug-Universities-Api/network/)
[![GitHub stars](https://img.shields.io/github/stars/WesleyKambale/Ug-Universities-Api)](https://github.com/WesleyKambale/Ug-Universities-Api/stargazers)
[![Tweet](https://img.shields.io/twitter/url?url=https%3A%2F%2Fgithub.com%2FWesleyKambale%2FUg-Universities-Api)](https://twitter.com)


# Uganda University Domain List

Uganda University Domain List is a JSON API that contains domain names, university names of most of the universities in Uganda.

The list includes;
- Private Universities
- Public Universities
- Ugandan Military Universities

JSON file attached acts as a data source which can work with any programming language.


## Usage
- Clone Project: git clone https://github.com/WesleyKambale/ug-universities-api.git
- Setup and activate your virtual environment
- Install requirements pip install -r requirements.txt
- Run server


## Using the JSON File

This is located in the uganda-universities-domians.json file. It is just a list of dictionaries in the following format:
```
[
	...
	{
		"domains": [
			"must.ac.ug"
			], 
		"web_pages": [
			"http://www.must.ac.ug/"
			], 
		"name": "Mbarara University of Science and Technology",
		"abbrev": "MUST",
		"location": "Mbarara", 
		"alpha_two_code": "UG",
		"alpha_three_code": "UGA",  
		"country": "Uganda"
	}, 
	...
]
```
## Filter through the Universities

If you want a particular university, run

```bash
filters.py $name1 [Optional: $name2]
```

from the root directory to return

```
filtered-uganda-universities-domains.json
```
## Contributing
Pull requests are welcome. Do not hesitate to fix any wrong data. But please open an issue first to discuss what you would like to change.

## License
[MIT License](https://github.com/WesleyKambale/Ug-Universities-Api/blob/main/LICENSE)

## Creation & Inspiration
Created by [Wesley Kambale](https://kambale.dev)

Inspiration from [Hipo](https://github.com/Hipo/university-domains-list)
