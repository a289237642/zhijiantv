<template>
    <div id="bannerManagement">
       <div class="h1">banner管理</div>
       <!-- 新增 -->
        <div class="header">
            <Button class="newbtn zhijian-new-btn" type="primary" @click="showEditModal('new')">新增</Button>
        </div>
       <Table class="zhijian-table account-table" stripe :columns="table.columns" :data="table.data"></Table>
        <div class="zhijian-pagination">
            <Page :total="table.total" :current="table.page" show-elevator @on-change="changePage" :pageSize="table.pagesize"></Page>
        </div>
        <!-- 新增、编辑弹框 -->
        <Modal :mask-closable="false" v-model="editModal" width="535" class-name="ma-edit-modal">
            <div class="edit-modal-body">
                <Icon type="android-close" @click="editModal=false"></Icon>
                <div v-if="formValidate.type=='new'" class="title">新增banner</div>
                <div v-if="formValidate.type=='edit'" class="title">编辑banner</div>
                <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="100" class="edit-form">
                    <FormItem label="排序" prop="sort">
                        <Input v-model="formValidate.sort" placeholder="请输入排序号"></Input>
                    </FormItem>
                    <FormItem label="活动图片" prop="uploadimg">
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
                    <FormItem label="跳转链接" >
                        <Input v-model="formValidate.link" placeholder="请输入链接"></Input>
                    </FormItem>
                    <FormItem label="跳转文章类型" prop="articlecategory" >
                         <Select v-model="arcCate" @on-change="getArticle">
                           <Option value="">不选择跳转文章类型</Option>
                            <Option v-for="item in arcCateList"  :value="item.group_id" :key="item.group_id">{{ item.group_name }}</Option>
                        </Select>
                    </FormItem>
                     <FormItem label="选择跳转文章" prop="article" >
                         <Select v-model="arcId"   @on-change="searchArc" >
                           <Option value="">不选择跳转文章</Option>
                            <Option v-for="item in arcList" :value="item.article_id" :key="item.article_id">{{ item.title }}</Option>
                        </Select>
                    </FormItem>
                    <FormItem label="状态" prop="status">
                        <RadioGroup v-model="formValidate.status">
                            <Radio label="1">启用</Radio>
                            <Radio label="0">禁用</Radio>
                        </RadioGroup>
                    </FormItem>
                </Form>
            </div>
            <div class="zhijian-btn-box">
                <div class="zhijian-btn-confirm" @click="submitForm('formValidate')">确定</div>
            </div>
            <Col class="demo-spin-col" span="8" v-show="isLoding">
                   <Spin size="large"></Spin>
              </Col>
        </Modal>
    </div>
