from discord.ext.commands.errors import MissingRequiredArgument
import requests, string, discord, random, datetime
from discord.ext import commands, tasks


owners = [852810538487906334] # your discord id, can put multiple separated by commas e.g [969696, 1234567]
hostname = 'box.your.domain'
admin_user = 'admin_account@your.domain'
admin_pass = 'candicenutsfitinyamouth'
token = 'discordbottoken'
password_characters = string.ascii_letters + string.digits + string.punctuation

client = commands.Bot(command_prefix='.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("A required parameter is missing.") 

@client.event
async def on_ready() :
    print('Bot is ready.')
    await client.change_presence(activity=discord.Activity(name=f"{hostname}", type=5))

@client.command()
async def register(ctx, *, email) :
    if int(ctx.message.author.id) in owners:

        password = ''.join(random.choice(password_characters) for i in range(10))

        register_data = {'email': f'{email}',
                        'password': f'{password}',
                        'privileges': ''}

        register_user = requests.post(f'https://{hostname}/admin/mail/users/add', auth=(f'{admin_user}', f'{admin_pass}'), data=register_data)
        print(register_user.text, register_user.status_code)
        
        if 'mail user added' in register_user.text :
            embed=discord.Embed(
                                title="Account created", 
                                description="nice",
                                color=0x109319,
                                timestamp=datetime.datetime.utcnow()
                                )

            
            embed.set_author(name=f"Requested by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)

            embed.add_field(name="Username", value=f"`{email}`", inline=False) 
            embed.add_field(name="Password", value=f"`{password}`", inline=False)

            await ctx.channel.send(embed=embed)
        else:
            
            embed=discord.Embed(
                                title="Error", 
                                description="oh shit",
                                color=0x109319,
                                timestamp=datetime.datetime.utcnow()
                                )

            
            embed.set_author(name=f"Requested by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)

            embed.add_field(name="Error message:", value=f"`{register_user.text}`", inline=False) 

            await ctx.channel.send(embed=embed)

@client.command()
async def ban(ctx, *, email) :
    if int(ctx.message.author.id) in owners:

        remove_data = {'email': f'{email}'}

        remove_user = requests.post(f'https://{hostname}/admin/mail/users/remove', auth=(f'{admin_user}', f'{admin_pass}'), data=remove_data)
        
        if 'mail user removed' in remove_user.text :
            embed=discord.Embed(
                                title="Banned.", 
                                description="lol rip",
                                color=0x109319,
                                timestamp=datetime.datetime.utcnow()
                                )

            
            embed.set_author(name=f"Banned by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)

            embed.add_field(name="Affected user", value=f"`{email}`", inline=False) 

            await ctx.channel.send(embed=embed)

        else:
            
            embed=discord.Embed(
                                title="Error", 
                                description="oh shit",
                                color=0x109319,
                                timestamp=datetime.datetime.utcnow()
                                )

            
            embed.set_author(name=f"Command run by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)

            embed.add_field(name="Error message:", value=f"`{remove_user.text}`", inline=False) 

            await ctx.channel.send(embed=embed)

@client.command()
async def addalias(ctx, alias, *, email) :
    if int(ctx.message.author.id) in owners:
            alias_data = {
                        'update_if_exists': '0',
                        'address': f'{alias}',
                        'forwards_to': f'{email}',
                        'permitted_senders': ''
                        }

            add_alias = requests.post(f'https://{hostname}/admin/mail/aliases/add', auth=(f'{admin_user}', f'{admin_pass}'), data=alias_data)
            
            if 'alias added' in add_alias.text :
                embed=discord.Embed(
                                    title="Alias added", 
                                    description="gg",
                                    color=0x109319,
                                    timestamp=datetime.datetime.utcnow()
                                    )

                
                embed.set_author(name=f"Added by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)

                embed.add_field(name=f"`{alias}` now forwards to `{email}`", value=f"‎", inline=False) # invis char in value 

                await ctx.channel.send(embed=embed)
            
            else:
            
                embed=discord.Embed(
                                    title="Error", 
                                    description="oh shit",
                                    color=0x109319,
                                    timestamp=datetime.datetime.utcnow()
                                    )

                embed.set_author(name=f"Command run by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
                embed.add_field(name="Error message:", value=f"`{add_alias.text}`", inline=False) 
                await ctx.channel.send(embed=embed)

@client.command()
async def rmalias(ctx, alias):
        if int(ctx.message.author.id) in owners:
            alias_data = {
                                'address': f'{alias}'
                                }

            remove_alias = requests.post(f'https://{hostname}/admin/mail/aliases/remove', auth=(f'{admin_user}', f'{admin_pass}'), data=alias_data)
            
            if 'alias removed' in remove_alias.text :
                embed=discord.Embed(
                                    title="Alias removed", 
                                    description="f",
                                    color=0x109319,
                                    timestamp=datetime.datetime.utcnow()
                                    )

                
                embed.set_author(name=f"Removed by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)

                embed.add_field(name=f"`{alias}` no longer forwards emails", value=f"‎", inline=False) # invis char in value 

                await ctx.channel.send(embed=embed)

            else:
            
                embed=discord.Embed(
                                    title="Error", 
                                    description="oh shit",
                                    color=0x109319,
                                    timestamp=datetime.datetime.utcnow()
                                    )

                embed.set_author(name=f"Command run by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
                embed.add_field(name="Error message:", value=f"`{remove_alias.text}`", inline=False) 
                await ctx.channel.send(embed=embed)


            
client.run(f'{token}')


