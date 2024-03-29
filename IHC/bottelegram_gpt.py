# -*- coding: utf-8 -*-
"""Cópia de Cópia de Data_Scientist_GPT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lAfPoerzgCt3JBAPBiCsUeL5GiwM1IeH
"""

! pip install pytelegrambotapi

import telebot

API_TOKEN = '6359988878:AAEGxZFvLnDqh35Z1JVx80plDyqKkzepEoM'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def reply_hi(message):
  bot.reply_to(message, 'hi')

bot.polling()

#######################

!pip install pandas pandasai==0.8.4

import pandas as pd
from pandasai import PandasAI

import csv

from pandasai.llm.starcoder import Starcoder

llm = Starcoder(api_token="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")

df = pd.read_csv("https://raw.githubusercontent.com/jasonong/List-of-US-States/master/states.csv",on_bad_lines='skip')

pandas_ai = PandasAI(llm, conversational=False)

a= pandas_ai.run(df, prompt='which state has the abbreviation ca?')

print(df.columns)

a

#a["Abbreviation"].to_string(index=False)



##########################

@bot.message_handler(func=lambda message: True)
def response(message):
    user_message = message.text

    # Verifica se a mensagem do usuário é uma pergunta sobre a abreviação do estado
    if "abbreviation" in user_message.lower():
        # Divide a mensagem do usuário para obter a abreviação
        words = user_message.split()
        abbreviation = None
        for word in words:
            if len(word) == 2 and word.isalpha():
                abbreviation = word.upper()
                break

        if abbreviation:
            # Procura a abreviação no DataFrame e obtém o estado correspondente
            state_info = df[df['Abbreviation'] == abbreviation]
            if not state_info.empty:
                state_name = state_info.iloc[0]['State']
                bot.reply_to(message, f"The state with abbreviation {abbreviation} is {state_name}.")
            else:
                bot.reply_to(message, "I'm not sure which state has that abbreviation.")
        else:
            bot.reply_to(message, "I couldn't find a valid state abbreviation in your question.")
    else:
        # Caso contrário, consulte a biblioteca Pandas AI
        response = pandas_ai.run(df, prompt=user_message)
        bot.reply_to(message, response)

bot.polling()

