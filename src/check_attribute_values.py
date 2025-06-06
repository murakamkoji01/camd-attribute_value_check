import os
import re
import sys
import argparse
import csv
import MeCab as mc
import tqdm
import neologdn

def convert_csv2tsv (info, tgtfile):
  
  with open(tgtfile) as f:
    reader = csv.reader(f)
    for row in reader:
      
      new = []
      for mem in row:
        mem = re.sub('\n', '', mem)
        mem = re.sub('\t', 'TAB', mem)          
        new.append(mem)
        
        line = '\t'.join(new)
        print(line)


def check_csv (tgtfile):
  '''
  Sophisticating input lines
  
  '''

  with open(tgtfile) as f:
    #reader = csv.reader(f)
    reader = csv.reader(f, delimiter='\t')    
    for row in reader:

        new = []
        for mem in row:
          mem = re.sub('\n', '', mem)
          mem = re.sub('\t', 'TAB', mem)
          mem = re.sub('〓', '、', mem)          
          new.append(mem)
          
        line = '\t'.join(new)
        print(line)


        
def old_get_synonym(synonym,synfile):
  '''
  '''
  with open(synfile) as f:
    for line in f:
      line = line.strip()
      row = line.split('\t')
      synonym_word = re.sub('"', '', row[0])
      attribute_id = row[1]
      dictionary_value_id = row[2]
      dictionary_value_name = re.sub('"', '', row[5])

      if(synonym.get(synonym_word)==None):
        synonym[synonym_word] = {}
        #synonym[synonym_word].setdefault('att_id', attribute_id)

      if(synonym[synonym_word].get('att_id')==None):
        synonym[synonym_word]['att_id'] = attribute_id
          
      if(synonym[synonym_word].get('dicval_id')==None):
        synonym[synonym_word]['dicval_id'] = dictionary_value_id

      if(synonym[synonym_word].get('orig')==None):
        synonym[synonym_word]['orig'] = dictionary_value_name

      #---#
      # そのものも登録しておく（必要ないかもだけど一応）
      if(synonym.get(dictionary_value_name)==None):
        synonym[dictionary_value_name] = {}
        #synonym[synonym_word].setdefault('att_id', attribute_id)

      if(synonym[dictionary_value_name].get('att_id')==None):
        synonym[dictionary_value_name]['att_id'] = attribute_id
          
      if(synonym[dictionary_value_name].get('dicval_id')==None):
        synonym[dictionary_value_name]['dicval_id'] = dictionary_value_id

      if(synonym[dictionary_value_name].get('orig')==None):
        synonym[dictionary_value_name]['orig'] = dictionary_value_name        


def tmp_get_synonym(synonym, synonym_matome, synfile):
  '''
  '''
  with open(synfile) as f:
    for line in f:
      line = line.strip()
      row = line.split('\t')
      synonym_word = re.sub('"', '', row[0])
      attribute_id = row[1]
      dictionary_value_id = row[2]
      dictionary_value_name = re.sub('"', '', row[5])

      # 店舗入力表現->辞書エントリ のための辞書
      if(synonym_matome.get(synonym_word)==None):
        synonym_matome[synonym_word] = {}
        #synonym[synonym_word].setdefault('att_id', attribute_id)

      if(synonym_matome[synonym_word].get('att_id')==None):
        synonym_matome[synonym_word]['att_id'] = attribute_id
          
      if(synonym_matome[synonym_word].get('dicval_id')==None):
        synonym_matome[synonym_word]['dicval_id'] = dictionary_value_id

      if(synonym_matome[synonym_word].get('orig')==None):
        synonym_matome[synonym_word]['orig'] = dictionary_value_name

      if(synonym_matome.get(dictionary_value_name)==None):
        synonym_matome[dictionary_value_name] = {}        
        if(synonym_matome[dictionary_value_name].get('orig')==None):
          synonym_matome[dictionary_value_name]['orig'] = dictionary_value_name        

      # 辞書エントリ->類義語展開 のための辞書
      if(synonym.get(dictionary_value_name)==None):
        synonym[dictionary_value_name] = {}
        #synonym[synonym_word].setdefault('att_id', attribute_id)

      if(synonym[dictionary_value_name].get('att_id')==None):
        synonym[dictionary_value_name]['att_id'] = attribute_id
        
      if(synonym[dictionary_value_name].get('dicval_id')==None):
        synonym[dictionary_value_name]['dicval_id'] = dictionary_value_id

      if(synonym[dictionary_value_name].get('syn')==None):
        synonym[dictionary_value_name]['syn'] = synonym_word

      # そのものも登録しておく（必要ないかもだけど一応）
      if(synonym[dictionary_value_name].get('syn')==None):
        synonym[dictionary_value_name]['syn'] = dictionary_value_name

        
