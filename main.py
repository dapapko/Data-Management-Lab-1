from db import Table, Column
if __name__ == '__main__':
    columns = [
        Column(name="name", unique=False, type='str'),
        Column(name="number", unique=True, type='str'),
        Column(name="age", unique=False, type='int'),
    ]

    path = "/root/dblab"
    tbl = Table(dir=path, columns=columns)
    #tbl.init_db()
    #entry = {"age":12, "name":"George", "number":"79006789123"}
    #tbl.insert(entry)
    #second_entry = {"age":35, "name":"George", "number":"88005553535"}
    #tbl.insert(second_entry)
    #selected = tbl.fast_search_by_field("79006789123", "number")
    #print(selected)
    #tbl.insert(entry) #Unique number constraint violation test
    #tbl.remove_by_id("e2861799-565a-4e5d-b43d-0804d85d3483")
    #print(tbl.search_by_field_value("name", "George"))
    #tbl.remove_by_value("name", "George")
    #tbl.update("3c73b249-3baf-486e-9b87-459154d38d4b", {"age":71, "name":"Jack", "number":"79006789123"})
    #tbl.cleanup()
    #tbl.delete_all()
    #tbl.backup()
    #tbl.restore()
    tbl.to_csv()
