# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 00:20:04 2023

@author: saura
"""

import openai
from openai import OpenAI

# from openai import AsyncOpenAI

def main(api_key):
    
    prompt = f"""
    Your task is to answer the question by only using the context to answer the question. 
    There are three contexts in total. 
    Each context consists of two part one is text another is author of the context. 
    Use all the text in the context to answer the question and mention author name after using the text. 
    Whenever you mention author name mention it as (Author et al) where Author is author's name followed by 'et al'.
    Question: What is the difference between GPT and BERT models?
    Context 1 author: Trinita Roy
    Context 1 text: BERT is an encoder transformer model which is trained on two tasks - masked
    LM and next sentence prediction.
    Context 2 author: Asheesh Kumar
    Context 2 text: GPT is a decoder model that works best on sequence generation tasks.
    Context 3 author: Siddhant Jain
    Context 3 text: LSTMs have been very popular for sequence-to-sequence tasks but have
    limitations in processing long texts.
    """
    
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(model="gpt-3.5-turbo-1106", messages=[{"role": "user", "content": prompt}])
    
    return prompt,completion

if __name__ == '__main__':
     
     api_key = input("Enter OpenAI api key :  ")
     query,comp = main(api_key)
     print('Prompt Used:\n')
     print(query)
     print('\n\n')
     print('Response:\n')
     print(comp.choices[0].message.content)
    