def get_synonym(synonym, synonym_matome, synfile):
  '''
  Reading Synonym Dictionary

  synonym : dictionary : 
  synonym_matome : dictionary : 
  synfile : text : file name 
  '''
  with open(synfile) as f:
    for line in f:
      line = line.strip()
      row = line.split('\t')
      synonym_word = re.sub('"', '', row[0])
      attribute_id = row[1]
      dictionary_value_id = row[2]
      dictionary_value_name = re.sub('"', '', row[5])

      #<--- 店舗入力表現->辞書エントリ のための辞書
      if(synonym_matome.get(synonym_word)==None):
        synonym_matome[synonym_word] = {}
        #synonym[synonym_word].setdefault('att_id', attribute_id)

      if(synonym_matome[synonym_word].get(attribute_id)==None):
        synonym_matome[synonym_word][attribute_id] = dictionary_value_name

      if(synonym_matome.get(dictionary_value_name)==None):
        synonym_matome[dictionary_value_name] = {}        

      # そのものも登録しておく（必要ないかもだけど一応）
      if(synonym_matome[dictionary_value_name].get(attribute_id)==None):
          synonym_matome[dictionary_value_name][attribute_id] = dictionary_value_name        

      #<--- 辞書エントリ->類義語展開 のための辞書
      if(synonym.get(dictionary_value_name)==None):
        synonym[dictionary_value_name] = {}
        #synonym[synonym_word].setdefault('att_id', attribute_id)

      if(synonym[dictionary_value_name].get(attribute_id)==None):
        synonym[dictionary_value_name][attribute_id] = {}

      if(synonym[dictionary_value_name][attribute_id].get(synonym_word)==None):
        synonym[dictionary_value_name][attribute_id][synonym_word] = dictionary_value_id
        
      # そのものも登録しておく（必要ないかもだけど一応）
      if(synonym[dictionary_value_name][attribute_id].get(dictionary_value_name)==None):
        synonym[dictionary_value_name][attribute_id][dictionary_value_name] = dictionary_value_id


def get_att_val_dic(dic_val, file_valdic):
  '''
  Reading Attribute values
  format: attribute ID -> dictionary_value_name

  dic_val : dictionary : attribute value information
  file_valdic : text : file name
  '''
  with open(file_valdic) as f:
    for line in f:
      line = line.strip()
      row = line.split('\t')
      attribute_id = row[0]
      attribute_name = row[1]
      dictionary_value_id = row[5]
      dictionary_value_name = row[6]

      if(dic_val.get(attribute_id)==None):
        dic_val[attribute_id] = {}

      if(dic_val[attribute_id].get(dictionary_value_name)==None):
        dic_val[attribute_id][dictionary_value_name] = 1


def old_get_att_id(attid_dic, file_attiddic):
  '''
  Reading attribute ID
  format : 
  '''
  with open(file_attiddic) as f:
    for line in f:
      line = line.strip()
      row = line.split('\t')
      genre_l1 = row[0]
      attribute_id = row[1]
      attribute_name = row[2]

      if(attid_dic.get(genre_l1)==None):
        attid_dic[genre_l1] = {}

      if(attid_dic[genre_l1].get(attribute_name)==None):
        attid_dic[genre_l1][attribute_name] = attribute_id

        
