import beatbox
from loadvar import *

# PROD
# sf_user = 'gabrielle.agrocostea@collibra.com'
# sf_token = '6RB94QStbxUGLIsxG8yfJvZj'

'''
script to login to either Sandbox SF or Prod using beatbox and query CONTACT table,
find CONTACT w.o a score
update the score in SF based on cleaned title and add Matching title
'''


# Assume column with score salesops_leadscore --> if it s empty look up score
# select data where title_score_c is null
# s = "SELECT Lead.Title from Lead WHERE Lead.Id =" +"'00Q2000000o9ISwEAM'"
s = "SELECT Id, Title, Title_Score__c from Contact where Contact.Title_Score__c = NULL AND Contact.Title != NULL"
svc = login_beatbox()

#qr = svc.query(s)
qr = query_data_bb(svc, s)

# update one record at a time:
contact_id_err = []
status_code_err = []
qr_updates = []
for rec in qr:
    contact_id = rec['Id']
    original_title = rec['Title']
    title = clean_title(title_string=rec['Title'],
                        mapping_dict=mapping)  ## need to make sure to clean title string
    score = rec['Title_Score__c']
    #temp = get_title_points(title=title, level_list= levels, **title_mapping_args)
    # if score:
    temp = get_title_points(title=title, level_list= levels, **title_mapping_args)
    new_title = temp[1]
    try:
        new_title = new_title.title() # make upper case 1st letters
    except:
        if np.isnan(new_title):
            new_title = ''
        else:
            pass
    score = temp[2]
    # don't allow negative scores
    if score <0:
        score = 0
    score = str(score)
    print "updating", contact_id, new_title," Score:", score
    # rec_update = {'Id': lead_id, 'Title': title, 'Title_Score__c': score, 'type': 'Lead', 'Job_Title_Match__c':new_title}
    rec_update = {'Id': contact_id, 'Title': original_title, 'Title_Score__c': score, 'type': 'Contact',
                  'Job_Title_Match__c': new_title}
    qr_updates.append(rec_update)
    # update one record:
    sr = svc.update(rec_update)
    if sr[0]['success'] == True:
        print "Success updating id " + sr[0]['id'] + " " + title + " " +  str(score)
    else:
        err_stat = sr[0]['errors'][0]['statusCode']
        # print "lead_id", lead_id, " error " + sr[0]['errors'][0]['statusCode'] + ":" + sr[0]['errors'][0]['message']
        contact_id_err.append(contact_id)
        status_code_err.append(err_stat)
        pass

print "DONE UPDATING TITLE SCORES ON CONTACTS"



'''
    Code to run if want to update in chunks of 100
'''
# def get_qr_updates(qr_bb_res):
#     qr = qr_bb_res
#     qr_updates = []
#
#     for rec in qr:
#         contact_id = rec['Id']
#         original_title = rec['Title']
#         title = clean_title(title_string=rec['Title'],
#                             mapping_dict=mapping)  ## need to make sure to clean title string
#         score = rec['Title_Score__c']
#         # if score:
#         temp = get_title_points(title=title, level_list= levels, **title_mapping_args)
#         new_title = temp[1]
#         try:
#             new_title = new_title.title() # make upper case 1st letters
#         except:
#             if np.isnan(new_title):
#                 new_title = ''
#             else:
#                 pass
#         score = temp[2]
#         # don't allow negative scores
#         if score <0:
#             score = 0
#         score = str(score)
#         print "updating", contact_id, new_title," Score:", score
#         # rec_update = {'Id': lead_id, 'Title': title, 'Title_Score__c': score, 'type': 'Lead', 'Job_Title_Match__c':new_title}
#         rec_update = {'Id': contact_id, 'Title': original_title, 'Title_Score__c': score, 'type': 'Contact',
#                       'Job_Title_Match__c': new_title}
#         qr_updates.append(rec_update)
#     return  qr_updates
#
# qr_updates = get_qr_updates(qr_bb_res=qr)
# chunks = get_chunks_bb(list_of_records=qr_updates)
# update_chunks_bb(svc=svc, chunk_list=chunks)
# if qr.done == False:
#     qr = svc.queryMore(qr.queryLocator)

# put errors in csv file
# pd.DataFrame({'lead_id':lead_id_err, 'error': status_code_err}).to_csv(outdir +'lead_ids_errors.csv' )