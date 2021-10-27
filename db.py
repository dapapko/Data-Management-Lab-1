import json
import os
import shutil
import uuid
from typing import List
import hashlib


class Column:
    name: str
    unique: bool
    type: str

    def __init__(self, name, unique, type):
        self.name = name
        self.unique = unique
        self.type = type


class Table:
    columns: List[Column]
    dir: str

    def __init__(self, dir, columns):
        self.dir = dir
        self.columns = columns

    def exists_by_key(self, k):
        return os.path.exists(f"{self.dir}/{k}")

    def create_table(self):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir, exist_ok=True)
        for column in self.columns:
            with open(f"{self.dir}/{column.name}.col", "wb") as col:
                pass

    def get_by_id(self, id):
        try:
            with open(f"{self.dir}/entries/{id}", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    def insert(self, record: dict, identifier=None):
        identif = identifier if identifier is not None else str(uuid.uuid4())
        for column in self.columns:
            if column.unique:
                hashed = hashlib.sha256(record[column.name].encode('utf-8')).hexdigest()
                path = f"{self.dir}/fastcols/{column.name}/{hashed}"
                try:
                    with open(path, 'r') as f:
                        id = f.readline().rstrip()
                        if os.path.exists(f"{self.dir}/entries/{id}"):
                            raise ValueError(f"Unique constraint violation on field {column.name}")
                except FileNotFoundError:
                    pass
                with open(path, "w") as f:
                    f.write(identif)
        with open(f"{self.dir}/entries/{identif}", "w") as entry:
            json.dump(record, entry)

    def remove_by_id(self, id):
        path = f"{self.dir}/entries/{id}"
        os.remove(path)

    def update(self, id, entry):
        self.remove_by_id(id)
        self.insert(entry, id)

    def remove_by_value(self, column, value):
        entries = os.listdir(f"{self.dir}/entries")
        for directory in entries:
            path = f"{self.dir}/entries/{directory}"
            with open(path, "r") as f:
                entry = json.load(f)
                if entry[column] == value:
                    os.remove(path)

    def search_by_field_condition(self, column: str, condition):
        filtered = []
        entries = os.listdir(f"{self.dir}/entries")
        for dir in entries:
            with open(f"{self.dir}/entries/{dir}", "rt") as f:
                entry = json.load(f)
                if condition(entry[column]): filtered.append(entry)
        return filtered

    def search_by_field_value(self, column: str, value):
        filtered = []
        entries = os.listdir(f"{self.dir}/entries")
        for dir in entries:
            with open(f"{self.dir}/entries/{dir}", "rt") as f:
                entry = json.load(f)
                if entry[column] == value: filtered.append(entry)
        return filtered

    def fast_search_by_field(self, value, colname):
        hash = hashlib.sha256(value.encode('utf-8')).hexdigest()
        try:
            with open(f"{self.dir}/fastcols/{colname}/{hash}", 'r') as f:
                identifier = f.readline().rstrip()
                print(identifier)
                return self.get_by_id(identifier)
        except FileNotFoundError:
            return None

    def cleanup(self):
        entries = os.listdir(f"{self.dir}/entries")
        for entry in entries:
            os.remove(f"{self.dir}/entries/{entry}")
        for col in self.columns:
            if not col.unique: continue
            path = f"{self.dir}/fastcols/{col.name}/"
            shutil.rmtree(path)
            os.mkdir(path)

    def delete_all(self):
        shutil.rmtree(f"{self.dir}/fastcols")
        shutil.rmtree(f"{self.dir}/entries")

    def init_db(self):
        os.makedirs(f"{self.dir}/entries")
        for col in self.columns:
            if not col.unique: continue
            path = f"{self.dir}/fastcols/{col.name}"
            os.makedirs(path)

    def backup(self):
        archive_name = os.path.expanduser(os.path.join('~', 'backup'))
        shutil.make_archive(archive_name, 'gztar', self.dir)

    def restore(self):
        self.delete_all()
        archive_name = os.path.expanduser(os.path.join('~', 'backup'))
        shutil.unpack_archive(archive_name, self.dir)

    def to_csv(self):
        csv = ""
        entries = os.listdir(f"{self.dir}/entries")
        for entry in entries:
            path = f"{self.dir}/entries/{entry}"
            with open(path, "r") as f:
                e = json.load(f)
                listvals = list(map(str, list(e.values())))
                s = ",".join(listvals) + "\n"
                csv += s
        with open("dump.csv", "w") as dump:
            dump.write(csv)
