from discord import Client, Embed, webhook
from get_data import *
from sqlite3 import connect
from json import dumps, loads


client = Client()

token = "NzEwNDg0NTQzOTM2NjU5NTU4.Xr1ISw.JtKa5nC9HEMRr5g_aWCzTycUbsE"

data_base = connect('./data.db')
cursor = data_base.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS jsons (id text, json text, i real)")

def editor(s, message_id):
    data = cursor.execute(f"SELECT * FROM jsons WHERE id={message_id}")
    results = []
    for i in data:
        results += i
    old_i = results[2]
    i = old_i
    if s == True:
        i += 1
    elif s == False and (i==0 or i >= len(results[1])):
        i = 0
    else:
        i -= 1
    json = results[1].replace('[', '').replace(']', '')
    json = '{'+json.split(', {')[int(i)]
    json = loads(json)
    cursor.execute(f"UPDATE jsons SET i={i} WHERE id={message_id}")
    style = Embed(title=json['name'])
    style.set_image(url=json['image_link'])
    return style



@client.event
async def on_ready():
    print('HI')

@client.event
async def on_message(message):
    global i, results, msg
    i = 0
    if '!find ' in message.content:
        try_find = message.content[len('!find '):]
        style = Embed(title='Carregando', description=f'<@{message.author.id}>')
        msg = await message.channel.send(embed=style)
        results = get_reference(try_find)
        cursor.execute(f"INSERT INTO jsons VALUES ('{msg.id}', '{dumps(results)}', {i})")
        data_base.commit()
        style = Embed(title=results[i]['name'])
        style.set_image(url=results[i]['image_link'])
        await msg.edit(embed=style)
        await msg.add_reaction('◀️')
        await msg.add_reaction('▶️')


@client.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        if reaction.emoji  == '▶️':
            result = editor(True, reaction.message.id)
            await reaction.message.edit(embed=result)
        if reaction.emoji  == '◀️':
            result = editor(False, reaction.message.id)
            await reaction.message.edit(embed=result)

@client.event
async def on_reaction_remove(reaction, user):
    if not user.bot:
        if reaction.emoji  == '▶️':
            result = editor(True, reaction.message.id)
            await reaction.message.edit(embed=result)
        if reaction.emoji  == '◀️':
            result = editor(False, reaction.message.id)
            await reaction.message.edit(embed=result)




client.run(token)
