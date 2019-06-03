<template>
    <div id="bannerManagement">
       <div class="h1">签到海报管理</div>
    
         <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="100" class="edit-form">
                     <FormItem label="状态" prop="is_show">
                        <RadioGroup v-model="formValidate.is_show">
                            <Radio label="1">启用</Radio>
                            <Radio label="0">禁用</Radio>
                        </RadioGroup>
                    </FormItem>
                     <FormItem label="海报图: " prop="sort">
                          <div class="h5ImgBox" v-if="isShow">
                            <img :src="h5Img" style="width:98px;height:98px;">
                        </div>
                        <div >
                            <label for="inputFile" class="button">
                            <span class="upload__select">点击上传图片</span>
                            <input type="file" id="inputFile" accept="image/gif, image/jpeg, image/png, image/jpg" style="display:none" @change="onUpload">
                            </label>
                        </div>
                    </FormItem>
                     <FormItem label="跳转路径：" prop="path">
                        <Input v-model="formValidate.path" placeholder="跳转路径"></Input>
                    </FormItem>
                <FormItem label="起止日期：" prop="">
                      <DatePicker v-model="startDate" type="date" placeholder="开始日期" style="width: 120px" @on-change="getStart"></DatePicker>
                至
                <DatePicker type="date" v-model="endDate" placeholder="结束日期" style="width:120px;"  @on-change="getEnd"></DatePicker>   
                    </FormItem>
               
                </Form>
                <div class="zhijian-btn-box">
                    <div class="zhijian-btn-confirm" @click="submitForm('formValidate')">确定</div>
                </div>
    </div>
</template>
<script>
export default {
  name: "bannerManagement",
  data() {
    return {
      module1: null,
      h5Img: "",
      isShow: true,
      startDate: "",
      endDate: "",
      posterid: "",
      formValidate: {
        path: "",
        // link: "",
        is_show: "1"
      },
      ruleValidate: {
        is_show: [{ required: true, message: "请选择状态", trigger: "change" }]
      },
      posterlist: []
    };
  },
  created() {
    this.getdata();
  },
  methods: {
    //获取列表数据
    getdata() {
      this.$http.get(this.PATH.PCPOSTERLIST).then(success => {
        console.log(success);
        if (success.status == 200) {
          if (success.data.errno == 0) {
            let posterlist = success.data.data;
            this.h5Img = posterlist[0].pic;
            this.startDate = posterlist[0].start_time;
            this.endDate = posterlist[0].end_time;
            this.formValidate.path = posterlist[0].jump_url;
            this.formValidate.is_show = posterlist[0].is_show + "";
            this.posterid = posterlist[0].id;
          } else {
            this.$Modal.error({
              width: 360,
              content: success.data.errmsg
            });
          }
        }else {
          this.$Message.error("Fail!");
        }
      });
    },
    //获取选择的开始时间
    getStart(value) {
      this.startDate = value;
    },
    //获取结束时间
    getEnd(value) {
      this.endDate = value;
    },
    //上传图片
    onUpload(e) {
      let files = e.target.files || e.dataTransfer.files;
      if (!files.length) return;
      let type = e.target.files[0].type;
      let typeArr = ["png", "jpg", "jpeg", "gif", "bmp"];

      var reads = new FileReader();
      reads.readAsDataURL(files[0]);
      let that = this;
      reads.onload = function(e) {
        var fd = new FormData();
        fd.append("data", this.result);
        let config = {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        };
        that.$http
          .post("/api/v1_0/uploadimage", {
            type: "jpg",
            data: this.result
          })
          .then(
            success => {
              if (success.data.status == "0") {
                that.isShow = true;
                that.h5Img = success.data.url;
                that.$refs.formValidate.validateField("uploadimg");
              } else {
                that.$Modal.error({
                  title: "提示",
                  // content:'上传失败，请重试'
                  content: success.data.msg
                });
              }
            },
            error => {
              this.$Modal.error({
                title: "提示",
                content: success.data.msg
              });
            }
          );
      };
    },
    //提交
    submitForm(name) {
      console.log("确定");
      // this.isHide = false;
      // this.isLoding = true;

      this.$refs[name].validate(valid => {
        if (valid) {
          // console.log(this.formValidate1.link);
          let path = "";
          let params = new Object();
          path = this.PATH.UPDATEPOSTER;
          params = {
            poster_id: this.posterid,
            jump_url: this.formValidate.path,
            start_time: this.startDate,
            end_time: this.endDate,
            pic: this.h5Img,
            is_show: this.formValidate.is_show
          };
          this.$http.post(path, params).then(success => {
            console.log(success);
            if (success.status == 200) {
              this.$Modal.error({
                width: 360,
                content: success.data.errmsg
              });
              this.getdata();
            }
            //   this.addLinkModal = false;
            //   this.formValidate1.link = "";
            this.getData();
            // } else {
            //   this.$Modal.error({
            //     width: 360,
            //     content: success.data.errmsg
            //   });
            // }
          });
        } else {
          this.$Message.error("Fail!");
        }
      });
    }
  }
};
</script>
<style lang="scss">
#bannerManagement {
  height: 100%;
  padding: 20px;
  width: 100%;
  box-sizing: border-box;
  -webkit-box-sizing: border-box;
  .h1 {
    font-size: 22px;
    color: #808080;
    margin: 12px;
  }
  .schoolManagement_container {
    width: 90%;
    margin: 20px auto auto auto;
    &:after {
      content: "";
      display: block;
      clear: both;
    }
    > div {
      &:nth-of-type(1) {
        width: 70%;
        float: left;
      }
      &:nth-of-type(2) {
        width: 30%;
        float: right;
        > img {
          width: 100%;
        }
      }
    }
  }
}
</style>
