# -*- coding: utf-8 -*-
import os
import json
import numpy as np
import tkinter as tk

def dict_to_json(o, level=0):
    INDENT = 3
    SPACE = " "
    NEWLINE = "\n"
    ret = ""
    if isinstance(o, dict):
        ret += "{" + NEWLINE
        comma = ""
        for k,v in o.items():
            ret += comma
            comma = ",\n"
            ret += SPACE * INDENT * (level+1)
            ret += '"' + str(k) + '":' + SPACE
            ret += dict_to_json(v, level + 1)

        ret += NEWLINE + SPACE * INDENT * level + "}"
    elif isinstance(o, str):
        ret += '"' + o + '"'
    elif isinstance(o, list):
        ret += "[" + ",".join([dict_to_json(e, level+1) for e in o]) + "]"
    elif isinstance(o, bool):
        ret += "true" if o else "false"
    elif isinstance(o, int):
        ret += str(o)
    elif isinstance(o, float):
        ret += '%.7g' % o
    elif isinstance(o, np.ndarray) and np.issubdtype(o.dtype, np.integer):
        ret += "[" + ','.join(map(str, o.flatten().tolist())) + "]"
    elif isinstance(o, np.ndarray) and np.issubdtype(o.dtype, np.inexact):
        ret += "[" + ','.join(map(lambda x: '%.7g' % x, o.flatten().tolist())) + "]"
    elif o is None:
        ret += 'null'
    else:
        raise TypeError("Unknown type '%s' for json serialization" % str(type(o)))
    
    return ret

def readJSON(path):
    with open(path, 'r', encoding='utf-8') as reader:
        jf = json.load(reader)
    return jf

def writeJSON(JSON_path, data):
    ret = dict_to_json(data, level=0)
    with open(JSON_path, 'w', encoding='utf-8') as writer:
        writer.write(ret)
    return None

def delete_texts():
    builddata_key.delete(0, tk.END)
    builddata_emoji.delete(0, tk.END)
    generator_input.delete('1.0', tk.END)
    generator_output.delete('1.0', tk.END)

def generator():
    # delete all texts
    delete_texts()
    
    # make build data page invisible
    builddata_key.place_forget()
    builddata_emoji.place_forget()
    builddata_button.place_forget()
    key_label.place_forget()
    emoji_label.place_forget()
    description_label.place_forget()
    
    # make generator page visible
    generator_input.place(x=200, y=175, width=400, height=175)
    generator_output.place(x=200, y=400, width=400, height=175)
    generator_button.place(x=350, y=360, width=100, height=30)

def build_data():
    # delete all texts
    delete_texts()
    
    # make generator page invisible
    generator_input.place_forget()
    generator_output.place_forget()
    generator_button.place_forget()
    
    # make build data page visible
    builddata_key.place(x=300, y=225, width=300, height=35)
    builddata_emoji.place(x=300, y=270, width=300, height=35)
    builddata_button.place(x=350, y=315, width=100, height=30)
    key_label.place(x=200, y=230)
    emoji_label.place(x=200, y=275)
    description_label.place(x=310, y=175)

def save():
    key = builddata_key.get()
    emoji_raw = builddata_emoji.get()
    emoji_arr = emoji_raw.split(' ')
    
    for emoji in emoji_arr:
        if key in database:
            if emoji not in database[key]:
                database[key].append(emoji)
        else:
            database[key] = [emoji]
    
    delete_texts()
    writeJSON(json_name, database)

def generate():
    input_raw = generator_input.get("1.0","end")
    input_line = input_raw.split('\n')
    input_line.pop(len(input_line)-1)
    
    output_line = []
    for sentence in input_line:
        if sentence == '':
            output_line.append(sentence)
            continue
        word_list = []
        for i in range(len(sentence)-1):
            word_list.append(sentence[i])
            word_list.append(sentence[i:2])
        word_list.append(sentence[len(sentence)-1])
        
        emoji_list = []
        for word in word_list:
            if word in database:
                for emoji in database[word]:
                    emoji_list.append(emoji)
                    
        emoji_num = round(np.random.normal(3, 1))
        if emoji_num > 4:
            emoji_num = 4
        elif emoji_num < 2:
            emoji_num = 2
        
        if emoji_list == []:
            index = np.random.randint(len(database['random']))
            temp = sentence
            for i in range(emoji_num):
                temp = temp + database['random'][index]
            output_line.append(temp)
        else:
            index = np.random.randint(len(emoji_list))
            temp = sentence
            for i in range(emoji_num):
                temp = temp + emoji_list[index]
            output_line.append(temp)
    
    output = str()
    for sentence in output_line:
        output = output + sentence + '\n'
    
    generator_output.delete('1.0', tk.END)
    generator_output.insert(tk.END, output)

if __name__ == '__main__':
    # program_path = os.path.dirname(__file__)
    json_name = 'database.json'
    database = {}
    if os.path.isfile(json_name):
        database = readJSON(json_name)
    else:
        database['random'] = ['😎', '😂', '🤣', '😜']
        writeJSON(json_name, database)
    
    # build window
    window = tk.Tk()
    window.title('複製文產生器')
    window.geometry('800x600')
    window.configure(background='white')
    
    
    # build buttons
    header_label = tk.Label(window, text='複製文產生器', font=('微軟正黑體', 32))
    header_label.pack()
    
    top_frame = tk.Frame(window)
    top_frame.pack(side=tk.TOP)
    left_button = tk.Button(top_frame, text='生成複製文', font=('微軟正黑體', 12), width=30, height=4, command=generator)
    left_button.pack(side=tk.LEFT)
    right_button = tk.Button(top_frame, text='建立資料庫', font=('微軟正黑體', 12), width=30, height=4, command=build_data)
    right_button.pack(side=tk.LEFT)
    
    
    # generator page
    generator_input = tk.Text(window)
    generator_output = tk.Text(window)
    generator_button = tk.Button(window, text='轉換', font=('微軟正黑體', 12), command=generate)
    
    # build data page
    builddata_key = tk.Entry(window, font=('微軟正黑體', 12))
    builddata_emoji = tk.Entry(window, font=('微軟正黑體', 12))
    builddata_button = tk.Button(window, text='儲存', font=('微軟正黑體', 12), command=save)
    key_label = tk.Label(window, text='關鍵字', font=('微軟正黑體', 12))
    emoji_label = tk.Label(window, text='表情', font=('微軟正黑體', 12))
    description_label = tk.Label(window, text='*關鍵字限制一至二個字*', font=('微軟正黑體', 12))
    
    window.mainloop()
    
    


