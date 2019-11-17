#!/usr/bin/env python
# coding: utf-8

# In[1]:


############################################################################################################
# Feature extraction from sentiment and metadata 
# df_v2 = train.csv + basic sentiment data + image features
# df_v3 = df_v2 + countRescuer
# df_v4 = df_v3 + pure breed

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import json
import matplotlib.pyplot as plt
import numbers

# Set the correct path for yourself:

import os
print(os.listdir("./"))


# In[2]:


############################################################################################
############################ Feature Merging ##############################################
############################################################################################

#helper function: get sum of var
def summ_var(obs,var_type):
    ''' obs: a dictionary read from json file. 
        var_type: either 'magnitude' or 'score'. '''    
    sum_var=0
    for i in obs['sentences']:
        sum_var+=i['sentiment'][var_type]
    return sum_var

#helper function: get entities (labels, tags) from description as string
def get_tags(obs):
    final_tags = []
    ent = obs['entities'] # list of entities
    for i in ent:
        final_tags.append(i['name'])
    joined = ' '.join(final_tags)
    return joined 

def merge_sentiment(folder):
    
    files = [f for f in os.listdir(folder)]
    record=[]
    for j in files:
        file = folder+j
        
        with open (file, 'r',encoding="utf8") as f: #read all the files
            obs = json.load(f)
        if type(obs)==list: data=obs[0] #sometimes json's are as list, sometimes dictionary,
        else: data=obs                 #here it is handled
        j=j[:-5]    #We want PetID without ".json" part
        doc_mag=data['documentSentiment']['magnitude'] #whole description magnitude!
        doc_score=data['documentSentiment']['score']  #whole desription score!
        sent_count = len(data['sentences']) #how many sentences?
        sen1_mag=data['sentences'][0]['sentiment']['magnitude'] #magnitude of the 1st sentence
        sen1_score=data['sentences'][0]['sentiment']['score'] #score of the 1st sentence
        sum_mag=summ_var(data,'magnitude') #sum magnitude of all sentences
        sum_score=summ_var(data,'score') #sum score of all sentences
        tags = get_tags(data) #returns a string with comma-separated tags
        record.append([j,doc_mag,doc_score,sent_count,sen1_mag,sen1_score, sum_mag, sum_score, tags])
    
    #Our DataFrame with columns as below:
    rec_df = pd.DataFrame(record,columns=['PetID','docMagnitude','doc_score','sent_count', 'sen1_magnitude','sen1_score', 'sum_mag', 'sum_score','sent_tags'])   
    
    # Correct the magnitude and sum of magnitude, dividing it by sentences number
    rec_df['doc_mag_corr']= rec_df.docMagnitude / rec_df.sent_count
    rec_df['sum_mag_corr']= rec_df.sum_mag / rec_df.sent_count
    
    del rec_df['docMagnitude']
    # does pet have english description
    sentiment = rec_df #we ignore Adoption Speed merging
    sentiment['has_eng_description']=np.where(sentiment.doc_mag_corr.isnull()==True, 0,1)
    
    return sentiment


# In[3]:


