[![GitHub license](https://img.shields.io/github/license/WesleyKambale/Ug-Universities-Api)](https://github.com/WesleyKambale/Ug-Universities-Api/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/WesleyKambale/Ug-Universities-Api)](https://github.com/WesleyKambale/Ug-Universities-Api/issues)
[![GitHub watchers](https://img.shields.io/github/watchers/WesleyKambale/Ug-Universities-Api)](https://github.com/WesleyKambale/Ug-Universities-Api/watchers)
[![GitHub forks](https://img.shields.io/github/forks/WesleyKambale/Ug-Universities-Api)](https://github.com/WesleyKambale/Ug-Universities-Api/network/)
[![GitHub stars](https://img.shields.io/github/stars/WesleyKambale/Ug-Universities-Api)](https://github.com/WesleyKambale/Ug-Universities-Api/stargazers)
[![Tweet](https://img.shields.io/twitter/url?url=https%3A%2F%2Fgithub.com%2FWesleyKambale%2FUg-Universities-Api)](https://twitter.com)


# Uganda Universities List

Uganda Universities List shows Universities in Uganda. It uses [OpenStreetMaps](https://openstreetmap.org/) to show the different universities on a map of Uganda. It includes a JSON API that contains domain names, university names of most of the universities in Uganda.

The list includes;
- Private Universities
- Public Universities
- Ugandan Military Universities

JSON file attached acts as a data source which can work with any programming language.

## Demo

Here is the demo link: [http://ug-universities.herokuapp.com](http://ug-universities.herokuapp.com)

## Using the JSON File

This is located in the uganda-universities-domains.json file. It is just a list of dictionaries in the following format:
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

## Contributing
Pull requests are welcome. Do not hesitate to fix any wrong data. But please open an issue first to discuss what you would like to change.

- Check out [CONTRIBUTING.md](CONTRIBUTING.md) for information about getting involved.

## License
[MIT License](https://github.com/WesleyKambale/Ug-Universities-Api/blob/main/LICENSE)

## Creation & Inspiration
Created by [Wesley Kambale](https://kambale.hashnode.dev)
