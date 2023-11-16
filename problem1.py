# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 12:05:40 2023

@author: saura
"""

from openai import OpenAI
import json


if __name__ == '__main__':
    
    api_key = input("Enter OpenAI api key :  ")
    
    client = OpenAI(api_key=api_key)
    
    sentences = []

    # reading pdf file for assistant
    file = client.files.create(
      file=open("knowledge.pdf", "rb"),
      purpose='assistants'
    )
    
    # Creating assistant
    assistant = client.beta.assistants.create(
      instructions="""
      You are tasked with developing an AI assistant capable of extracting and paraphrasing the abstract of research papers. The assistant should have the following functionalities:

        Get Abstract:
        
        Implement a feature that allows users to ask the assistant to retrieve the abstract of a given research paper.
        Paraphrasing Functionality:
        
        Develop a paraphrasing capability for the assistant based on the following user input:
        a. Tone: Academic / Creative / Aggressive
        b. Output Length: 1x (same length) / 2x (twice the length) / 3x (thrice the length)
      """,
      model="gpt-3.5-turbo-1106",
      tools=[{"type": "retrieval"}],
      file_ids=[file.id]
    )
    
    thread = client.beta.threads.create()
    
    message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content="Create an abstract of the provided data",
    )
    
    run = client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=assistant.id,
    )
    
    run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id=run.id
    )
    
    while run.status == 'in_progress':
        ## Loop to check status of request
        run = client.beta.threads.runs.retrieve(
          thread_id=thread.id,
          run_id=run.id
        )
    
    print('Done')

    
    messages1 = client.beta.threads.messages.list(
      thread_id=thread.id
    )
    
    sentences.append(messages1.data[0].content[0].text.value)
    print('Abstract created by assistant:\n')
    print(messages1.data[0].content[0].text.value)
    print('\n\n')
    
    tone = input("Enter tone ('Academic / Creative / Aggressive'): ")
    length = input("Enter length (1x / 2x / 3x): ")
    
    message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content=f"Now paraphrase the abstract with {tone} tone and {length} length",
    )
    
    run = client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=assistant.id,
    )
    
    run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id=run.id
    )
    
    while run.status == 'in_progress':
        
        run = client.beta.threads.runs.retrieve(
          thread_id=thread.id,
          run_id=run.id
        )
    
    print('Done')

    
    messages2 = client.beta.threads.messages.list(
      thread_id=thread.id
    )
    
    sentences.append(messages2.data[0].content[0].text.value)
    print('Paraphrased response created by assistant:\n')
    print(messages2.data[0].content[0].text.value)
    print('\n\n')
    
    json_data = json.dumps(sentences, indent=2)  
    
    # Save the JSON data to a file
    with open('gpt_output.json', 'w') as json_file:
        json_file.write(json_data)