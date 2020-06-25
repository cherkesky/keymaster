airbnb = {
"listing_description": ['listing_uid'], #ex "townhome_nyc": '1937753458',
"listing_description": ['listing_uid'] #ex "my_home" :'1937753459',
}

airbnbAll = f'&listings[]={airbnb["listing_description"]}&listings[]={airbnb["listing_description"]}' 

vrbo = {
"listing_description": ['listing_uid'], #ex "townhome_nyc": '1937753458',
"listing_description": ['listing_uid'] #ex "my_home" :'1937753459',
}

vrboAll = f'&listings[]={vrbo["listing_description"]}&listings[]={vrbo["listing_description"]}'