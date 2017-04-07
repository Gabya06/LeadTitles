import os
import pandas as pd
import numpy as np
import itertools
import re
import string
import beatbox

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

delims = ",", ".", "/", "&", "-", ' '
regexPattern = '|'.join(map(re.escape, delims))

# set directory and project path
os.chdir("/Users/Gabi/Documents/dev/titles/")
project_dir = '/Users/Gabi/Documents/dev/titles/'
data_dir = project_dir + 'data/input/'


outdir = '/Users/Gabi/Documents/dev/titles/data/processed/'



# title_file: SFDC titles for all lead sources - as of 8/08/2016
# scoring_file: scoring matrix
#title_file = '08082016_All_Lead_from_Salesforce.xlsx'
# title_file = 'CA_Leads_08252016.xlsx'
# title_file  = 'All_Leads_for_Scoring_26Aug16.xlsx'

# title_file = 'EloquaExport_09012016.xlsx'
title_file = 'campaign_titles.xlsx'
#title_file ='pwc_gdpr_bigdata.xlsx'
scoring_file = 'title_scoring.xlsx'