def get_att_id(attid_dic, file_attiddic):
  '''
  Reading attribute names
  format : genre_id -> attribute_name -> 'MANDATORY|OPTIONAL' = 'MANDATORY|OPTIONAL'
           genre_id -> attribute_name -> 'id' = ID

  attid_dic : dictoinary :
  file_attiddic : text : file name
  '''
  #0  	genre_id	genre_name_path	attribute_spec_group_doc_name	attribute_spec_group_detail_doc_name	attribute_id	attribute_name	attribute_dictionary_id	rms_mandatory	rms_input_method	rms_recommend	attribute_data_type	attribute_max_length	attribute_date_format	rms_unit_usable	attribute_unit_name	attribute_unit_list	rms_multi_value_flg	rms_multi_value_limit	attribute_min_value	attribute_max_value	rms_sku_unify_flg	attribute_display_order	cr_date

  with open(file_attiddic) as f:
    for line in f:
      line = line.strip()
      row = line.split('\t')
      genre_id = row[1]
      attribute_id = row[5]
      attribute_name = row[6]
      rms_mandatory = row[8]

      if(attid_dic.get(genre_id)==None):
        attid_dic[genre_id] = {}

      if(attid_dic[genre_id].get(attribute_name)==None):
        attid_dic[genre_id][attribute_name] = {}

      if(attid_dic[genre_id][attribute_name].get('id')==None):
        attid_dic[genre_id][attribute_name]['id'] = attribute_id

      # store attribute style (mandatory/optional)
      if(attid_dic[genre_id][attribute_name].get('mandatory')==None):
        if rms_mandatory == '必須':
          attid_dic[genre_id][attribute_name]['mandatory'] = 'MANDATORY'
        else:
          attid_dic[genre_id][attribute_name]['mandatory'] = 'OPTIONAL'

          
def main (tgt_file,file_syn,file_valdic,file_attiddic,flag_highlight):
  '''
  '''

  # Prepare synonym dictionary
  synonym = dict()
  synonym_matome = dict()  
  get_synonym(synonym, synonym_matome, file_syn)
  test_length = len(synonym)
  print('Synonym dic length: '+str(test_length), file=sys.stderr)
  test_length_matome = len(synonym_matome)
  print('Synonym_matome dic length: '+str(test_length_matome), file=sys.stderr)  

  #print('checkcheck', file=sys.stderr)
  
  dic_val = dict()
  get_att_val_dic(dic_val, file_valdic)
  #print('check')
  
  attid_dic = dict()
  get_att_id(attid_dic, file_attiddic)
  
  #print(f'{tgt_file}', file=sys.stderr)
  
  info = dict()
  line_cnt = 0
  with open(tgt_file) as f:
    lines = f.readlines()
    #for line in f:
    for line in tqdm.tqdm(lines):
      line = line.strip()
      #row = line.split('\t')

      #line = str(line_cnt)+'\t'+line   ##<--- ファイルによる（要調整）
      #print(f'==>{line}')
      row = line.split('\t')
      length = len(row)
      
      count = row[0]
      shop_id  = row[1]
      item_id = row[2]
      inventory_id = row[3]
      sku_info = row[4]
      genre_id = row[5]
      gn1 = row[6]
      ran_code = row[7]
      attribute_name = row[8]
      attribute_value = row[9]
      item_name = row[10]
      item_url = row[11]
      caption = row[12]
      pc_caption = row[13]
      image_url = row[14]
      answer = row[15]
      attribute_id = "NONE"
      line_cnt += 1
