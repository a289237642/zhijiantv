<template>
  <div id="upload">
    <div class="upload_content">
      <div class="header">
        <Icon custom="i-icon location_icon" />
        <span>上传视频</span>
        <div class="btn_box">
          <Button class="upload_btn" @click="modalChange('upload')">上传</Button>
          <Button class="cancel" @click="modalChange('cancel')">取消</Button>
        </div>
      </div>
      <div class="main">
        <ul>
          <li class="classify_item">
            <span>
              <Icon custom="i-icon star" />
              分类名称：
            </span>
            <Select v-model="classifyName">
              <Option v-for="item in className" :value="item.id" :key="item.id">{{ item.title }}</Option>
            </Select>
          </li>
          <li class="video_item">
            <span>
              <Icon custom="i-icon star" />
              视频名称：
            </span>
            <textarea name="" id="" cols="30" rows="10" v-model="videoName" class="video_name" placeholder="输入视频名称"></textarea>
          </li>
          <li class="add_video_item">
            <span>
              <Icon custom="i-icon star" />
              添加视频：
            </span>
               <Upload   
              multiple
              type="drag"
              :on-success='upVideoSuccess'
              action="https://upload.qiniup.com"
              :data="{token:videoToken,key:videokey}"
              :on-format-error="handleFormatError">
              <Button icon="ios-cloud-upload-outline" @click="getToken">添加视频文件</Button>
            </Upload>
          </li>
          <li class="add_img_item">
            <span>
              <Icon custom="i-icon star" />
              添加封面：
            </span>
            <Upload
              multiple
              type="drag"
              :on-success='upSuccess'
              :format="['jpg','jpeg','png']"
              :on-format-error="handleFormatError"
              action=" https://bjzhijian.max-tv.net.cn/api/tv1_0/up_tp_oss">
              <div class="upload_img">
                <Icon custom="i-icon upload_icon" />
                <p>上传图片</p>
              </div>
            </Upload>
          </li>
        </ul>
      </div>
      <div class="modal">
        <Modal
          v-model="modal.modalCancel"
          title="提示"
          @on-ok="asyncOK">
          <p>{{modal.txtInfo}}</p>
        </Modal>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'uploadVideo',
  data(){
    return {
      classifyName: '',// 传的分类名称
      videoName: '',//视频名称
      className:'',//获取的所有分类名称
      imgUrl:'', // 上传图片后获取的地址
      url:'',
      play_times:'',
      modal: {
        modalCancel: false,
        txtInfo: '您编辑的内容尚未保存，确定取消上传视频吗？',
        buttonFrom: 'cancel' /*另一个是upload来源*/
      },
      onlyCode:'',//为了传唯一的token给后端
      videoToken:'', // 获取到传回来的token
      videokey:'',
      countTime:''
    }
  },
  mounted(){
    this.upVideoName()
    this.productNum()
  },
  methods: {
    getToken(){
      this.$http.post(this.URL+this.PATH.getosstoken,{key:this.onlyCode}).then(res=>{
        if(res.data.errno == 0){
          this.videoToken = res.data.token;
          this.videokey = res.data.key;
        }else{
              this.$Modal.error({
                title: '提示',
                content: res.data.errmsg
            })
          }
      })
    },
    countTimes(s){
          /**
         * 将秒转换为 分:秒
         * s int 秒数
        */
        //计算分钟
        //算法：将秒数除以60，然后下舍入，既得到分钟数
        var h;
        h  =   Math.floor(s/60);
        //计算秒
        //算法：取得秒%60的余数，既得到秒数
        s  =   s%60;
        //将变量转换为字符串
        h    +=    '';
        s    +=    '';
        //如果只有一位数，前面增加一个0
        h  =   (h.length==1)?'0'+h:h;
        s  =   (s.length==1)?'0'+s:s;
        // let i = s.indexOf('.');
        // let s1= s.slice(0,i)
        return h+':'+s;
    },
    productNum(){
       var result = [];
      for (var i = 0; i < 4; i++) {
          var ranNum = Math.ceil(Math.random() * 25); //生成一个0到25的数字
          //大写字母'A'的ASCII是65,A~Z的ASCII码就是65 + 0~25;然后调用String.fromCharCode()传入ASCII值返回相应的字符并push进数组里
          result.push(String.fromCharCode(65 + ranNum))
          this.onlyCode = result + (new Date()).valueOf().toString() //为了传唯一的token给后端
        }
    },
    // 上传视频
    upVideoSuccess(response, file){
      if(response.key){
        let key = response.key;
        this.url =`http://prjkmnaf0.bkt.clouddn.com/${key}` ;
        if(this.url){
            this.$http.post(this.URL+this.PATH.getFileTime,{key:key}).then(res=>{
              if(res.data.errno == 0){
                // 获取到转化后的视频时间
                  this.countTime = res.data.play_times
              }else{
                  this.$Modal.error({
                    title: '提示',
                    content: '上传失败'
                })  
              }
            })
          }
      }
    },
    // 上传图片
    upSuccess(response,file){
      if(response.errno == 0){
        this.imgUrl = response.url
      }else{
          this.$Modal.error({
            title: '提示',
            content: '上传失败'
        })  
      }
    },
    // 获取分类名称
    upVideoName(){
      this.$http.post(this.URL+this.PATH.upVideoName).then(res=>{
        if(res.data.errno == 0){
          this.className = res.data.info_list
        }else{
              this.$Modal.error({
                title: '提示',
                content: res.data.errmsg
            })
          }
      })
    },
    handleFormatError(){
       this.$Notice.warning({
          title: '文件格式不正确',
      });
    },
    resetConcent(){
        this.classifyName =  '',// 传的分类名称
        this.videoName = '',//视频名称
        this.imgUrl='', // 上传图片后获取的地址
        this.url='',
        this.play_times=''
    },
    modalChange(txt){
      if(txt == 'upload'){
        this.modal.txtInfo = '确定要上传吗？';
        this.modal.buttonFrom = 'upload';
      }else{
        this.modal.txtInfo = '您编辑的内容尚未保存，确定取消上传视频吗？';
        this.modal.buttonFrom = 'cancel';
      }
      this.modal.modalCancel = true;
    },
 
    asyncOK () {
      if(this.modal.buttonFrom == 'cancel'){
       this.resetConcent()
      }
      if(this.modal.buttonFrom == 'upload'){
        if(this.classifyName == ''){
            this.$Modal.error({
            title: '提示',
            content: '请选择分类'
          })
           return false
        }
        else if(this.videoName == ''){
            this.$Modal.error({
            title: '提示',
            content: '请填写视频名称'
          })
            return false
        }else if(this.imgUrl == ''){
            this.$Modal.error({
            title: '提示',
            content: '请添加视频封面'
          })
           return false
        }else if(this.url == ''){
            this.$Modal.error({
            title: '提示',
            content: '请添加视频'
          })
           return false
        }else{
             let data = {
                vtype:this.classifyName,
                title:this.videoName,
                pic_url:this.imgUrl,
                url:this.url,
                play_times:this.countTime,
            }
            this.$http.post(this.URL+ this.PATH.viedeoNew,data).then(res=>{
              if(res.data.errno == 0){
                this.$Modal.success({
                   title: '提示',
                  content: '上传成功'
                })
                this.resetConcent()
              }else{
                  this.$Modal.error({
                    title: '提示',
                    content: res.data.errmsg
                })
              }
            })
         }
      }
    },
  }
}
</script>

