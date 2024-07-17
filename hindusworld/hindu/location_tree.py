from .models import village,block,District,State,Country,Continent

# def get_location_hierarchy():
#     hierarchy_map = {}

#     query_set = Continent.objects.all()


#     for continent in query_set:
#         continent_id = str(continent._id)
#         continent_list = hierarchy_map.setdefault(continent_id, [continent_id])

#         # Fetch states related to the current country
#         country = Country.objects.filter(continent_id=continent._id)

#     for country in query_set:
#         country_id = str(country._id)
#         country_list = hierarchy_map.setdefault(country_id, [country_id])
#         continent_list.append(country_id)

#         # Fetch states related to the current country
#         states = State.objects.filter(country_id=country._id)

#         for state in states:
#             state_id = str(state._id)
#             state_list = hierarchy_map.setdefault(state_id, [state_id])
#             country_list.append(state_id)

#             # Fetch districts related to the current state
#             districts = District.objects.filter(state_id=state._id)

#             for district in districts:
#                 district_id = str(district._id)
#                 district_list = hierarchy_map.setdefault(district_id, [district_id])
#                 country_list.append(district_id)
#                 state_list.append(district_id)

#                 # Fetch blocks related to the current district
#                 blocks = Block.objects.filter(district_id=district._id)

#                 for block in blocks:
#                     block_id = str(block._id)
#                     block_list = hierarchy_map.setdefault(block_id, [block_id])
#                     country_list.append(block_id)
#                     state_list.append(block_id)
#                     district_list.append(block_id)

#                     # Fetch villages related to the current block
#                     villages = Village.objects.filter(block_id=block._id)

#                     for village in villages:
#                         village_id = str(village._id)
#                         hierarchy_map[village_id] = [village_id]
#                         country_list.append(village_id)
#                         continent_list.append(village_id)
#                         state_list.append(village_id)
#                         district_list.append(village_id)
#                         block_list.append(village_id)

#                     hierarchy_map[block_id] = block_list

#                 hierarchy_map[district_id] = district_list
#             hierarchy_map[state_id] = state_list
#         hierarchy_map[country_id] = country_list
#         hierarchy_map[continent_id] = continent_id

#     return hierarchy_map



def get_location_hierarchy():
    hierarchy_map = {}

    # Fetch all continents
    continents = Continent.objects.all()

    for continent in continents:
        continent_id = str(continent._id)
        continent_list = hierarchy_map.setdefault(continent_id, [continent_id])

        # Fetch countries related to the current continent
        countries = Country.objects.filter(continent=continent)

        for country in countries:
            country_id = str(country._id)
            country_list = hierarchy_map.setdefault(country_id, [country_id])
            continent_list.append(country_id)

            # Fetch states related to the current country
            states = State.objects.filter(country=country)

            for state in states:
                state_id = str(state._id)
                state_list = hierarchy_map.setdefault(state_id, [state_id])
                country_list.append(state_id)

                # Fetch districts related to the current state
                districts = District.objects.filter(state=state)

                for district in districts:
                    district_id = str(district._id)
                    district_list = hierarchy_map.setdefault(district_id, [district_id])
                    state_list.append(district_id)

                    # Fetch blocks related to the current district
                    blocks = block.objects.filter(district=district)

                    for block in blocks:
                        block_id = str(block._id)
                        block_list = hierarchy_map.setdefault(block_id, [block_id])
                        district_list.append(block_id)

                        # Fetch villages related to the current block
                        villages = village.objects.filter(block=block)

                        for village in villages:
                            village_id = str(village._id)
                            hierarchy_map[village_id] = [village_id]
                            block_list.append(village_id)

                        hierarchy_map[block_id] = block_list

                    hierarchy_map[district_id] = district_list

                hierarchy_map[state_id] = state_list

            hierarchy_map[country_id] = country_list

        hierarchy_map[continent_id] = continent_list

    return hierarchy_map