#      if row[16]:
#        op_month = row[16]
#      else:
#        op_month = 'NONE'

      # L1-genre
      l1_genre = "NONE"
      if gn1:
        L1_genre = gn1
      else:
        L1_genre = genre_name_path.split('>>')[0]

      flag_mandatory = 'UNKNOWN'
      if attribute_id == 'NONE':
        if genre_id in attid_dic and attribute_name in attid_dic[genre_id]:
          attribute_id = attid_dic[genre_id][attribute_name]['id']
          flag_mandatory = attid_dic[genre_id][attribute_name]['mandatory']          
      
      # checking attribute_value
      ##flag = check_value (attribute_value)
      #attribute_value = re.sub(r'.0000000','',attribute_value)
      attribute_value = re.sub(r'\.0+','',attribute_value)            
      #print('check::'+flag)
      #print(f'===>{attribute_value}')
      re_res = 0

      # 0: attribute value not found in neither attribute dic or synonym dic
      # 1: attribute value found in only attribute dic
      # 2: attribute value found in only synonym dic
      # 3: attribute value found in both synonym dic and attribute dic
      re_res2 = 0

      dictionary_value_name = attribute_value
      #print('(2) att_id:'+attribute_id+' /attribute_name:'+attribute_name+'/attribute_value:'+attribute_value)
    
      # check_value()の結果を使わない(re_res|res_res2 =10を考慮しない）
      # attribute_valueが正しいのかチェック（属性値辞書とのマッチング）
      if attribute_id in dic_val and attribute_value in dic_val[attribute_id]:
        re_res2 = 1
        
      # attribute_valueは店舗入力の値なので、それがattribute_value_nameを持つなら（入力値が何らかの類義語かどうか）標準形を格納
      if attribute_value in synonym_matome and attribute_id in synonym_matome[attribute_value]:
        re_res2 = re_res2 + 2
        dictionary_value_name = synonym_matome[attribute_value][attribute_id]

      # 辞書エントリのSynonymの存在を認識
      # title : 1 / caption : 2 / pc_caption : 3 / sku_info : 4
      re_res_regex,matched_token = match_attval_regex(synonym, dictionary_value_name, attribute_id, item_name, caption, pc_caption, sku_info)
      if (flag_highlight):
        line = highlight_token(re_res_regex, matched_token, line)
                        
      re_res_token = match_attval_tokenization(synonym, dictionary_value_name, attribute_id, item_name, caption, pc_caption, sku_info)      


      #print('---->'+attribute_value+'\t'+item_name)
      judge1 = str(re_res_token)+str(re_res_regex)
      judge2 = str(re_res2)
      #print(judge1+'\t'+judge2+'\t'+line)
      if flag_mandatory == 'UNKNOWN':
        print('M/O'+'\t'+judge1+'\t'+judge2+'\t'+line)
      else:
        print(flag_mandatory+'\t'+judge1+'\t'+judge2+'\t'+line)      
      


def highlight_token(source_id, matched_token, line):
  '''
  highlight matched token with '<highlight>${token}</highlight>'
  '''
  if (source_id==0):
    return line

  row = line.split('\t')
  converted_token = '<highlight>'+matched_token+'</highlight>'

  #print(f'check_debug ==> {matched_token} ==> {converted_token}')
  if (source_id==1):
    #row[10] = re.sub(matched_token,converted_token,row[10])
    title = re.sub(matched_token,converted_token,row[10])
    row[10] = title
  
  elif(source_id==2):
    tmp = re.sub(matched_token,converted_token,row[12])    
    row[12] = tmp
  
  elif(source_id==3):
    tmp = re.sub(matched_token,converted_token,row[13])
    row[13] = tmp
  
  elif(source_id==4):
    tmp = re.sub(matched_token,converted_token,row[4])
    row[4] = tmp

  return '\t'.join(row)


def match_attval_regex(synonym, dictionary_value_name, attribute_id, item_name, caption, pc_caption, sku_info):
  '''
  Find attribute value in information sources (item_name, sku_info, caption and pc_caption)

  synonym : dictonary : synonym dic
  dicionary_value_name : text : attribute value
  attribute_id : int : attribute ID
  item_name : text : item name
  caption : text : caption
  pc_caption : text : pc_caption

  outout:
  1 : attribute value found in item_name
  2 : attribute value found in caption
  3 : attribute value found in pc caption
  4 : attribute value found in sku_info
  0 : attribute value not found in item_name/caption/pc_caption/sku_info
  '''

  cands = []
  cands.append(re.escape(dictionary_value_name))

  # making a list including merchants' input attribute value and its synonyms
  if dictionary_value_name in synonym and attribute_id in synonym[dictionary_value_name]:
    for synonym in synonym[dictionary_value_name][attribute_id]:
      #print(f'target : {synonym}')
      cands.append(re.escape(synonym))

  # information sources are in ordering : (1)item_name (2)sku_info (3)caption (4)pc_caption
  res = 0
  for entry in cands:
    if re.search(entry, item_name):
      res = 1
      return res,entry

  for entry in cands:
    if re.search(entry, sku_info):
      res = 4
      return res,entry

  for entry in cands:    
    if re.search(entry, caption):
      if res == 0:
        res = 2
    if re.search(entry, pc_caption):
      res = 3
      return res,entry

  return res,"none"


