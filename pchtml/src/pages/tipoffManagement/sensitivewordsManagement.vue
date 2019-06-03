<template>
  <div id="sensitivewordsManagement">
    <div class="h1">
      文章敏感词管理
      <!-- <div class="search">
        <Input v-model="words" search enter-button="搜索" @on-search="search" placeholder="请输入搜索关键字"/>
      </div>-->
    </div>
    <div class="header">
      <Button
        class="newbtn zhijian-new-btn"
        v-if="table.data.length === 0"
        type="primary"
        @click="showEditModal('new')"
      >新增</Button>
    </div>
    <Table class="zhijian-table account-table" stripe :columns="table.columns" :data="table.data"></Table>

    <Modal :mask-closable="false" v-model="editModal" width="535" class-name="ma-edit-modal">
      <div class="edit-modal-body">
        <Icon type="android-close" @click="editModal=false"></Icon>
        <div v-if="formValidate.type=='new'" class="title">新增标签</div>
        <div v-if="formValidate.type=='edit'" class="title">编辑标签</div>
        <Form ref="formValidate" :model="formValidate" :rules="ruleValidate" :label-width="100">
          <FormItem label="敏感词" prop="sensitive_words">
            <Input
              v-model="formValidate.sensitive_words"
              autosize
              type="textarea"
              placeholder="关键词之间请用逗号隔开"
            ></Input>
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
  name: "sensitivewordsManagement",
  data() {
    return {
      editModal: false,
      table: {
        columns: [
          {
            title: "敏感词",
            key: "sensitive_words",
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
                        content: "确定删除吗?",
                        onOk: () => {
                          this.$http
                            .post(this.PATH.DELSENSITIVEWORDS, {
                              sensitive_id: [params.row.sensitive_id]
                            })
                            .then(res => {
                              if (res.data.errno === 0) {
                                console.log("shanchu");
                                this.getSensitiveList();
                              }
                            });
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
        row: {},
        sensitive_words: ""
      },
      ruleValidate: {
        sensitive_words: [
          { required: true, message: "请输入一级关键词", trigger: "blur" }
        ]
      }
    };
  },
  methods: {
    //获取关键词列表
    getSensitiveList() {
      this.$http.get(this.PATH.SENSITIVEWORDSLS).then(res => {
        console.log(res);
        if (res.data.errno == 0) {
          console.log("res.data.data", res.data.data);
          var arr = Object.keys(res.data.data);
          if (arr.length !== 0) {
            console.log("111");
            this.table.data = [res.data.data];
          } else {
            this.table.data = [];
          }
        } else {
          this.$Modal.error({
            width: 360,
            content: res.data.errmsg
          });
        }
      });
    },
    showEditModal(type, row) {
      // 显示添加爆料类型
      this.formValidate.type = type;
      if (type == "new") {
        //对整个表单进行重置，将所有字段值重置为空并移除校验结果
        this.$refs.formValidate.resetFields();
        this.formValidate.sensitive_words = "";
        this.formValidate.style = 1;
      } else {
        this.formValidate.sensitive_words = row.sensitive_words;
        this.formValidate.sensitive_id = row.sensitive_id;
        this.formValidate.style = 2;
      }
      this.editModal = true;
    },
    //提交表单数据给后台
    submitForm(name) {
      this.$refs[name].validate(valid => {
        if (valid) {
          let type = this.formValidate.type;
          let path = this.PATH.SENSITIVEWORDSUPDATE;
          let params = new Object();
          if (type == "new") {
            params = {
              sensitive_words: this.formValidate.sensitive_words,
              style: this.formValidate.style
            };
          } else {
            params = {
              sensitive_id: this.formValidate.sensitive_id,
              sensitive_words: this.formValidate.sensitive_words,
              style: this.formValidate.style
            };
          }
          this.$http.post(path, params).then(res => {
            console.log(res);
            if (res.data.errno === 0) {
              this.editModal = false;
              this.getSensitiveList();
            }
          });
        } else {
          this.$Message.error("Fail!");
        }
      });
    }
  },

  created() {
    this.getSensitiveList();
  }
};
</script>
<style lang="scss">
#sensitivewordsManagement {
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
  .search {
    width: 200px;
    position: absolute;
    top: 132px;
    right: 160px;
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
  //新增编辑弹框
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
  }
}
</style>
