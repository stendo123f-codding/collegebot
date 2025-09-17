import aiosqlite


async def create_tables():
    async with aiosqlite.connect('databases/db.db') as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT, ggroup TEXT default None, notifi INTEGER default 1)")
        await db.commit()

async def create_table_zamena():
    async with aiosqlite.connect('databases/db.db') as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS zamena (image TEXT, date TEXT)")
        await db.commit()

async def press_start(user_id, username):
    async with aiosqlite.connect('databases/db.db') as db:
        await db.execute('INSERT INTO users (id, username) VALUES (?, ?)', (user_id, username,))
        await db.commit()

async def user_exists(tg_id):
    async with aiosqlite.connect('databases/db.db') as db:
        exists = await db.execute('SELECT id FROM users WHERE id = ?', (tg_id,))
        data_exists = await exists.fetchone()
        try:
            exists_data = data_exists[0]
        except:
            return 0
        try:
            return exists_data
        except:
            return 0

async def add_to_group(group, user_id):
    async with aiosqlite.connect('databases/db.db') as db:
        await db.execute('UPDATE users SET ggroup = ? WHERE id = ?', (group, user_id,))
        await db.commit()

async def check_group(user_id):
    async with aiosqlite.connect('databases/db.db') as db:
        check = await db.execute('SELECT ggroup FROM users WHERE id = ?', (user_id,))
        group = await check.fetchone()
        end_group = group[0]
        return end_group

async def check_notifi(user_id):
    async with aiosqlite.connect('databases/db.db') as db:
        check = await db.execute('SELECT notifi FROM users WHERE id = ?', (user_id,))
        notifi = await check.fetchone()
        end_notifi = notifi[0]
        print(end_notifi)
        return end_notifi

async def off_notifi(user_id):
    async with aiosqlite.connect('databases/db.db') as db:
        await db.execute('UPDATE users SET notifi = 0 WHERE id = ?', (user_id,))
        await db.commit()

async def on_notifi(user_id):
    async with aiosqlite.connect('databases/db.db') as db:
        await db.execute('UPDATE users SET notifi = 1 WHERE id = ?', (user_id,))
        await db.commit()

async def get_group(user_id):
    async with aiosqlite.connect('databases/db.db') as db:
        check = await db.execute('SELECT ggroup FROM users WHERE id = ?', (user_id,))
        group = await check.fetchone()
        end_group = group[0]
        return end_group

async def get_first_group():
    async with aiosqlite.connect('databases/db.db') as db:
        target_groups = ['es-10', 'em-11', 'es-12', 'sm-13', 'os-14', 'es-22', 'te-11', 'tt-12', 't-13', 'tm-14']
        check = await db.execute(f'SELECT id FROM users WHERE ggroup IN (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', target_groups)
        group_first = await check.fetchall()
        return group_first

async def get_second_group():
    async with aiosqlite.connect('databases/db.db') as db:
        target_groups = ['te-21', 'tt-22', 't-23', 'tm-24', 't-33', 'tm-34', 'ns-23', 'mo-24', 'nm-33', 'ms-34']
        check = await db.execute(f'SELECT id FROM users WHERE ggroup IN (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', target_groups)
        group_first = await check.fetchall()
        return group_first

async def get_second_group_notifi_on():
    async with aiosqlite.connect('databases/db.db') as db:
        target_groups = ['te-21', 'tt-22', 't-23', 'tm-24', 't-33', 'tm-34', 'ns-23', 'mo-24', 'nm-33', 'ms-34']
        check = await db.execute(f'SELECT id FROM users WHERE ggroup IN (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) AND notifi = 1', target_groups)
        group_first = await check.fetchall()
        return group_first

async def get_first_group_notifi_on():
    async with aiosqlite.connect('databases/db.db') as db:
        target_groups = ['es-10', 'em-11', 'es-12', 'sm-13', 'os-14', 'es-22', 'te-11', 'tt-12', 't-13', 'tm-14']
        check = await db.execute(f'SELECT id FROM users WHERE ggroup IN (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) AND notifi = 1', target_groups)
        group_first = await check.fetchall()
        return group_first

async def get_all_users():
    async with aiosqlite.connect('databases/db.db') as db:
        check = await db.execute('SELECT id FROM users')
        users = await check.fetchall()
        return users

async def get_users_notifi_on():
    async with aiosqlite.connect('databases/db.db') as db:
        check = await db.execute('SELECT id FROM users WHERE notifi = 1')
        users = await check.fetchall()
        return users

async def add_zamena(photo, date):
    async with aiosqlite.connect('databases/db.db') as db:
        await db.execute('UPDATE zamena SET image = ?, date = ?', (photo, date,))
        await db.commit()

async def check_date_zamena():
    async with aiosqlite.connect('databases/db.db') as db:
        check = await db.execute('SELECT date FROM zamena')
        get = await check.fetchone()
        fin = get[0]
        return fin

async def get_photo_zamena():
    async with aiosqlite.connect('databases/db.db') as db:
        check = await db.execute('SELECT image FROM zamena')
        photo = await check.fetchone()
        fin = photo[0]
        return fin