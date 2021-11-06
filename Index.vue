<template>
  <q-page class="flex flex-center">

 <q-splitter
      v-model="splitterModel"
      style="height: 550px"
    >

      <template v-slot:before>
        <q-tabs
          v-model="tab"
          vertical
          class="text-teal"
        >
          <q-tab name="list" icon="mail" label="List" />
          <q-tab name="update" icon="alarm" label="Update" />
          <q-tab name="create" icon="movie" label="Create" />
           <q-tab name="delete" icon="movie" label="Delete" />
           <q-tab name="show" label="Show" />
             <q-tab name="operations" icon="movie" label="Operations" />
        </q-tabs>
      </template>

      <template v-slot:after>
        <q-tab-panels
          v-model="tab"
          animated
          swipeable
          vertical
          transition-prev="jump-up"
          transition-next="jump-up"
        >
          <q-tab-panel name="create">
            <div class="text-h4 q-mb-md">Create</div>
           <q-input v-model="newEntity.name" label="Name"></q-input>
            <q-input v-model="newEntity.number" label="Number"></q-input>
            <q-input v-model="newEntity.age" label="Age" type="number"></q-input>
            <q-btn @click="create">Add record</q-btn>
          </q-tab-panel>

          <q-tab-panel name="update">
            <div class="text-h4 q-mb-md">Update</div>
            <q-input v-model="updateUUID" label="UUID to update"></q-input>
            <q-input v-model="entityForm.name" label="Name"></q-input>
            <q-input v-model="entityForm.number" label="Number"></q-input>
            <q-input v-model="entityForm.age" label="Age" type="number"></q-input>
             <q-btn @click="update">Update record</q-btn>
          </q-tab-panel>

           <q-tab-panel name="show">
            <div class="text-h4 q-mb-md">Show</div>
            <q-input v-model="UUIDToSearch" label="Enter UUID"></q-input>
            <q-btn @click="searchByUUID" label="Search by UUID"></q-btn>
            <p v-if="entityForm.age">{{entityForm.age}}</p>
            <p v-if="entityForm.name">{{entityForm.name}}</p>
            <p v-if="entityForm.number">{{entityForm.number}}</p>
          </q-tab-panel>

          <q-tab-panel name="list">
            <div class="text-h4 q-mb-md">List (search by field)</div>
            <q-form>
                 <q-select :options="['name', 'age', 'number']" v-model="currentField" label="Select field"></q-select>
<q-input v-model="criteria" label="Field value" v-if="currentField === 'name' || currentField === 'number'"></q-input>
      <q-input v-model="criteria" label="Field value" v-else type="number"></q-input>
<q-btn @click="delete" label="Delete record"></q-btn>
            </q-form>
           <q-table
      title="Records"
      :rows="entries"
      :columns="columns"
    />
          </q-tab-panel>

           <q-tab-panel name="delete">
            <div class="text-h4 q-mb-md">Remove</div>
              <q-card class="my-card text-white">
      <q-card-section>
        <div class="text-h6">Remove by UUID</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
      <q-input v-model="UUIDToDelete" label="UUID"></q-input>
<q-btn @click="deleteByUuid" label="Delete record by UUID"></q-btn>
      </q-card-section>
    </q-card>

    <q-card class="my-card text-white">
      <q-card-section>
        <div class="text-h6">Remove by field name</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <q-select :options="['name', 'age', 'number']" v-model="fieldToDelete"></q-select>
<q-input v-model="criteriaToDelete" label="Field value" v-if="fieldToDelete === 'name' || fieldToDelete === 'number'"></q-input>
      <q-input v-model="criteriaToDelete" label="Field value" v-else type="number"></q-input>
<q-btn @click="delete" label="Delete record"></q-btn>
      </q-card-section>
    </q-card>

    
           
          </q-tab-panel>

           <q-tab-panel name="operations">
            <div class="text-h4 q-mb-md">Operations</div>
            <q-btn color="primary" label="Init DB" @click="init" />
           <q-btn color="primary" label="Delete all records" @click="deleteall" />
           <q-btn color="primary" label="Clean up" @click="cleanup"  />
            <q-btn color="primary" label="Backup" @click="backup"  />
            <q-btn color="primary" label="Restore" @click="restore"  />
            <q-btn color="primary" label="Dump to CSV" @click="dump"  />
          </q-tab-panel>
        </q-tab-panels>
      </template>

    </q-splitter>


  </q-page>
</template>

<script>
import axios from "axios"
import { ref } from 'vue'
export default {
    name:"Index",
    methods:{
        deleteByUuid(){
            axios.get(`http://82.146.45.43:5000/remove/${this.UUIDToDelete}`);
        },
        delete(){
            let query = {column:this.fieldToDelete, value:this.criteriaToDelete}
            axios.post('http://82.146.45.43:5000/remove', JSON.stringify(query))
        },
        searchBy(){
            let query = {column:this.currentField, value:this.criteria}
            let url = this.currentField === 'number' ? 'http://82.146.45.43:5000/fastbyfield' : 'http://82.146.45.43:5000/byfield';
            axios.post(url, JSON.stringify(query)).then((resp)=>this.entries = resp.data);
        },
        getByUUID(){
            
            let url =  `http://82.146.45.43:5000/byid/${this.UUIDToSearch}`;
            axios.get(url, JSON.stringify(query)).then((resp) => this.entityForm = resp.data);
        },
        dump(){
            let url = 'http://82.146.45.43:5000/dump'
            axios.get(url)
        },
        backup(){
            let url = 'http://82.146.45.43:5000/backup'
            axios.get(url)
        },
        create(){
            let url = 'http://82.146.45.43:5000/insert'
            axios.post(url, newEntity)
        },
        update(){
            let url = `http://82.146.45.43:5000/update/${this.updateUUID}`
            axios.post(url, newEntity)
        },
        restore(){
            let url = 'http://82.146.45.43:5000/restore'
            axios.get(url)
        },
        init(){
            let url = 'http://82.146.45.43:5000/init'
            axios.get(url)
        },
         cleanup(){
            let url = 'http://82.146.45.43:5000/cleanup'
            axios.get(url)
        },
         deleteall(){
            let url = 'http://82.146.45.43:5000/deleteall'
            axios.get(url)
        }

    },
    data() {
        return {
            splitterModel:ref(20),
            updateUUID:undefined,
            tab:ref('create'),
            entityForm:{},
            newEntity:{name:undefined, number:undefined, age:0},
            entries:[],
            columns:[],
            currentField:undefined,
            criteria:undefined,
            fieldToDelete:undefined,
            UUIDToDelete:undefined,
            criteriaToDelete:undefined,
            }
            },
    mounted(){
        axios.get('http://82.146.45.43:5000/columns').then( (resp) => {
            this.columns = resp.data
            });
        axios.get('http://82.146.45.43:5000/all').then( (resp) => {
            this.entries = resp.data
            });
        }}
</script>