<style lang="less">
  @base: #6461FF;
  #upload{
    width: 100%;
    height: 100%;
  }
  .upload_content{
    height: 100%;
    background: #fff;
    box-shadow: 0 2px 4px 5px rgba(145,136,212,0.07);
    border-radius: 8px;
    padding-top: 22px;
    >div{
      text-align: left;
    }
    .header{
      padding-left: 25px;
      border-bottom: 1px solid #eee;
      padding-bottom: 18px;
      .location_icon{
        width: 17px;
        height: 21px;
        background: url("../../assets/img/location.png") no-repeat left top;
        background-size: 17px 21px;
        /*vertical-align: sub;*/
        position: relative;
        top: -5px;
      }
      >span{
        font-size: 24px;
        line-height: 33px;
        color: @base;
        margin-left: 7px;
      }
      .btn_box{
        float: right;
        margin-right: 40px;
        position: relative;
        top: -6px;
        button{
          width: 110px;
          height: 44px;
          font-size: 20px;
          border: none;
          border-radius: 0;
        }
        .upload_btn{
          color: #fff;
          background-image: linear-gradient(90deg, #535AFF 0%, #747DFF 100%);
          box-shadow: 0 2px 5px 0 #545AFF;
        }
        .cancel{
          background: #F2F2F2;
          box-shadow: 0 2px 5px 0 #C7C7C7;
          color: #999;
          margin-left: 19px;
        }
      }
    }
    .main{
      padding: 18px 0 0 19px;
      font-size: 17px;
      color: #5D5BBC;
      ul{list-style: none;}
      li{
        &:not(:first-child){
          margin-top: 17px;
        }
        >span{
          margin-right: 25px;
          .star{
            width: 13px;
            height: 13px;
            background: url("../../assets/img/star.png") no-repeat left top;
            background-size: 13px 13px;
            vertical-align: baseline;
          }
        }
        &.classify_item{
          .ivu-select{
            width: auto;
            .ivu-select-selection{
              display: inline-block;
              width: 330px;
              height: 35px;
              border: 1px solid lighten(#B4C7E0, 10%);
              border-radius: 0;
              .ivu-select-placeholder{
                color: #ddd;
                line-height: 35px;
              }
              .ivu-icon-ios-arrow-down{
                right: 7px;
                top: 8px;
                &::before{
                  content: '\F33D';
                  font-size: 19px;
                  color: @base;
                }
              }
              .ivu-select-arrow{
                transform: translateY(0);
              }
            }
            .ivu-select-dropdown{
              width: 330px;
              min-width: 300px;
            }
          }
        }
        &.video_item{
          .video_name{
            width: 272px;
            height: 67px;
            border: 1px solid lighten(#B4C7E0, 10%);
            vertical-align: top;
            padding: 5px 0 0 8px;
            outline-color: #d9e9fc;
            outline-width: 4px;
          }
          ::-webkit-input-placeholder { /* WebKit browsers */
            font-size: 14px;
            color: #ddd;
          }
        }
        &.add_video_item{
          .ivu-upload{
            display: inline-block;
            height: 35px;
            .ivu-btn{
              border: 1px solid lighten(#B4C7E0, 10%);
              border-radius: 0;
              color: #ddd;
              padding: 5px 8px 6px;
              .ivu-icon-ios-cloud-upload-outline:before{
                content: '+';
                position: relative;
                top: -2px;
              }
            }
          }
        }
        &.add_img_item{
          .ivu-upload{
            display: inline-block;
            width: 310px;
            height: 180px;
            vertical-align: top;
            background: lighten(#D8D8D8, 10%);
            border: none;
            border-radius: 0;
            color: #ddd;
            font-size: 20px;
            .upload_img{
              position: relative;
              top: 50%;
              transform: translateY(-50%);
              .upload_icon{
                width: 55px;
                height: 55px;
                background: url("../../assets/img/upload_icon.png") no-repeat center center;
                background-size: 47px 37px;
                margin-bottom: 6px;
              }
            }
          }
        }
      }

    }
  }
  .ivu-upload-drag{
    border: none;
  }
 .ivu-upload .ivu-btn{
   border: 1px dashed #d8e2ef !important;
 }
</style>
