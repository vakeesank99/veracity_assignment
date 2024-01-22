import json
import ijson
import csv
import pandas as pd

#change the following paths
input_file_path = 'C:\\Users\\vakee\\veracity_ai\\docs\\dev.jsonl' #initial file
jsonl_file_path = 'C:\\Users\\vakee\\veracity_ai\\docs\\cleaned_file.jsonl'  #after cleaning
csv_file_path = 'C:\\Users\\vakee\\veracity_ai\\docs\\dev.jsonl2.csv' #final csv file link

def clean_dataset(input_file_path,jsonl_file_path):

    with open(input_file_path, 'r',encoding='utf-8') as infile, open(jsonl_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            try:
                json.loads(line)
                outfile.write(line)
            except json.JSONDecodeError as e:
                print(f"Ignoring line due to JSON decoding error: {e}")

def jsonl2csv(jsonl_file_path,csv_file_path):
    # Define the chunk size (adjust as needed)
    chunk_size = 1000

    # Create an iterator to read the JSONL file in chunks
    jsonl_reader = pd.read_json(jsonl_file_path, lines=True, chunksize=chunk_size)
    # Iterate through chunks and append to CSv
    for i, chunks in enumerate(jsonl_reader):
        # we need`document_title`, `question_text`, `short_answer`, `yes_no_answer` columns.
        short_answers_list = []
        yes_no_answer_list = []
        for j,chunk in enumerate(chunks["annotations"]): #runs chunk_size times
            short_answers=[]
            yes_no_answer=[]
            for k,sub_chunk in enumerate(chunk): #runs for 5 times
                if (sub_chunk['short_answers']!=[] ):
                    start_token=sub_chunk['short_answers'][0]['start_token']
                    end_token=sub_chunk['short_answers'][0]['end_token']
                    try:
                        ans=chunks['document_tokens'][j][start_token]['token'] +" "+ chunks['document_tokens'][j][end_token-1]['token']
                    except:
                        ans=None
                else:
                    ans=None
                short_answers.append(ans)
                yes_no_answer.append(sub_chunk.get('yes_no_answer',None))

            short_answers_list.append(short_answers)
            yes_no_answer=[i for i in yes_no_answer if i != 'NONE']
            if yes_no_answer==[]:
                yes_no_answer_list.append(None)
            else:
                yes_no_answer_list.append(list(set(yes_no_answer))[0])

        # Create a DataFrame with 'short_answers_0', 'short_answers_1', etc. columns
        short_answers_df = pd.DataFrame(short_answers_list)#.add_prefix('short_answers')   #here bro
        short_answers_df.columns = [f'short_answer{int(c)+1}' for c in short_answers_df]
        # yes_no_answer = [item.get('short_answers', None) if isinstance(item, dict) else None for item in chunk['annotations']]
        yes_no_answer_df = pd.DataFrame({'yes_no_answer': yes_no_answer_list})
        # Concatenate the original chunk with the required data
        chunk_concatenated = pd.concat([chunks['document_title'], chunks['question_text'] ,short_answers_df, yes_no_answer_df], axis=1) #
        # We drop any rows with NaN values
        chunk_concatenated.dropna(axis = 0)

        if i == 0:
            # For the first chunk, create the CSV file with header
            chunk_concatenated.to_csv(csv_file_path, index=False, mode='w')
        else:
            # For subsequent chunks, append to the existing CSV file without header
            chunk_concatenated.to_csv(csv_file_path, index=False, header=False, mode='a')
        print(f'Processed chunk {i + 1}')
    print('Conversion completed.')

#first clean the dataset    
clean_dataset(input_file_path,jsonl_file_path)

#then convert to csv
jsonl2csv(jsonl_file_path,csv_file_path)