def merge_metadata(folder, pics):
    
    files = [f for f in os.listdir(folder)]
    record_img=[]
    for j in files:
        file = folder+j
      
        with open (file, 'r',encoding="utf8") as f: #read all the files
            obs = json.load(f)
        if type(obs)==list: data=obs[0] #sometimes json's are as list, sometimes dictionary,
        else: data=obs    #here it is handled        
        
        if pics != "ALL": condition = "j[-6] == '1'" #do we want just 1st pic or all
        else: condition = 'True'
        flag=eval(condition)
            
        if flag==True:
        
        #1. CropHintsAnnotation:
    
        #boundingPoly 	: The bounding polygon for the crop region. 
        #The coordinates of the bounding box are in the original image's scale.
        #confidence 	:Confidence of this being a salient region. Range [0, 1].
        #importanceFraction 	: Fraction of importance of this salient region with respect to the original image. 

            img_bound_polygon_x = data['cropHintsAnnotation']['cropHints'][0]['boundingPoly']['vertices'][2]['x']
            img_bound_polygon_y = data['cropHintsAnnotation']['cropHints'][0]['boundingPoly']['vertices'][2]['y']
            img_confidence = data['cropHintsAnnotation'] ['cropHints'] [0] ['confidence']
            try: 
                img_imp_fract = data['cropHintsAnnotation'] ['cropHints'] [0] ['importanceFraction']
            except KeyError:
                img_imp_fract = 0
                
        #2. imagePropertiesAnnotation:
        
            try:
                domcol_r = data['imagePropertiesAnnotation']['dominantColors']['colors'][0]['color']['red']
                domcol_g = data['imagePropertiesAnnotation']['dominantColors']['colors'][0]['color']['green']
                domcol_b = data['imagePropertiesAnnotation']['dominantColors']['colors'][0]['color']['blue']
            except KeyError:
                domcol_r,domcol_g,domcol_b = 0,0,0
        
        # 3. labelAnnotations: tags, like 'dog', 'puppy' , with topicality score.
            file_keys = list(data.keys())
        
            if 'labelAnnotations' in file_keys:
                file_annots = data['labelAnnotations'][:int(len(data['labelAnnotations']) * 0.3)]
                file_top_score = np.asarray([x['score'] for x in file_annots]).mean()
                file_top_desc = [x['description'] for x in file_annots]
            else:
                file_top_score = np.nan
                file_top_desc = ['']
            meta_tags = ' '.join(file_top_desc)  
            
        # 4. imagePropertiesAnnotation
            file_colors = data['imagePropertiesAnnotation']['dominantColors']['colors']
            file_crops = data['cropHintsAnnotation']['cropHints']

            file_color_score = np.asarray([x['score'] for x in file_colors]).mean()
            file_color_pixelfrac = np.asarray([x['pixelFraction'] for x in file_colors]).mean()

            file_crop_conf = np.asarray([x['confidence'] for x in file_crops]).mean()
        
            if 'importanceFraction' in file_crops[0].keys():
                file_crop_importance = np.asarray([x['importanceFraction'] for x in file_crops]).mean()
            else:
                file_crop_importance = np.nan
  
            PetID = j[:-7] #PetID
            PetID=PetID.replace('-','') #just in case
            if pics == "ALL": 
                PetID_pic=j[:-5]    #We want PetID with "-picture number.json" part
                pic_no = int(j[-6])
            row = [PetID, img_bound_polygon_x,img_bound_polygon_y, img_confidence, 
                   img_imp_fract, domcol_r, domcol_g, domcol_b, file_top_score, meta_tags,
                   file_color_score, file_color_pixelfrac, file_crop_conf, file_crop_importance]
            if pics == "ALL": 
                row.append(PetID_pic) 
                row.append(pic_no) 
            record_img.append(row)
            row=[]  #clear
    
    columns =  ['PetID', 'img_bound_polygon_x','img_bound_polygon_y','img_confidence',
               'img_imp_fract','domcol_r','domcol_g','domcol_b','file_top_score', 'img_tags',
               'file_color_score', 'file_color_pixelfrac', 'file_crop_conf', 'file_crop_importance']
    
    if pics == "ALL":  
        columns.append('PetID_pic')
        columns.append('pic_no')
    
    rec_img_df = pd.DataFrame(record_img, columns = columns)
    
    rec_img_df.set_index('PetID')
    
    return rec_img_df


# In[4]:


def get_all_data(ds_type, directory, pics):
    ''' Extracts features: text sentiment and metadata images.
        Merges it with CSV and returns the final file.
        ds_type - train or test, which file are you separating
        directory - dir to place with test.csv, train.csv and folders with metadata
    '''
    #-1.Set the directory
    os.chdir(directory)
    folder_sentiment= ds_type + "_sentiment/" 
    folder_meta= ds_type + "_metadata/"
    
    dataset = pd.read_csv(ds_type + '/' + ds_type + '.csv')
    
    # 2. GET DESCRIPTION (TEXT) SENTIMENT DATA
    sentiment_df = merge_sentiment(folder_sentiment)

    # 3. GET IMAGES METADATA & MERGE IT WITH THE REST
    
    metadata_df = merge_metadata(folder_meta, pics)
    # 4. MERGE ALL FILES
    dataset_meta = pd.merge(dataset, metadata_df,  how="outer", left_on='PetID' , right_on='PetID', suffixes=('_img','_dataset'))
    
    dataset_meta_senti = pd.merge(dataset_meta, sentiment_df, how="left", left_on='PetID' , right_on='PetID', suffixes=('_every','_sent'))
      
    # 5. CLEAR FINAL DATASET
    df = dataset_meta_senti
    
    return df


