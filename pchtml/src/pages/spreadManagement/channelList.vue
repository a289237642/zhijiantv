<template>
  <div id="channelList">
    <div class="h1">渠道列表</div>
    <!-- 新增 -->
    <div class="header">
      <Input
        search
        enter-button="搜索"
        placeholder="快速搜索"
        class="search"
        @on-search="getSearch"
        @on-blur="table.page = 1"
        @on-enter="table.page = 1"
        v-model="searchValue"
      />
      <Button class="newbtn zhijian-new-btn" type="primary" @click="showEditModal('new')">新增</Button>
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
        <div v-if="formValidate.type=='new'" class="title">新增渠道</div>
        <div v-if="formValidate.type=='edit'" class="title">编辑渠道</div>
        <Form
          ref="formValidate"
          :model="formValidate"
          :rules="ruleValidate"
          :label-width="100"
          class="edit-form"
        >
          <FormItem label="渠道名称" prop="spread_name">
            <Input v-model="formValidate.spread_name" placeholder="请输入渠道名称"></Input>
          </FormItem>
          <FormItem label="推广形式" prop="spread_type_id">
            <Select v-model="formValidate.spread_type_id">
              <Option
                v-for="item in spreadTypeList"
                :value="item.spread_type_id"
                :key="item.spread_type_id"
              >{{item.spread_type_name}}</Option>
            </Select>
          </FormItem>
        </Form>
      </div>
      <div class="zhijian-btn-box">
        <div class="zhijian-btn-confirm" @click="submitForm('formValidate')">确定</div>
      </div>
    </Modal>
  </div>
