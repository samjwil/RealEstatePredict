import trulia.stats
import trulia.location


TRULIA_KEY = 'uacak7su5m4snvwvvqbqmbrf'

# # Get all cities in California
# cities = trulia.location.LocationInfo(TRULIA_KEY).get_cities_in_state('CA')
#
# # Get all counties in California
# counties = trulia.location.LocationInfo(TRULIA_KEY).get_counties_in_state('CA')
# print counties
#
# # Get all neighborhoods in Los Angeles
# neighborhoods = trulia.location.LocationInfo(TRULIA_KEY).get_neighborhoods_in_city('Los Angeles', 'CA')
# print neighborhoods
# # Get all states in the United States
# states = trulia.location.LocationInfo(TRULIA_KEY).get_states()
# print states
#
# # Get all zip codes in California
# zip_codes = trulia.location.LocationInfo(TRULIA_KEY).get_zip_codes_in_state('CA')
# print zip_codes
#
# # Get all traffic and listing stats for the city of Los Angeles in January 2014
# city_stats = trulia.stats.TruliaStats(TRULIA_KEY).get_city_stats(city='Los Angeles', state='CA', start_date='2014-01-01', end_date='2014-01-31')
# print city_stats
#
# # Get all traffic and listing stats for Santa Clara county in January 2014
# county_stats = trulia.stats.TruliaStats(TRULIA_KEY).get_county_stats(county='Santa Clara', state='CA', start_date='2014-01-01', end_date='2014-01-31')
# print county_stats
#
# # Get all traffic and listing stats for Venice, CA neighborhood in January 2014
# neighborhood_stats = trulia.stats.TruliaStats(TRULIA_KEY).get_neighborhood_stats(neighborhood_id=7183, start_date='2014-01-01', end_date='2014-01-31')
# print neighborhood_stats
#
# # Get all traffic and listing stats for California in January 2014
# state_stats = trulia.stats.TruliaStats(TRULIA_KEY).get_state_stats(state='CA', start_date='2014-01-01', end_date='2014-01-31')
# print state_stats

# Get all traffic and listing stats for the 90025 zip code in January 2014
zip_code_stats = trulia.stats.TruliaStats(TRULIA_KEY).get_zip_code_stats(zip_code='90025', start_date='2001-01-01', end_date='2014-01-31')
print zip_code_stats
