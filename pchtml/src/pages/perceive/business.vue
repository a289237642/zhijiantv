<template>
  <div id="business">
    <div class="h1">商学院banner设置</div>
    <input type="file" id="inputFile" accept="image/gif, image/jpeg, image/png, image/jpg" style="display:none" @change="onUpload($event)">
    <div class="schoolManagement_container">
      <div>
        <div class="schoolManagement_part" v-for="(item,index) in banners">
          <div>{{index+1}}</div>
          <div @click="withUpload(index)">
            <img :src="item.pic" v-if="item.pic !== ''">
          </div>
          <div>
            <Input type="text" v-model="item.jump_url" placeholder="请输入跳转路径" :value="item.jump_url" />
            <Input type="text" v-model="item.appid" placeholder="请输入appid" :value="item.appid"/>
          </div>
          <div>
            <Button class=" zhijian-new-btn" type="primary" @click="submitInfo(item)">提交</Button>
          </div>
        </div>
      </div>
      <div>
        <img src="@/assets/images/simple.png">
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "business",
    data() {
      return {
        banners: null,
        bannerIndex: null
      }
    },
    created() {
      this.getInfo()
    },
    methods: {
      getInfo() {
        this.$post(this.PATH.GET_PC_BUSSINESS,{}).then(res=>{
          console.log(res)
          if (res.data.errno === 0) {
            this.banners = res.data.data
          } else {
            this.$Modal.error({
              title:'提示',
              content:res.data.errmsg
            })
          }
        })
      },
      submitInfo(data) {
        this.$post(this.PATH.CREATE_BUSSINESS,data).then(res=>{
          if (res.data.errno === 0) {
            this.getInfo()
            this.$Modal.error({
              title:'提示',
              content:'提交成功！'
            })
          } else {
            this.$Modal.error({
              title:'提示',
              content:res.data.errmsg
            })
          }
        })
      },
      withUpload(index) {
        this.bannerIndex = index
        document.getElementById('inputFile').click()
      },
      //上传图片
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
            that.$post('/api/v1_0/uploadimage',{
              type:'jpg',
              data:this.result
            }).then(
              res => {
                console.log(res)
                if(res.data.status=="0") {
                  that.banners[that.bannerIndex].pic = res.data.url
                }else {
                  that.$Modal.error({
                    title:'提示',
                    content: res.data.msg
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
      }
    }
  }
</script>

<style lang="scss" scoped>
  #business{
    height: 100%;
    padding: 20px;
    width: 100%;
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    .h1 {
      font-size: 22px;
      color: #808080;
      margin-bottom: 20px;
    }
  }
  .schoolManagement_head{
    width: 100%;
    margin: 0 auto 30px auto;
    line-height: 32px;
    font-size: 16px;
    &:after{
      content: '';
      display: block;
      clear: both;
    }
    >div{
      &:after{
        content: '';
        display: block;
        clear: both;
      }
      margin-bottom: 10px;
      >label{
        float: left;
        margin-right: 40px;
      }
      >div{
        float: left;
        width: 60%;
      }
    }
  }
  .schoolManagement_part{
    width: 100%;
    margin: 0 auto 30px auto;
    &:after{
      content: '';
      display: block;
      clear: both;
    }
    >div{
      float: left;
      line-height: 40px;
      font-size: 18px;
      &:not(:last-of-type) {
        margin-right: 20px;
      }
      &:nth-of-type(2) {
        width: 80px;
        height: 80px;
        border: 1px dashed #333;
        cursor: pointer;
        position: relative;
        >img{
          width: 105%;
          height: 105%;
          position: absolute;
          z-index: 999;
          left: -1px;
          top: -1px;
          background-color: #f0f0f0;
        }
        &:before{
          position: absolute;
          content: '';
          display: block;
          width: 10px;
          height: 2px;
          background-color: #333;
          top: 50%;
          left: 50%;
          transform: translate(-50%,-50%);
        }
        &:after{
          position: absolute;
          content: '';
          display: block;
          width: 2px;
          height: 10px;
          background-color: #333;
          top: 50%;
          left: 50%;
          transform: translate(-50%,-50%);
        }
      }
      &:nth-of-type(3) {
        width: 60%;
      }
    }
  }
  .newbtn{
    margin-bottom: 60px;
  }
  .schoolManagement_btn{
    margin: 0 auto;
    width: 20%;
    text-align: center;
  }
  .ivu-switch-checked{
    background-color: #ffc639;
    border-color: #ffc639;
  }
  .schoolManagement_container{
    width: 90%;
    margin: 20px auto auto auto;
    &:after{
      content: '';
      display: block;
      clear: both;
    }
    >div{
      &:nth-of-type(1) {
        width: 70%;
        float: left;
      }
      &:nth-of-type(2) {
        width: 30%;
        float: right;
        >img{
          width: 100%;
        }
      }
    }
  }
</style>
