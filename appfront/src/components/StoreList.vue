<template>
  <div class="box">
    <div>
      <el-input v-model="input" placeholder="仓库名" style="width:350px"></el-input>
      <el-button type="success" @click="addStore">新建仓库</el-button>
    </div>
    <el-table
      :data="tableData"
      style="width: 800px;">
      <el-table-column
        prop="name"
        label="仓库名"
        width="450">
      </el-table-column>
      
      <el-table-column
        prop="time"
        label="创建时间"
        width="180">
      </el-table-column>

      <el-table-column label="操作">
      <template slot-scope="scope">
        <el-button
          size="mini"
          @click="enterStore(scope.row.id)">进入</el-button>
        <el-button
          size="mini"
          type="danger"
          @click="deleteStore(scope.row.id)">删除</el-button>
      </template>
    </el-table-column>
    </el-table>
  </div>
</template>
 
<script>
export default {
  name: 'FileList',
  data () {
    return {
      input: '',
      tableData: []
    }
  },
  created () {
    this.showStore()
  },
  methods: {
    showStore(){
        this.axios.get('storelist/')
        .then((response)=>{
            console.log(response.data.storelist)
            this.tableData = response.data.storelist
        })
        .catch(function(error){
            console.log(error)
        })
    },
    addStore(){
        this.axios.get('addStore/',{params:{store_name:this.input}})
        .then((response) => {
            this.showStore()
        })
        .catch(function (error) {
            console.log(error);
        });
    },
    deleteStore(store_id){
      this.axios.get('deleteStore/',{params:{store_id:store_id}})
      .then((response)=>{
        this.showStore()
      })
    },
    enterStore(store_id){
        this.$router.push({
            name:'StoreContent',
            query:{
                store_id:store_id
            }
        })
    },
  }
}
</script>
 
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.box{
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}
</style>
