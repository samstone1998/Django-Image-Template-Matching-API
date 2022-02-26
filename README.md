# Django Image Template Matching API
 A simple Django rest api that takes 2 images and an option threshold and returns true or false depending on if the template image is matched in the base image.  Due to the method of template matching being used the template image size does not matter as it gets resized in the matching search.

## Features
- Throttling to 10 requests a minute
- Database logging to catch unexpected issues
- Matches template no matter what the image size is

## How to use
#### Example Curl From Postman
```
curl --location --request POST 'http://localhost:8000/api/match' \
--form 'base=@"super_mario.jpeg"' \
--form 'template=@"SuperMarioCoin.jpeg"' \
--form 'threshold="0.6"'
```
#### Body Data
- base -> Image file that you want to check the template in
- template -> Image you want to be found in the base
- threshold (optional) -> The minimum threshold the match must be equal to, default is 0.8.

