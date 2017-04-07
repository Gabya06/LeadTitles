from functions import *

# read title matrix
title_matrix = load_xl(root_dir = data_dir, file_name = scoring_file, sheetname = 'title_matrix')
# list of target titles
target_titles = title_matrix.title.tolist()
# dictionary lookup
d = title_matrix.set_index('title').to_dict('s')

# load spell check mapping
mapping_df = load_xl(root_dir = data_dir, file_name = scoring_file, sheetname = 'mapping')
mapping = mapping_df.set_index('old').to_dict('s')

# load actual:sfdc mapping
level_mapping_df = load_xl(root_dir = data_dir, file_name = scoring_file, sheetname = 'level_mapping')
# list of all levels 
levels = level_mapping_df.Actual.tolist()
level_mapping = level_mapping_df.set_index('Actual').to_dict()

# load keywords:points mapping
keyword_df = load_xl(root_dir = data_dir, file_name = scoring_file, sheetname = 'keywords')
keywords = keyword_df.keyword.tolist()
keyword_mapping = keyword_df.set_index('keyword').to_dict()

# load joblevel:points mapping --> for no matches
not_match_df = load_xl(root_dir = data_dir, file_name = scoring_file, sheetname = 'no_match_levels')
not_match_levels = not_match_df.set_index('job_level').to_dict()

# lists of levels, keywords
levels = sorted(levels, key = len, reverse = True)
keywords = sorted(keywords, key = len, reverse = True)
levels_ordered = not_match_df.sort_values('points', ascending = False).job_level.tolist()

# params for title mapping and score
title_mapping_args = dict(target_title_list = target_titles, level_mapping_dict = level_mapping, points_dict = d,
                          keyword_mapping_dict = keyword_mapping, levels_ranked = levels_ordered, keyword_list = keywords,
                          levels_not_match = not_match_levels)

# load & clean dataframe
df = load_xl(root_dir = data_dir, file_name = title_file, sheetname = 'SF_LEADS')
df = clean_data(dat = df, mapping_dict = mapping)

df.reset_index(inplace = True)
df.drop('index', axis = 1, inplace = True)

# run get_title_points for each row in title_split
# parse out results in 3 columns
df['temp'] = df.title_split.map(lambda x: get_title_points(title = x, level_list = levels, **title_mapping_args))
df['temp_level'] = df.temp.map(lambda x: x[0])
df['temp_title'] = df.temp.map(lambda x: x[1])
df['temp_score'] = df.temp.map(lambda x: x[2])

print "finished running... Here are the most frequent titles \n", df.temp_title.value_counts().head()
# df.to_csv('/Users/Gabi/Documents/dev/titles/data/processed/Eloqua_scores_results_09012016.csv', encoding ='utf-8')
df.to_csv('/Users/Gabi/Documents/dev/titles/data/processed/campaign_titles_processed.csv', encoding ='utf-8')

