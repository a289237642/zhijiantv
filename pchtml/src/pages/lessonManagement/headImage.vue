<template>
  <div id="headImage">
    <div class="h1">头像库</div>
    <div class="header">
      <Button class="newbtn zhijian-new-btn" type="primary" @click="withUpload">上传头像</Button>
    </div>
    <input type="file" id="inputFile" accept="image/gif, image/jpeg, image/png, image/jpg" style="display:none" @change="onUpload($event)">
    <div class="headImage_list">
      <div v-for="(item,index) in imgList">
        <img :src="item.pic">
        <div @click="deleteImg(item.image_id)">
          <i class="iconfont icon-delete"></i>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    name: "headImage",
    data() {
      return {
        imgList: []
      }
    },
    methods: {
      withUpload() {
        document.getElementById('inputFile').click()
      },
      onUpload(e){
        let that = this;
        let files = e.target.files || e.dataTransfer.files;
        if (!files.length) return;
        let type = e.target.files[0].type;
        if (/^image/.test(type)){
          var reads= new FileReader();
          reads.readAsDataURL(files[0]);
          reads.onload = function () {
            let fd = new FormData()
            fd.append('data', this.result)
            let config = {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            }
            that.$post(that.PATH.UPUPUP,{
              type:'jpg',
              data:this.result
            }).then(
              res => {
                console.log(res)
                if(res.data.errno=== 0) {
                  that.getList()
                }else {
                  that.$Modal.error({
                    title:'提示',
                    content: res.data.errmsg
                  })
                }
              },
              error => {
                that.$Modal.error({
                  title:'提示',
                  content:error.data.msg
                })
              })
          }
        }
      },
      getList() {
        this.$post(this.PATH.IMAGE_STORE,{
          pagesize: 100000,
        }).then(res=>{
          console.log(res)
          if (res.data.errno === 0) {
            this.imgList = res.data.image_list
          }
        })
      },
      deleteImg(id) {
         this.$post(this.PATH.DEL_IMAGE,{
           image_id: id
         }).then(res=>{
           if (res.data.errno === 0) {
             this.$Modal.success({
               title: "提示",
               content: '删除成功',
             })
             this.getList()
           } else {
             this.$Modal.error({
               title: "提示",
               content: res.data.errmsg,
             })
           }
         })
      }
    },

    created() {
      this.getList()
    }
  };
</script>
<style lang="scss" scoped>
  #headImage {
    height: 100%;
    padding: 20px 20px 100px 20px;
    width: 100%;
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    .h1 {
      font-size: 22px;
      color: #808080;
      margin-bottom: 20px;
    }
  }
  .header {
    margin-top: 20px;
    text-align: right;
    margin-bottom: 30px;
    position: relative;
    height: 42px;
    //新增按钮
    .newbtn {
      float: right;
      text-align: left;
      margin-left: 10px;
    }
    .zhijian-new-btn {
      height: 32px;
      line-height: 12px;
    }
  }
  .headImage_list{
    display: flex;
    flex-wrap: wrap;
    align-items: flex-start;
    align-content: flex-start;
    margin-bottom: -20px;
    >div{
      width: 80px;
      height: 80px;
      margin: 0 20px 20px 0;
      position: relative;
      &:hover{
        >div{
          display: block;
        }
        &:after{
          display: block;
          content: '';
          position: absolute;
          width: 100%;
          height: 100%;
          background-color: #000;
          opacity: .6;
          top: 0;
          left: 0;
        }
      }
      >div{
        display: none;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%,-50%);
        z-index: 9;
        >i{
          color: #c2a450;
          cursor: pointer;
        }
      }
      >img{
        width: 100%;
        height: 100%;
      }
    }
  }
</style>
