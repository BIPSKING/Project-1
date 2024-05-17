import json

filename = "task.json"

#returns true or false
def list_store():
    with open(filename,'r') as f:
        temp_data_load = json.load(f)
    if temp_data_load != []:
        return True
    else:
        return False

#load files
def load_tasks():
    with open(filename,'r') as f:
        task_items = []
        temp_data_get = json.load(f)
    
    if temp_data_get != []:
        for i in range(len(temp_data_get)):
            task_items.append([temp_data_get[i]['id'],temp_data_get[i]['task'],temp_data_get[i]['date'],temp_data_get[i]['time'],temp_data_get[i]['complete state']])
        return task_items
    else:
        pass

#Add Tasks to the Json file:
def add_task(task,date,time):
    item_data = {}
    index_counter = 0
    with open (filename,'r') as f:
        temp_data = json.load(f)

    if temp_data != []:
        index_counter = temp_data[-1]['id']
    else:
        index_counter = -1

    item_data['id'] = int(index_counter) + 1
    item_data['task'] = task
    item_data['date'] = date
    item_data['time'] = time
    item_data['complete state'] = False

    temp_data.append(item_data)

    with open (filename,'w') as fi:
        json.dump(temp_data,fi,indent=4)


#Delete Tasks to the Json file:
def pop_task(index):
    with open (filename,'r') as f:
        temp_data_pop = json.load(f)

    temp_data_pop.pop(index)

    with open(filename,'w') as fi:
        json.dump(temp_data_pop,fi,indent=4)

#Sort ids
def sort_id():
    index_counter = 0
    
    with open (filename,'r') as f:
        temp_data_id = json.load(f)

    for i in range(len(temp_data_id)):
        temp_data_id[i]["id"] = index_counter
        index_counter += 1

    with open(filename,'w') as fi:
        json.dump(temp_data_id,fi,indent=4)

#Get Tasks from Json file:
def get_tasks():
    with open(filename,'r') as f:
        task_items = []
        temp_data_get = json.load(f)
    
    if temp_data_get != []:
        for i in range(len(temp_data_get)):
            task_items = ([temp_data_get[i]['id'],temp_data_get[i]['task'],temp_data_get[i]['date'],temp_data_get[i]['time'],temp_data_get[i]['complete state']])
        return task_items
    else:
        pass

#if checkbox is active
def task_complete(task_id):
    with open (filename,'r') as f:
        temp_data_bool_c = json.load(f)
    
    for items in temp_data_bool_c:
        if items['id'] == task_id:
            temp_data_bool_c[task_id]['complete state'] = True

    with open(filename,'w')as fi:
        json.dump(temp_data_bool_c,fi,indent=4)


#if checkobox is not active
def task_incomplete(task_id):
    with open (filename,'r') as f:
        temp_data_bool_inc = json.load(f)
    
    for items in temp_data_bool_inc:
        if items['id'] == task_id:
            temp_data_bool_inc[task_id]['complete state'] = False

    with open(filename,'w')as fi:
        json.dump(temp_data_bool_inc,fi,indent=4)

    return temp_data_bool_inc[task_id]['task']
get_tasks()