</template>
<script>
export default {
  name: "channelList",
  data() {
    return {
      isShow: false, // 显示图片
      editModal: false, // 新增编辑弹框
      spreadTypeList: [],
      is_search: false,
      searchValue: "",
      table: {
        page: 1,
        pagesize: 10,
        total: 50,
        columns: [
          {
            title: "序号",
            key: "location",
            align: "center",
            width: 150
          },

          {
            title: "渠道名称",
            key: "spread_name",
            align: "center"
          },
          {
            title: "推广形式",
            align: "center",
            width: 150,
            render: (h, params) => {
              return h(
                "div",
                params.row.spread_type_id === 1
                  ? "海报"
                  : params.row.spread_type_id === 2
                  ? "直跳"
                  : params.row.spread_type_id === 3
                  ? "公众号"
                  : ""
              );
            }
          },
          {
            title: "链接",
            key: "spread_url",
            align: "center"
          },
          {
            title: "操作",
            align: "center",
            render: (h, params) => {
              return h("div", [
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
                      this.$Modal.confirm({
                        content: "是否删除该渠道？",
                        onOk: res => {
                          this.deleteSperad(params.row);
                        }
                      });
                    }
                  }
                })
              ]);
            }
          }
        ],
        data: []
      },
      formValidate: {
        type: "new",
        spread_name: "",
        spread_type_name: ""
      },
      ruleValidate: {
        spread_name: [
          {
            required: true,
            message: "请输入渠道名称",
            trigger: "blur"
          }
        ],
        spread_type_id: [
          {
            required: true,
            message: "请选择推广形式",
            trigger: "blur",
            type: "number"
          }
        ]
      }
    };
  },
  created() {
    this.getdata(this.table.page, this.table.pagesize);
    this.getspreadtype();
  },
  methods: {
    //获取列表数据
    getdata(page, pagesize) {
      this.$http
        .post(this.PATH.SPREADNAMELS, {
          page: page,
          pagesize: pagesize
        })
        .then(success => {
          console.log(success, "列表");
          if (success.status == 200) {
            if (success.data.errno == 0) {
              this.table.data = success.data.data;
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
    // 获取渠道推广方式
    getspreadtype() {
      this.$http.get(this.PATH.SPREADTYPE).then(res => {
        console.log(res, 11);
        if (res.status == 200) {
          if (res.data.errno == 0) {
            this.spreadTypeList = res.data.data;
          } else {
            this.$Modal.error({
              width: 360,
              content: res.data.errmsg
            });
          }
        }
      });
    },
    //分页
    changePage(page) {
      this.table.page = page;
      console.log("this.table.page", this.table.page);
      if (this.is_search) {
        this.getSearch();
      } else {
        this.getdata(page, this.table.pagesize);
      }
    },
    //删除
    deleteSperad(params) {
      console.log(params, "del");
      this.$http
        .post(this.PATH.SPREADNAMEDEL, {
          spread_id: params.spread_id
        })
        .then(success => {
          console.log(success, "删除");
          if (success.data.errno == 0) {
            this.getdata(this.table.page, this.table.pagesize);
            // this.$Modal.success({
            //   width: 360,
            //   content: success.data.errmsg,
            //   onOk: () => {
            //   }
            // });
          } else {
            this.$Message.error(success.data.errmsg);
          }
        });
    },
    //展示弹框
    showEditModal(type, row) {
      console.log(row, "展示");
      // 显示添加分组、编辑
      this.formValidate.type = type;
      //对整个表单进行重置，将所有字段值重置为空并移除校验结果
      this.$refs.formValidate.resetFields();
      if (type == "new") {
        this.formValidate.spread_name = "";
        this.formValidate.spread_type_id = "";
      } else {
        this.formValidate.spread_name = row.spread_name;
        this.formValidate.spread_type_id = row.spread_type_id;
        this.formValidate.spread_id = row.spread_id;
      }
      this.editModal = true;
    },
    //提交
    submitForm(name) {
      this.$refs[name].validate(valid => {
        if (valid) {
          let type = this.formValidate.type;
          let params = new Object();
          if (type == "new") {
            //新增
            params = {
              spread_name: this.formValidate.spread_name,
              spread_type_id: this.formValidate.spread_type_id
            };
          } else {
            params = {
              spread_name: this.formValidate.spread_name,
              spread_type_id: this.formValidate.spread_type_id,
              spread_id: this.formValidate.spread_id
            };
          }
          console.log("create", params);
          this.$http.post(this.PATH.SPREADNAMEUPDATE, params).then(success => {
            console.log(success.data);
            if (success.data.errno == "0") {
              this.generateSperadUrl(
                success.data.spread_id,
                params.spread_type_id
              );
            } else {
              this.$Modal.success({
                title: "提示",
                content: success.data.errmsg,
                onOk: () => {
                  this.editModal = false;
                }
              });
            }
            // this.table.page = 1;
            // this.getdata(this.table.page, this.table.pagesize);
          });
        } else {
          this.$Message.error(success.data.errmsg);
        }
      });
    },
    // 生成链接
    generateSperadUrl(spread_id, spread_type_id) {
      let sTyId = spread_type_id;
      let sId = spread_id;
      let params = new Object();
      if (sTyId == 1) {
        //海报
        params = {
          spread_id: spread_id,
          page: "pages/changehome/main",
          scene: "sid=" + sId + "&sTyId=" + sTyId
        };
      } else if (sTyId == 2) {
        // 直跳
        params = {
          spread_id: spread_id,
          path:
            "pages/changehome/main?spread_id=" +
            sId +
            "&spread_type_id=" +
            sTyId
        };
      } else {
        // 公众号
        params = {
          spread_id: spread_id,
          path:
            "pages/changehome/main?spread_id=" +
            sId +
            "&spread_type_id=" +
            sTyId
        };
      }
      this.$http.post(this.PATH.GENERATESPERATEURL, params).then(res => {
        console.log(res, 222);
        if (res.status == 200) {
          if (res.data.errno == "0") {
            this.$Modal.success({
              title: "提示",
              content: res.data.errmsg == "OK" ? "设置成功" : res.data.errmsg,
              onOk: () => {
                this.editModal = false;
              }
            });
            this.table.page = 1;
            this.getdata(this.table.page, this.table.pagesize);
          } else {
            this.$Modal.success({
              title: "提示",
              content: res.data.errmsg,
              onOk: () => {}
            });
          }
        }
      });
    },
    /**
     * 获取搜索框的输入值
     */
    getSearch() {
      this.is_search = true;
      this.$http
        .post(this.PATH.SPREADNAMESEARCH, {
          page: this.table.page,
          pagesize: this.table.pagesize,
          words: this.searchValue
        })
        .then(success => {
          console.log(success, "搜索");
          if (success.status == 200) {
            if (success.data.errno == 0) {
              this.table.data = success.data.data;
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
    }
  }
};
</script>
<style lang="scss">
#channelList {
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
    height: 50px;
    margin-top: 20px;
    position: relative;
    .search {
      width: 200px;
      position: absolute;
      // top: 75px;
      right: 120px;
    }
    .newbtn {
      font-size: 12px;
      line-height: 10px;
      height: 32px;
      position: absolute;
      // top: 75px;
      right: 20px;
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
