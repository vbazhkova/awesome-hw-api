import ydb
import random
import json

def connect_DB(iam_token):
    driver_config = ydb.DriverConfig(
    'grpcs://ydb.serverless.yandexcloud.net:2135', '/ru-central1/b1gd9chcn9avh3nko03c/etn5418na3ttniejtffc',
    credentials=ydb.AccessTokenCredentials(iam_token))
    
    driver = ydb.Driver(driver_config)
    driver.wait(fail_fast=True, timeout=5)
    pool = ydb.SessionPool(driver)
    
    return pool

def ydb_request(pool, text):
    return pool.retry_operation_sync(lambda s: s.transaction().execute(
        text,
        commit_tx=True,
        settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2)
    ))

def get_pets(pool):
    text = """
        SELECT * FROM pets;
    """
    return ydb_request(pool, text) 

def get_pet_by_id(pool, id):
    text = f"""
        SELECT * FROM pets WHERE id == {id};
    """
    return ydb_request(pool, text)  

def get_pets_by_type(pool, type):
    text = f"""
        SELECT * FROM pets WHERE type == "{type}";
    """
    return ydb_request(pool, text)  

def save_new_pet(pool, type, name, id):
    text = f"""
        UPSERT INTO pets ( id, name, type )
        VALUES ( {id}, "{name}", "{type}" );
    """
    return ydb_request(pool, text)

def delete_pet_by_id(pool, id):
    text = f"""
        DELETE FROM pets WHERE id = {id};
    """
    return ydb_request(pool, text)

def update_pet_name(pool, id, name):
    text = f"""
        UPDATE pets SET name = "{name}" WHERE id = {id};
    """
    return ydb_request(pool, text)

def handler(event, context):
    iam_token = context.token['access_token']
    pool = connect_DB(iam_token)

    response_body = {}

    method = event['httpMethod']
    current_url = event['url']
    current_params = event['params']

    if method == 'GET' :
        if current_url == '/pets?':
            response_body = {
                'pets' : get_pets(pool)[0].rows
            }
            
        elif 'pets?type' in current_url:
            pet_type = current_params['type']
            response_body = {
                'pets' : get_pets_by_type(pool, pet_type)[0].rows
            }

        elif 'pets?id' in current_url:
            pet_id = current_params['id']
            response_body = {
                'your_pet' : get_pet_by_id(pool, pet_id)[0].rows
            }
    elif method == 'DELETE':
        if '/pets?' in current_url:
            pet_id = current_params['id']
            delete_pet_by_id(pool, pet_id)
            response_body = {
                'message' : 'Питомец удален'
            }
    elif method == 'PATCH':
        if '/pets?' in current_url:
            body = json.loads(event['body'])
            pet_id = current_params['id']
            pet_new_name = body['new_name']
            update_pet_name(pool, pet_id, pet_new_name)
            response_body = {
                'message' : 'Имя изменено'
            }
    else:
        if '/pets?' in current_url:
            body = json.loads(event['body'])
            pet_type = body['type']
            pet_name = body['name']
            pet_id = random.randint(1, 1000000)
            
            save_new_pet(pool, pet_type, pet_name, pet_id)
            
            response_body = {
                'message' : 'Данные успешно сохранены'
            }
            
            
    return {
        'statusCode': 200,
        'body': response_body,
    }
    # return {
    #     'statusCode': 200,
    #     'body': event,
    # }