</template>
<script>
export default {
  name: "bannerManagement",
  data() {
    const validateImg = (rule, value, callback) => {
      if (this.h5Img == "") {
        callback(
          new Error(
            "请上传活动图片(大小不超过2M, 只支持png,jpg,jpeg,gif,bmp格式)"
          )
        );
      } else {
        callback();
      }
    };
    return {
      isShow: false, // 显示图片
      editModal: false, // 新增编辑弹框
      arcCate: "",
      arcCateList: [],
      arcId: "",
      arcList: [],
      isLoding:false,
      table: {
        page: 1,
        pagesize: 10,
        total: 50,
        columns: [
          {
            title: "排序",
            key: "location",
            align: "center"
          },
          {
            title: "图片",
            key: "image",
            align: "center",
            render: (h, params) => {
              return h("img", {
                attrs: {
                  src: params.row.image
                },
                style: {
                  width: "35px",
                  height: "35px"
                }
              });
            }
          },
          {
            title: "跳转模块",
            key: "link",
            align: "center"
          },
          {
            title: "操作",
            align: "center",
            width: 150,
            render: (h, params) => {
              return h("div", [
                h("i", {
                  attrs: {
                    class:
                      params.row.status == "1"
                        ? "iconfont icon-yanjing"
                        : "iconfont icon-yanjing-bi"
                  },
                  on: {
                    click: () => {
                      this.changeBannerStatus(params.row);
                    }
                  }
                }),
                h("i", {
                  attrs: {
                    class: "iconfont icon-edit"
                  },
                  on: {
                    click: () => {
                      this.getgroups();
                      this.getArticle1(params.row);
                      // let that = this;
                      // setTimeout(function(){
                      //   that.showEditModal("edit", params.row);
                      // },2000);
                      
                    }
                  }
                }),
                h("i", {
                  attrs: {
                    class: "iconfont icon-delete"
                  },
                  style: {
                    color: "#ffc639"
                  },
                  on: {
                    click: () => {
                      this.deleteBanner(params.row);
                    }
                  }
                })
              ]);
            }
          }
        ],
        data: []
      },
      h5Img: "",
      formValidate: {
        type: "new",
        row: {},
        sort: "",
        // link: "",
        status: "1"
      },
      ruleValidate: {
        sort: [
          {
            required: true,
            message: "请输入排序号",
            pattern: /^[0-9]*$/,
            trigger: "blur"
          }
        ],
        uploadimg: [
          {
            required: true,
            validator: validateImg,
            trigger: "blur"
          }
        ],
        // link: [{ required: true, message: "请输入链接", trigger: "blur" }],
        status: [{ required: true, message: "请选择状态", trigger: "change" }]
      
      }
    };
  },
  created() {
    this.getdata();
  },
  methods: {
    //获取列表数据
    getdata() {
      this.$http
        .post(this.PATH.GETPXBANNER, {
          page: this.table.page,
          size: this.table.pagesize
        })
        .then(success => {
          console.log(success);
          if(success.status==200){
            if(success.data.errno==0){
               this.table.data = success.data.list;
            this.table.total = success.data.total;
            }else {
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
    //分页
    changePage(page) {
      this.table.page = page;
      this.getdata();
    },
    //修改banner状态
    changeBannerStatus(params) {
      this.$http
        .post(this.PATH.CHANGEBANNERTATUS, {
          id: params.id,
          status: params.status
        })
        .then(success => {
          console.log(success.data,'111')
          if (success.data.errno == "0") {
            this.$Modal.success({
              width: 360,
              content: success.data.msg,
              onOk: () => {
                this.getdata();
              }
            });
          }
        });
    },
    //删除
    deleteBanner(params) {
      // console.log(params)
      this.$http
        .post(this.PATH.DELETEBANNER, {
          id: params.id
        })
        .then(success => {
          console.log(success.data)
          if (success.data.errno == "0") {
            this.$Modal.success({
              width: 360,
              content: success.data.msg,
              onOk: () => {
                this.getdata();
              }
            });
          }else{
            this.$Message.error(success.data.errmsg);
          }
        });
    },
    //展示弹框
    showEditModal(type, row) {

      console.log(row)
      // this.getgroups(); //获取文章类型列表
      // 显示添加分组、编辑
      this.editErrorTip = false;
      this.formValidate.type = type;
      //对整个表单进行重置，将所有字段值重置为空并移除校验结果
      this.$refs.formValidate.resetFields();
      if (type == "new") {
        this.getgroups();
        this.formValidate.id = "";
        this.isShow = false;
        this.h5Img = "";
        this.formValidate.row = {
          id: "",
          sort: "",
          link: "",
          status: "1"
        };
        this.arcCate = "";
        this.arcId = "";
      } else {

        console.log(row.group_id,'row');
        this.isShow = true;
        this.h5Img = row.image;
        this.formValidate.id = row.id;
        this.formValidate.sort = row.sort;
        this.formValidate.link = row.link;
        this.formValidate.status = row.status;
        this.arcCate = row.group_id;
        this.arcId = row.article_id;
        console.log(this.arcCate,'this.arcCate');
        console.log(this.arcId,'this.arcId');

      }
      this.editModal = true;
    },
    //获取跳转文章类别
    getgroups() {
      this.$http.get(this.PATH.GROUPS).then(res => {
        // console.log(res);
        if (res.data.errno == 0) {
          this.arcCateList = res.data.data;
        } else {
          this.$Modal.error({
            width: 360,
            content: res.data.errmsg
          });
        }
      });
    },
    //根据类型获取对应文章
    getArticle(value) {
      // console.log(value);
      this.arcList=[];
      this.arcId = "";
      this.arcCate = value; //拿到要跳转的文章类型ID
      this.$http
        .post(this.PATH.PCARTICLETITLE, {
          group_id: value
        })
        .then(res => {
          console.log(res.data);
          if (res.status == 200) {
            this.arcList = res.data.data;
          }
        });
    },
    //根据类型获取对应文章
    getArticle1(row) {
      this.editModal = true;
      this.isLoding = true;
      this.formValidate.id = "";
      this.isShow = false;
      this.h5Img = "";
      this.formValidate.row = {
        id: "",
        sort: "",
        link: "",
        status: "1"
      };
      this.arcCate = "";
      this.arcId = "";
      this.$http
        .post(this.PATH.PCARTICLETITLE, {
          group_id: row.group_id
        })
        .then(res => {
          console.log(res.data);
          if (res.status == 200) {
            this.arcList = res.data.data;
            console.log(row.group_id,'row');
            this.isShow = true;
            this.h5Img = row.image;
            this.formValidate.id = row.id;
            this.formValidate.sort = row.sort;
            this.formValidate.link = row.link;
            this.formValidate.status = row.status;
            this.arcCate = row.group_id;
            this.arcId = row.article_id;
            console.log(this.arcCate,'this.arcCate');
            console.log(this.arcId,'this.arcId');
            this.isLoding = false;
          }
        });
    },
    //选择跳转文章
    searchArc(query) {
      // console.log(query);
      this.arcId = query; //选择跳转文章的ID
    },
    //提交
    submitForm(name) {
      this.$refs[name].validate(valid => {
        if (valid) {
          let type = this.formValidate.type;
          let path = "";
          let params = new Object();
          if (type == "new") {
            //新增
            path = this.PATH.CREATEBANNER;
            params = {
              sort: this.formValidate.sort,
              link: this.formValidate.link,
              status: this.formValidate.status,
              image: this.h5Img,
              group_id: this.arcCate,
              article_id: this.arcId
            };
          } else {
            path = this.PATH.CHANGEBANNER;
            params = {
              id: this.formValidate.id,
              sort: this.formValidate.sort,
              link: this.formValidate.link,
              status: this.formValidate.status,
              image: this.h5Img,
              group_id: this.arcCate,
              article_id: this.arcId
            };
          }
          this.$http.post(path, params).then(success => {
            console.log(success.data);
            if (this.formValidate.type == "new") {
              if (success.data.errno == "0") {
                this.$Modal.success({
                  title: "提示",
                  content:
                    success.data.msg == "success"
                      ? "设置成功"
                      : success.data.msg,
                  onOk: () => {
                    this.editModal = false;
                  }
                });
              } else {
                 this.$Modal.success({
                  title: "提示",
                  content: success.data.errmsg,
                  onOk: () => {
                    this.editModal = false;
                  }
                });
              }
            } else {
              if (success.data.errno == "0") {
                this.$Modal.success({
                  title: "提示",
                  content:
                    success.data.msg == "success"
                      ? "设置成功"
                      : success.data.msg,
                  onOk: () => {
                    this.editModal = false;
                  }
                });
              }else{
                 this.$Modal.success({
                  title: "提示",
                  content: success.data.errmsg,
                  onOk: () => {
                    this.editModal = false;
                  }
                });
              }
            }
            this.table.page = 1;
            this.getdata();
          });
        } else {
          this.$Message.error(success.data.errmsg);
        }
      });
    },
    //上传图片
    onUpload(e) {
      let files = e.target.files || e.dataTransfer.files;
      if (!files.length) return;
      let type = e.target.files[0].type;
      let typeArr = ["png", "jpg", "jpeg", "gif", "bmp"];
      // if(type == "" || typeArr.indexOf(type.split("/")[1])<0 || e.target.files[0].size >2*1024*1024) {
      //     this.h5Img = '';
      //     this.$refs.formValidate.validateField("qrcard")
      //     return;
      // }
      var reads = new FileReader();
      reads.readAsDataURL(files[0]);
      let that = this;
      // console.log(reads)
      reads.onload = function(e) {
        var fd = new FormData();
        fd.append("data", this.result);
        let config = {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        };
        // console.log(this.result)
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
    &:before,
    &:after {
      display: table;
      line-height: 0;
      content: "";
    }
    &:after {
      clear: both;
    }
  }
  .account-table {
    margin-top: 20px;
  }
}

//新增编辑弹框
.ivu-radio-inner:after {
  position: absolute;
  width: 8px;
  height: 8px;
  left: 2px;
  top: 2px;
  border-radius: 6px;
  display: table;
  border-top: 0;
  border-left: 0;
  content: " ";
  background-color: #ffc639 !important;
  opacity: 0;
  transition: all 0.2s ease-in-out;
  transform: scale(0);
}
.ma-edit-modal {
  .edit-modal-body {
    position: relative;
    margin-bottom: 30px;
    font-size: 14px;
  }
  .ivu-icon-android-close {
    position: absolute;
    top: -20px;
    right: -14px;
    font-size: 24px;
    color: var(--base);
    cursor: pointer;
  }
  .title {
    margin-bottom: 24px;
    text-align: center;
    font-size: 24px;
    color: var(--base);
  }
  .ivu-radio-checked .ivu-radio-inner {
    border-color: var(--base) !important;
  }

  //弹框表单
  .edit-form {
    .error-tip {
      position: absolute;
      top: 100%;
      left: 0;
      line-height: 1;
      padding-top: 6px;
      color: #ed4958;
    }
    .role-select {
      height: 42px;
      line-height: 42px;
    }
    .department-select {
      margin-right: 12px;
    }
    .department-select,
    .job-select {
      width: 48%;
    }
  }
  .demo-spin-col{
    position: absolute;
    top:50%;
    left:60%;
    transform: translate(-50%,-60%);
  }
}
</style>
