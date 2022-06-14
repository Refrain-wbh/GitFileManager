
<template>
  <el-container style="height: 600px; border: 0px solid #eee">
    <el-header style="text-align: left; font-size: 12px">
    
    <el-button type="primary" icon="el-icon-upload" circle @click="dialogVisible = true"></el-button>
    <el-dialog
      title="上传文件"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose">
      <el-upload
        class="upload-demo"
        action="/upload/"
        :headers="{'X-CSRFToken': this.csrf_token}"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :before-remove="beforeRemove"
        multiple
        :on-exceed="handleExceed"
        :file-list="fileList">
        <el-button size="small" type="primary">点击上传</el-button>
        <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
      </el-upload>

      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
      </span>
    </el-dialog>

    </el-header>
    <el-container>
      <el-aside width="500px">
          <el-tree 
            :data="fileTree" 
            node-key="id"
            ref="fileTree" 
            empty-text=""
            :props="defaultProps" 
            @node-expand="(data,node,t)=>{data.isopen=true}"
            @node-click="handleNodeClick"
            @node-collapse="(data,node,t)=>{data.isopen=false}">
            <span class="custom-tree-node" slot-scope="{ node, data }">
              <!--font-awesome-icon icon="fa-brands fa-java" /-->
              <i v-if="data.children && !data.isopen" class="el-icon-folder"></i>
              <i v-else-if="data.children && data.isopen" class="el-icon-folder-opened"></i>
              <i v-else class="el-icon-document"></i>
              <span>{{ node.label }}</span>
            </span>
          </el-tree>
       
      </el-aside>
      <el-container>
        <el-header style="text-align: right; font-size: 12px">
        </el-header>
        <el-main>

        </el-main>
      </el-container>
    </el-container>
  </el-container>


</template>
 
<script>
  export default {
    data() {
      const store_id = this.$route.query.store_id;
      return {
        dialogVisible: false,
        store_id:store_id,
        csrf_token:0,
        fortest:{store_id:store_id},
        fileTree:[],
        fileList: [{name: 'food.jpeg', url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'}, {name: 'food2.jpeg', url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'}],
      defaultProps: {
        children: 'children',
        label: 'label'
        }
      };
    },
    created (){
      this.getStoreContent();
      this.getToken();
    },
    methods: {
      getStoreContent(){
        this.axios.get('storeContent/',{params:{store_id:this.store_id}})
        .then((response)=>{
            console.log('???',response.data.fileTree)
            this.fileTree = response.data.fileTree
        })
        .catch(function(error){
            console.log(error)
        })
      },
      handleNodeClick(data) {
        if (data.children)
        {
          data.isopen = !data.isopen
        }
        console.log(data);
      },
      handleClose(done) {
        this.$confirm('确认关闭？')
          .then(_ => {
            done();
          })
          .catch(_ => {});
      },
      getToken(){
        this.axios.get('getToken/')
        .then((response)=>{
            this.csrf_token = response.data.csrf_token
            console.log("this.csrf_token",this.csrf_token)
        })
        .catch(function(error){
            console.log(error)
        })
      },
      handleRemove(file, fileList) {
        console.log(file, fileList);
      },
      handlePreview(file) {
        console.log(file);
      },
      handleExceed(files, fileList) {
        this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
      },
      beforeRemove(file, fileList) {
        return this.$confirm(`确定移除 ${ file.name }？`);
      },
      handleNodeClick(data,checked,indeterminate) {
        console.log('check',data)
      }
    }
  };

</script>
 
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.box{
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}
.el-header {
  background-color: #B3C0D1;
  color: #333;
  line-height: 60px;
}

.el-aside {
  
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
  color: rgb(192, 88, 88);
  background-color: rgb(255, 255, 255);
}
</style>
