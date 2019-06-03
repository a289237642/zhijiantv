<template>
  <div id="advList">
    <div class="h1">换量列表</div>
    <!-- 新增 -->
    <div class="header">
      <Button
        class="newbtn zhijian-new-btn"
        :disabled="table.data.length >= 10"
        type="primary"
        @click="showEditModal('new')"
      >新增</Button>
    </div>
    <Table class="zhijian-table account-table" stripe :columns="table.columns" :data="table.data"></Table>
    <div class="zhijian-pagination">
      <Page
        :total="table.total"
        :current="table.page"
        show-elevator
        @on-change="changePage"
        :pageSize="table.pagesize"
      ></Page>
    </div>
    <!-- 新增、编辑弹框 -->
    <Modal :mask-closable="false" v-model="editModal" width="535" class-name="ma-edit-modal">
      <div class="edit-modal-body">
        <Icon type="android-close" @click="editModal=false"></Icon>
        <div v-if="formValidate.type=='new'" class="title">新增换量</div>
        <div v-if="formValidate.type=='edit'" class="title">编辑换量</div>
        <Form
          ref="formValidate"
          :model="formValidate"
          :rules="ruleValidate"
          :label-width="100"
          class="edit-form"
        >
          <FormItem label="排序" prop="sort_num">
            <Input v-model="formValidate.sort_num" placeholder="请输入排序号"></Input>
          </FormItem>
          <FormItem label="广告图片" prop="uploadimg">
            <div class="h5ImgBox" v-if="isShow">
              <img :src="h5Img" style="width:198px;height:98px;">
            </div>
            <div>
              <label for="inputFile" class="button">
                <span class="upload__select">点击上传图片</span>
                <input
                  type="file"
                  id="inputFile"
                  accept="image/gif, image/jpeg, image/png, image/jpg"
                  style="display:none"
                  @change="onUpload"
                >
              </label>
            </div>
          </FormItem>
          <FormItem label="奖励钢镚数" prop="coin">
            <Input v-model="formValidate.coin" placeholder="请输入奖励钢镚数"></Input>
          </FormItem>
          <FormItem label="appId">
            <Input v-if="formValidate.type=='edit'" v-model="formValidate.app_id" disabled></Input>
            <Input v-if="formValidate.type=='new'" v-model="formValidate.app_id"></Input>
          </FormItem>
          <FormItem label="文案信息" prop="words">
            <Input v-model="formValidate.words"></Input>
          </FormItem>
          <FormItem label="小程序名称" prop="name">
            <Input v-model="formValidate.name"></Input>
          </FormItem>
          <FormItem label="换量路径" prop="path">
            <Input v-model="formValidate.path"></Input>
          </FormItem>
          <FormItem label="状态" prop="is_show">
            <RadioGroup v-model="formValidate.is_show">
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
  name: "advList",
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
      isLoding: false,
      table: {
        page: 1,
        pagesize: 10,
        total: 50,
        columns: [
          {
            title: "排序",
            key: "sort_num",
            align: "center"
          },
          {
            title: "图片",
            key: "img_url",
            align: "center",
            render: (h, params) => {
              return h("img", {
                attrs: {
                  src: params.row.img_url
                },
                style: {
                  width: "70px",
                  height: "35px"
                }
              });
            }
          },
          {
            title: "钢镚数",
            key: "coin",
            align: "center"
          },
          {
            title: "文案信息",
            key: "words",
            align: "center"
          },
          {
            title: "appId",
            key: "app_id",
            align: "center"
          },
          {
            title: "小程序名称",
            key: "name",
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
                      params.row.is_show == "1"
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
                      this.showEditModal("edit", params.row);
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
        sort_num: "",
        name: "",
        is_show: "1",
        coin: "",
        words: "",
        path: ""
      },
      ruleValidate: {
        coin: [
          {
            required: true,
            message: "请输入奖励钢镚数",
            pattern: /^[0-9]*$/,
            trigger: "blur"
          }
        ],
        sort_num: [
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
        words: [
          {
            required: true,
            message: "请输入文案信息",
            trigger: "blur"
          }
        ],
        name: [
          {
            required: true,
            message: "请输入小程序名称",
            trigger: "blur"
          }
        ]
        // is_show: [{ required: true, message: "请选择状态", trigger: "change" }]
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
        .post(this.PATH.MINIPROGRAMLS, {
          page: this.table.page,
          pagesize: this.table.pagesize
        })
        .then(success => {
          console.log(success);
          if (success.status == 200) {
            if (success.data.errno == 0) {
              this.table.data = success.data.data;
              this.table.data.coin = 5;
              this.table.total = success.data.count;
            } else {
              this.$Modal.error({
                width: 360,
                content: success.data.errmsg
              });
            }
          } else {
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
      // console.log("params", params);
      this.$http
        .post(this.PATH.MINICHANGESTATUS, {
          mini_program_id: params.mini_program_id
        })
        .then(success => {
          // console.log(success, "111");
          if (success.data.errno == "0") {
            this.$Modal.success({
              width: 360,
              content: success.data.errmsg,
              onOk: () => {
                this.getdata();
              }
            });
          }
        });
    },
    //删除
    deleteBanner(params) {
      console.log(params, "del");
      let paramss = [];
      paramss.push(params.mini_program_id);
      this.$http
        .post(this.PATH.DELMINIPROGRAM, {
          mini_program_id_list: paramss
        })
        .then(success => {
          console.log(success.data);
          if (success.data.errno == 0) {
            this.$Modal.success({
              width: 360,
              content: success.data.errmsg,
              onOk: () => {
                this.getdata();
              }
            });
          } else {
            this.$Message.error(success.data.errmsg);
          }
        });
    },
    //展示弹框
    showEditModal(type, row) {
      console.log(row, "展示");
      // this.getgroups(); //获取文章类型列表
      // 显示添加分组、编辑
      this.formValidate.type = type;
      //对整个表单进行重置，将所有字段值重置为空并移除校验结果
      this.$refs.formValidate.resetFields();
      if (type == "new") {
        this.formValidate.mini_program_id = "";
        this.isShow = false;
        this.h5Img = "";
        this.formValidate.row = {
          mini_program_id: "",
          sort_num: "",
          name: "",
          is_show: "1",
          coin: "",
          app_id: "",
          words: "",
          path: ""
        };
        this.arcCate = "";
        this.arcId = "";
      } else {
        console.log(row, "row");
        this.isShow = true;
        this.h5Img = row.img_url;
        this.formValidate.mini_program_id = row.mini_program_id;
        this.formValidate.sort_num = row.sort_num;
        this.formValidate.name = row.name;
        this.formValidate.is_show = row.is_show + "";
        this.formValidate.coin = row.coin;
        this.formValidate.app_id = row.app_id;
        this.formValidate.words = row.words;
        this.formValidate.path = row.path;
      }
      this.editModal = true;
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
            params = {
              sort_num: this.formValidate.sort_num,
              name: this.formValidate.name,
              is_show: this.formValidate.is_show,
              img_url: this.h5Img,
              coin: this.formValidate.coin,
              app_id: this.formValidate.app_id,
              words: this.formValidate.words,
              path: this.formValidate.path
            };
          } else {
            params = {
              mini_program_id: this.formValidate.mini_program_id,
              sort_num: this.formValidate.sort_num,
              name: this.formValidate.name,
              is_show: this.formValidate.is_show,
              coin: this.formValidate.coin,
              app_id: this.formValidate.app_id,
              words: this.formValidate.words,
              path: this.formValidate.path,
              img_url: this.h5Img
            };
          }
          console.log("create", params);
          this.$http.post(this.PATH.UPDATEMINIPROGRAM, params).then(success => {
            console.log(success.data);
            if (this.formValidate.type == "new") {
              if (success.data.errno == "0") {
                this.$Modal.success({
                  title: "提示",
                  content:
                    success.data.errmsg == "OK"
                      ? "设置成功"
                      : success.data.errmsg,
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
                    success.data.errmsg == "OK"
                      ? "设置成功"
                      : success.data.errmsg,
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
#advList {
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
  .demo-spin-col {
    position: absolute;
    top: 50%;
    left: 60%;
    transform: translate(-50%, -60%);
  }
}
</style>