def match_attval_tokenization(synonym, dictionary_value_name, attribute_id, item_name, caption, pc_caption, sku_info):
  '''
  Find attribute value in information sources (item_name, sku_info, caption and pc_caption)
  Tokenization by MeCab and word-based matching
  
  synonym : dictonary : synonym dic
  dicionary_value_name : text : attribute value
  attribute_id : int : attribute ID
  item_name : text : item name
  caption : text : caption
  pc_caption : text : pc_caption

  outout:
  1 : attribute value found in item_name
  2 : attribute value found in caption
  3 : attribute value found in pc caption
  4 : attribute value found in sku_info
  0 : attribute value not found in item_name/caption/pc_caption/sku_info
  '''

  cands = []
  cands.append(re.escape(dictionary_value_name))
  #print(f'dictionary_value_name:{dictionary_value_name}')
  
  # making a list including merchants' input attribute value and its synonyms
  if dictionary_value_name in synonym and attribute_id in synonym[dictionary_value_name]:
    for synonym in synonym[dictionary_value_name][attribute_id]:
      cands.append(re.escape(synonym))

  # Tokenizing attribute value candidates
  cands_wakati = []
  for entry in cands:
    cands_wakati.append(re.escape(get_wakati(neologdn.normalize(entry))))
    #print(f'{entry} --> {cands_wakati}')

  res = 0
  # information sources are in ordering : (1)item_name (2)sku_info (3)caption (4)pc_caption
  if check_word(item_name,cands_wakati):
    res = 1
    return res

  if check_word(sku_info,cands_wakati):
    res = 4
    return res  

  if check_word(pc_caption,cands_wakati):
    res = 3
    return res

  if check_word(caption,cands_wakati):
    res = 2
    return res  

  return res


def check_word(source, cands_wakati):
  '''
  Match tokenized candidate with tokens in sources (item_naem/SKU_info/caption/pc_caption)
  '''
  source = re.sub(r'\s+','<s>',source)
  source_wakati = get_wakati(neologdn.normalize(source))
  source_wakati = re.sub(r'<s>',' ',source_wakati)
  source_wakati = re.sub(r'< s >',' ',source_wakati)
  #source_wakati = get_wakati(source)  

  for cand_wakati in cands_wakati:
    # cand is single word, just try to match with word in source
    #print(f'single word : {cand_wakati} :: {source_wakati}')
    if not ' ' in cand_wakati:
      for word in source_wakati.split(' '):
        if cand_wakati == word:
          return True

    # cand is based on multi-words, make patterns to match words in source
    # 多分Ngram作るよりRegexの方が速い
    else:
      #print(f'multi : try: {entry_wakati}')
      pattern1 = cand_wakati+' '
      pattern2 = ' '+cand_wakati
      pattern3 = ' '+cand_wakati+' '
      
      if re.search(pattern1, source_wakati):
        return True
      elif re.search(pattern2, source_wakati):
        return True
      elif re.search(pattern3, source_wakati):
        return True
      #else:
        #print('False')        

  return False



def get_wakati (input_line):
  '''                                                                                                                                                                                                                                  
  分かち書きする
  '''
  t = mc.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/')
  #t = mc.Tagger('-Owakati -d /usr/local/lib/mecab/dic/unidic/')
  #t = mc.Tagger('-Owakati -d /usr/local/lib/mecab/dic/ipadic/')  
  wakati = t.parse(input_line)
  wakati = wakati.rstrip()

  return wakati

    
def check_value(value):
  '''
  '''
  #if re.search('\(|\)', value):
  if re.search('(|)', value):    
    return 'none'
  else:
    return 'valid'
  

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--file', required=True)    # Target Data file
  parser.add_argument('-prep', '--preprocessing', action='store_true')    # flag for data preparation(csv->tsv)
  parser.add_argument('-syn', '--synonym', required=False)    # Synonym dictionary
  parser.add_argument('-avalue', '--attvalue', required=False)    # AttributeValue dictonary
  parser.add_argument('-attid', '--attid', required=False)    # AttributeID dictionary
  parser.add_argument('-high', '--highlight', action='store_true')    # flag for highlighting
  args = parser.parse_args()

  tgt_file = args.file
  file_syn = args.synonym
  file_valdic = args.attvalue
  file_attiddic = args.attid
  flag_highlight = args.highlight

  if args.preprocessing :
    check_csv (tgt_file)   # データ整形の場合
  else :
    main(tgt_file,file_syn,file_valdic,file_attiddic,flag_highlight) # メイン
    
    