# In[5]:


############################################################################################
############################ Feature Aggregation ###########################################
############################################################################################

def merge_tags(array):
    try:
        res = ' '.join(array)
    except TypeError:
        res = ' '.join(str(array))
    return res

def aggregate_features(data):
    ''' returns features per pet, not per picture '''
    #we separate columns connected to image: only those will be summed. Rest: only averaged
    img_cols = ['img_bound_polygon_x','img_bound_polygon_y','img_confidence',
               'img_imp_fract','domcol_r','domcol_g','domcol_b','file_top_score', 'img_tags',
               'file_color_score', 'file_color_pixelfrac', 'file_crop_conf', 'file_crop_importance']
    sent_cols = [ 'docMagnitude', 'doc_score', 'sent_count', 'sen1_magnitude', 'sen1_score', 'sum_mag',
                 'sum_score', 'sent_tags', 'doc_mag_corr', 'sum_mag_corr', 'has_eng_description']
    added_cols = img_cols + sent_cols
    final_df = pd.DataFrame()
    cols = list(data)
    for col in cols:
        if isinstance(data[col][0], numbers.Number): #if numeric, we aggregate:
            column = data.groupby(['PetID'])[col].mean()
            if col in added_cols: #name: either 'normal' or with suffix
                final_df[col+'_Mean'] = column
            else:
                final_df[col] = column
            if col in img_cols: #also sum
                column2 = data.groupby(['PetID'])[col].sum()
                final_df[col+'_Sum'] = column2
        
        else:  # text object   
            column = data.groupby(['PetID'])[col].unique()
            if col=='PetID': column = [x[0] for x in column]
            else:
                column = column.map(merge_tags)
            final_df[col]= column
            
    return final_df


# In[6]:


def count_rescuer(df):
    rescuer_count = df.groupby(['RescuerID'])['PetID'].count().reset_index()
    rescuer_count.columns = ['RescuerID', 'RescuerID_COUNT']
    df = df.merge(rescuer_count, how='left', on='RescuerID')
    del df["RescuerID"]
    return df


# In[7]:


def pure_breed(df):
    extra_df = pd.DataFrame() 
    count = 0
    
    for i in range (0, len(df)):
        pure_breed_1 = df.iloc[i]['Breed1']
        pure_breed_2 = df.iloc[i]['Breed2']
        
        if (pure_breed_1 != pure_breed_2 
        or int(pure_breed_2) == 307 # mixed breed
        or int(pure_breed_1) == 307
        or pure_breed_2 == None):
            is_pure_breed = 0
        else:
            count = count + 1
            is_pure_breed = 1
            
        extra_df = extra_df.append({'PureBreed': is_pure_breed}, ignore_index = True)
    
    #print('Total pure breed: ', count)
    assert(len(df) == len(extra_df))
    df = df.join(extra_df)
    
    return df


# In[8]:


def merge_PetID(ID_source, y):
    ID_source=ID_source.reset_index()
    try:
        y=y.reset_index(drop=True)
    except AttributeError:
        pass
    y_df = pd.DataFrame(y)
    y_final = pd.concat([ID_source['PetID'],y_df],ignore_index=True, axis=1)
    y_final.columns=["PetID","AdoptionSpeed"]
    return y_final


# In[9]:


# TRAIN

# Obtain CSV file merged with other features (text sentiment and metadata images).
df=get_all_data(ds_type="train",directory="./petfinder-adoption-prediction/",pics="ALL")
# Return features per pet, not per picture.
df_v2 = aggregate_features(df)
df_v3 = count_rescuer(df_v2)
df_v4 = pure_breed(df_v3)


# In[11]:


# WRITE FINAL TRAIN/TEST CSV DATA

df_v4.to_csv('final_train.csv',index=False)

